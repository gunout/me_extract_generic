#!/usr/bin/env python3
"""
me_tui.py - Interface TUI complète pour explorer l'Intel ME
Fusion de me_tui.py + me_extract.py
Nécessite : textual (pip install textual)
Exécution : sudo ./venv/bin/python me_tui.py
"""
import os
import fcntl
import ctypes
import struct
import select
import datetime
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Button, DataTable, Static, RichLog
from textual.binding import Binding


# --- Structures noyau ---
class mei_client(ctypes.Structure):
    _fields_ = [("max_msg_length", ctypes.c_uint32),
                ("protocol_version", ctypes.c_uint8),
                ("reserved", ctypes.c_uint8 * 3)]


class mei_connect_client_data(ctypes.Union):
    _fields_ = [("in_client_uuid", ctypes.c_ubyte * 16),
                ("out_client_properties", mei_client)]


IOCTL_MEI_CONNECT_CLIENT = 0xC0104801
MEI_DEVICE = "/dev/mei0"
SYSFS_BASE = "/sys/class/mei/mei0"
GUID_MKHI = "8e6a6715-9abc-4043-88ef-9e39c6f63e0f"


# --- Utilitaires ---
def guid_to_bytes_le(guid_str):
    parts = guid_str.replace('-', '')
    d1 = bytes.fromhex(parts[0:8])[::-1]
    d2 = bytes.fromhex(parts[8:12])[::-1]
    d3 = bytes.fromhex(parts[12:16])[::-1]
    d4 = bytes.fromhex(parts[16:32])
    return d1 + d2 + d3 + d4


def read_sysfs(name):
    path = os.path.join(SYSFS_BASE, name)
    if os.path.exists(path):
        try:
            with open(path) as f:
                return f.read().strip()
        except OSError:
            return None
    return None


def hexdump_str(data, width=16):
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f'{i:08x}  {hex_part:<{width*3}}  {ascii_part}')
    return '\n'.join(lines)


def connect_me(guid_str):
    fd = os.open(MEI_DEVICE, os.O_RDWR)
    data = mei_connect_client_data()
    guid_le = guid_to_bytes_le(guid_str)
    for i in range(16):
        data.in_client_uuid[i] = guid_le[i]
    fcntl.ioctl(fd, IOCTL_MEI_CONNECT_CLIENT, data)
    return fd, data.out_client_properties


def send_mkhi(fd, group, cmd, payload=b'', timeout=2.0):
    header = struct.pack('<BBBB', group, cmd, 0x00, 0x00)
    os.write(fd, header + payload)
    r, _, _ = select.select([fd], [], [], timeout)
    if r:
        return os.read(fd, 4096)
    return None


def decode_fw_status(values):
    """Décode les registres HFSTS du ME 11 (Skylake, d'après coreboot)."""
    if len(values) < 6:
        return ["(nombre de registres insuffisant)"]

    h1, h2, h3, h4, h5, h6 = values[:6]
    lines = []

    cws = h1 & 0xF
    cws_map = {0: "Reset", 1: "Initializing", 2: "Recovery", 5: "Normal",
               6: "Platform Disable Wait", 7: "OP State Transition",
               8: "Invalid CPU Plugged In"}
    opstate = (h1 >> 6) & 0x7
    opstate_map = {0: "Preboot", 1: "M0 with UMA", 2: "M3 without UMA",
                   3: "M0 without UMA", 4: "Bring up",
                   5: "M0 without UMA but with error"}
    opmode = (h1 >> 16) & 0xF
    opmode_map = {0: "Normal", 1: "Debug", 2: "Soft Temporary Disable",
                  3: "Security Override via Jumper",
                  4: "Security Override via MEI Message"}
    err = (h1 >> 12) & 0xF
    err_map = {0: "No Error", 1: "Uncategorized Failure",
               2: "Image Failure", 3: "Debug Failure"}
    upd = (h1 >> 11) & 1

    lines.append(f"HFSTS1 (0x{h1:08x}):")
    lines.append(f"  Current Working State  : {cws} ({cws_map.get(cws, 'Unknown')})")
    lines.append(f"  Current Operation State: {opstate} ({opstate_map.get(opstate, 'Unknown')})")
    lines.append(f"  Current Operation Mode : {opmode} ({opmode_map.get(opmode, 'Unknown')})")
    lines.append(f"  Error Code             : {err} ({err_map.get(err, 'Unknown')})")
    lines.append(f"  Update In Progress     : {upd} ({'YES' if upd else 'NO'})")

    progress = (h2 >> 28) & 0xF
    progress_map = {0: "ROM Phase", 2: "uKernel Phase", 3: "BUP Phase",
                    6: "Host Communication"}
    pmevent = (h2 >> 24) & 0xF
    lines.append(f"HFSTS2 (0x{h2:08x}):")
    lines.append(f"  Progress Code  : {progress} ({progress_map.get(progress, 'Unknown')})")
    lines.append(f"  PM Event       : {pmevent}")

    lines.append(f"HFSTS3 (0x{h3:08x}): recovery_mode={(h3 >> 9) & 1}")
    lines.append(f"HFSTS4 (0x{h4:08x})")
    lines.append(f"HFSTS5 (0x{h5:08x}): crash_dump_pending={h5 & 1}")
    lines.append(f"HFSTS6 (0x{h6:08x})")

    return lines


def list_me_clients_debugfs():
    candidates = [
        "/sys/kernel/debug/mei0/meclients",
        "/sys/kernel/debug/mei/mei0/meclients",
        "/sys/kernel/debug/mei/meclients",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    return f"{path}\n\n" + f.read()
            except OSError as e:
                return f"{path}: erreur lecture: {e}"
    if os.path.exists("/sys/class/mei"):
        return f"Aucun meclients trouvé.\nDevices ME: {os.listdir('/sys/class/mei')}"
    return "Aucun device ME trouvé."


def read_dev_state():
    path = os.path.join(SYSFS_BASE, "dev_state")
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return "N/A"


# --- Application TUI ---
class MEExplorer(App):
    CSS = """
    Screen { layout: vertical; }
    #top-panel { height: 10; }
    #button-bar { height: 3; }
    #log-panel { height: 1fr; }
    DataTable { height: 100%; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quitter"),
        Binding("s", "show_sysfs", "Version FW"),
        Binding("m", "show_mkhi", "MKHI"),
        Binding("c", "show_clients", "Clients"),
        Binding("e", "extract_all", "Extraction"),
        Binding("f", "explore_extra", "FWUPDATE/CRASH"),
        Binding("ctrl+s", "save_log", "Sauver log"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="top-panel"):
            yield Static("Chargement...", id="status")
            yield DataTable(id="client-table")
        with Horizontal(id="button-bar"):
            yield Button("Version FW", id="btn-sysfs", variant="primary")
            yield Button("MKHI", id="btn-mkhi", variant="success")
            yield Button("Clients", id="btn-clients", variant="warning")
            yield Button("FWUPDATE/CRASH", id="btn-extra", variant="default")
            yield Button("Extraction complète", id="btn-extract", variant="default")
            yield Button("Sauver log", id="btn-save", variant="default")
            yield Button("Quitter", id="btn-quit", variant="error")
        yield RichLog(id="log-panel", highlight=True, markup=True, wrap=True)
        yield Footer()

    def on_mount(self):
        state = read_dev_state()
        debugfs_ok = any(os.path.exists(p) for p in [
            "/sys/kernel/debug/mei0/meclients",
            "/sys/kernel/debug/mei/mei0/meclients",
            "/sys/kernel/debug/mei/meclients",
        ])
        self.query_one("#status").update(
            f"ME device: {MEI_DEVICE} | dev_state={state} | "
            f"debugfs={'OK' if debugfs_ok else 'N/A'} | "
            f"fw_ver={read_sysfs('fw_ver') or 'N/A'}"
        )
        table = self.query_one(DataTable)
        table.add_columns("Client", "GUID", "Max msg", "Protocol")
        self.log_message("[green]Application démarrée.[/] Raccourcis: s/m/c/e/f, Ctrl+S, q")
        fw = read_sysfs("fw_ver")
        if fw:
            self.log_message(f"Version firmware actuelle:\n{fw}")

    def log_message(self, msg: str):
        """Ajoute au log RichLog et écrit aussi dans /tmp/me_tui.log."""
        self.query_one(RichLog).write(msg)
        try:
            with open("/tmp/me_tui.log", "a") as f:
                f.write(msg + "\n")
        except OSError:
            pass

    def action_show_sysfs(self):
        self._handle("btn-sysfs")

    def action_show_mkhi(self):
        self._handle("btn-mkhi")

    def action_show_clients(self):
        self._handle("btn-clients")

    def action_extract_all(self):
        self._handle("btn-extract")

    def action_explore_extra(self):
        self._handle("btn-extra")

    def action_save_log(self):
        self._handle("btn-save")

    def on_button_pressed(self, event: Button.Pressed):
        self._handle(event.button.id)

    def _handle(self, bid: str):
        if bid == "btn-quit":
            self.exit()
        elif bid == "btn-sysfs":
            self.show_sysfs()
        elif bid == "btn-mkhi":
            self.try_mkhi()
        elif bid == "btn-clients":
            clients = list_me_clients_debugfs()
            self.log_message("[cyan]─ Clients ME ─[/]")
            for line in clients.splitlines():
                self.log_message(line)
        elif bid == "btn-extra":
            self.explore_extra()
        elif bid == "btn-extract":
            self.extract_all()
        elif bid == "btn-save":
            self.log_message("[green]Log déjà écrit dans /tmp/me_tui.log[/]")

    def show_sysfs(self):
        self.log_message("[cyan]─ Sysfs /sys/class/mei/mei0/ ─[/]")
        for name in ["dev_state", "fw_ver", "fw_status", "hbm_ver", "hbm_ver_drv"]:
            val = read_sysfs(name)
            if val:
                self.log_message(f"[bold]{name}[/]:")
                for line in val.splitlines():
                    self.log_message(f"  {line}")
                if name == "fw_status":
                    try:
                        values = [int(x, 16) for x in val.splitlines()]
                        self.log_message("  [yellow](décodé):[/]")
                        for dline in decode_fw_status(values):
                            self.log_message(f"    {dline}")
                    except ValueError:
                        self.log_message("  (impossible de décoder fw_status)")
            else:
                self.log_message(f"[bold]{name}[/]: (non disponible)")

    def try_mkhi(self):
        self.log_message("[cyan]─ MKHI ─[/]")
        try:
            fd, props = connect_me(GUID_MKHI)
            self.log_message(
                f"[green]Connecté[/]: max_len={props.max_msg_length}, "
                f"protocol={props.protocol_version}"
            )
            r, _, _ = select.select([fd], [], [], 0.5)
            if r:
                passive = os.read(fd, 4096)
                self.log_message(f"Lecture passive ({len(passive)} octets):")
                self.log_message(hexdump_str(passive))
            else:
                self.log_message("Lecture passive: aucune donnée en attente")

            for name, grp, cmd in [
                ("GET_FW_VERSION", 0xFF, 0x02),
                ("GET_PLATFORM_TYPE", 0xFF, 0x03),
                ("GET_FW_CAPS", 0xFF, 0x04),
                ("GET_SKU", 0xFF, 0x08),
            ]:
                self.log_message(f"\n[bold]Commande:[/] {name} (group=0x{grp:02x}, cmd=0x{cmd:02x})")
                try:
                    resp = send_mkhi(fd, grp, cmd)
                    if resp:
                        self.log_message(f"  Réponse brute ({len(resp)} octets):")
                        self.log_message(hexdump_str(resp))
                        if len(resp) >= 8:
                            result = struct.unpack_from('<I', resp, 4)[0]
                            self.log_message(f"  Result code: 0x{result:08x}")
                    else:
                        self.log_message("  (pas de réponse / timeout)")
                except OSError as e:
                    self.log_message(f"  [red]Erreur:[/] {e}")
            os.close(fd)
        except OSError as e:
            self.log_message(f"[red]Erreur:[/] {e}")

    def explore_extra(self):
        self.log_message("[cyan]─ FWUPDATE (0x04) et CRASH (0x03) ─[/]")
        try:
            fd, _ = connect_me(GUID_MKHI)
        except OSError as e:
            self.log_message(f"[red]Erreur connexion:[/] {e}")
            return
        cmds = [
            ("FWUPDATE_GET_VERSION", 0x04, 0x01),
            ("FWUPDATE_GET_CAPS", 0x04, 0x02),
            ("CRASH_GET_INFO", 0x03, 0x01),
        ]
        for name, grp, cmd in cmds:
            self.log_message(f"\n[bold]Commande:[/] {name} (group=0x{grp:02x}, cmd=0x{cmd:02x})")
            try:
                resp = send_mkhi(fd, grp, cmd)
                if resp:
                    self.log_message(f"  Réponse brute ({len(resp)} octets):")
                    self.log_message(hexdump_str(resp))
                    if len(resp) >= 8:
                        result = struct.unpack_from('<I', resp, 4)[0]
                        self.log_message(f"  Result code: 0x{result:08x}")
                else:
                    self.log_message("  (pas de réponse / timeout)")
            except OSError as e:
                self.log_message(f"  [red]Erreur:[/] {e}")
        os.close(fd)

    def extract_all(self):
        """Génère un fichier me_dump_*.txt complet."""
        self.log_message("[cyan]─ Extraction complète vers fichier txt ─[/]")
        out = []
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"me_dump_{ts}.txt"

        def log(msg):
            out.append(msg)
            self.log_message(msg)

        log("=== Intel ME Extraction ===")
        log(f"Date: {datetime.datetime.now().isoformat()}")
        log(f"Device: {MEI_DEVICE}\n")

        # [1] Sysfs
        log("--- [1] Sysfs /sys/class/mei/mei0/ ---")
        for name in ["dev_state", "fw_ver", "fw_status", "hbm_ver", "hbm_ver_drv"]:
            val = read_sysfs(name)
            if val:
                log(f"{name}:")
                for line in val.splitlines():
                    log(f"  {line}")
                if name == "fw_status":
                    try:
                        values = [int(x, 16) for x in val.splitlines()]
                        log("  (décodé):")
                        for dline in decode_fw_status(values):
                            log(f"    {dline}")
                    except ValueError:
                        log("  (impossible de décoder fw_status)")
            else:
                log(f"{name}: (non disponible)")
        log("")

        # [2] PCI
        log("--- [2] Informations PCI du contrôleur MEI ---")
        try:
            for dev in sorted(os.listdir("/sys/bus/pci/devices")):
                base = f"/sys/bus/pci/devices/{dev}"
                vp, dp, cp = f"{base}/vendor", f"{base}/device", f"{base}/class"
                if os.path.exists(vp) and os.path.exists(dp):
                    try:
                        with open(vp) as f:
                            vendor = f.read().strip()
                        with open(dp) as f:
                            device = f.read().strip()
                        with open(cp) as f:
                            cls = f.read().strip()
                        if vendor == "0x8086" and "0780" in cls:
                            log(f"Device: {dev}")
                            log(f"  Vendor: {vendor}")
                            log(f"  Device: {device}")
                            log(f"  Class:  {cls}")
                    except OSError:
                        continue
        except Exception as e:
            log(f"Erreur scan PCI: {e}")
        log("")

        # [3] MKHI complet
        log("--- [3] Interface MKHI ---")
        try:
            fd, props = connect_me(GUID_MKHI)
            log(f"Connexion MKHI OK: max_len={props.max_msg_length}, "
                f"protocol={props.protocol_version}")
            r, _, _ = select.select([fd], [], [], 0.5)
            if r:
                passive = os.read(fd, 4096)
                log(f"Lecture passive ({len(passive)} octets):")
                log(hexdump_str(passive))
            else:
                log("Lecture passive: aucune donnée en attente")
            for name, grp, cmd in [
                ("GET_FW_VERSION", 0xFF, 0x02),
                ("GET_PLATFORM_TYPE", 0xFF, 0x03),
                ("GET_FW_CAPS", 0xFF, 0x04),
                ("GET_SKU", 0xFF, 0x08),
                ("FWUPDATE_GET_VERSION", 0x04, 0x01),
                ("FWUPDATE_GET_CAPS", 0x04, 0x02),
                ("CRASH_GET_INFO", 0x03, 0x01),
            ]:
                log(f"\nCommande: {name} (group=0x{grp:02x}, cmd=0x{cmd:02x})")
                try:
                    resp = send_mkhi(fd, grp, cmd)
                    if resp:
                        log(f"  Réponse brute ({len(resp)} octets):")
                        log(hexdump_str(resp))
                        if len(resp) >= 8:
                            result = struct.unpack_from('<I', resp, 4)[0]
                            log(f"  Result code: 0x{result:08x}")
                            if result == 0 and len(resp) > 8:
                                log(f"  Payload: {resp[8:].hex()}")
                    else:
                        log("  (pas de réponse / timeout)")
                except OSError as e:
                    log(f"  Erreur: {e}")
            os.close(fd)
        except OSError as e:
            log(f"Erreur ioctl/échange MKHI: {e}")

        log("\n--- Fin de l'extraction ---")

        try:
            with open(filename, "w") as f:
                f.write('\n'.join(out) + '\n')
            self.log_message(f"[green]✅ Fichier sauvegardé:[/] {filename}")
        except OSError as e:
            self.log_message(f"[red]Erreur écriture fichier:[/] {e}")


if __name__ == "__main__":
    MEExplorer().run()
