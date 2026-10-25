#!/bin/bash
#
# me_extract_generic.sh - Extraction générique des données Intel ME (Linux)
# Usage: sudo ./me_extract_generic.sh
#
# Ce script tente de :
#   1. Lire les données exposées par le noyau (sysfs, PCI) - sans risque
#   2. Installer et utiliser CHIPSEC pour tenter un dump SPI - RISQUE MODÉRÉ
#
# Sortie: me_dump_<hostname>_<date>.txt dans le répertoire courant
#

set -e

# --- Vérifications préliminaires ---
if [[ $EUID -ne 0 ]]; then
    echo "Erreur: ce script doit être exécuté en root (sudo)."
    exit 1
fi

OUTFILE="me_dump_$(hostname)_$(date +%Y%m%d_%H%M%S).txt"
exec > >(tee -a "$OUTFILE") 2>&1

echo "=============================================="
echo " Intel ME Extraction - Générique"
echo " Date: $(date -Iseconds)"
echo " Host: $(hostname)"
echo " Kernel: $(uname -r)"
echo "=============================================="
echo

# --- Section 1: Vérification de la présence d'un Intel ME ---
echo "--- [1] Détection de l'Intel ME ---"

MEI_PCI=$(lspci -nn 2>/dev/null | grep -i "communication controller.*8086" | head -1)
if [[ -z "$MEI_PCI" ]]; then
    echo "Aucun contrôleur MEI Intel détecté sur le bus PCI."
    echo "Cette machine n'a probablement pas d'Intel ME, ou le device est masqué."
else
    echo "Contrôleur MEI détecté:"
    echo "  $MEI_PCI"
fi
echo

# --- Section 2: Sysfs (sans risque) ---
echo "--- [2] Données sysfs (/sys/class/mei/) ---"

if [[ -d /sys/class/mei ]]; then
    for mei_dev in /sys/class/mei/mei*; do
        [[ -e "$mei_dev" ]] || continue
        echo "Device: $mei_dev"
        for attr in dev_state fw_ver fw_status hbm_ver hbm_ver_drv; do
            if [[ -f "$mei_dev/$attr" ]]; then
                echo "  $attr:"
                sed 's/^/    /' "$mei_dev/$attr"
            fi
        done
        echo
    done
else
    echo "/sys/class/mei/ n'existe pas (module mei_me non chargé ?)"
    echo "Essayez: sudo modprobe mei_me"
fi
echo

# --- Section 3: Dump SPI via CHIPSEC (tentative) ---
echo "--- [3] Dump SPI via CHIPSEC (si disponible/installable) ---"
echo "AVERTISSEMENT: CHIPSEC charge un module noyau. Risque d'instabilité."
echo

CHIPSEC_OK=0

# Vérifier si chipsec_util est déjà disponible
if command -v chipsec_util &>/dev/null; then
    echo "CHIPSEC déjà installé: $(command -v chipsec_util)"
    CHIPSEC_OK=1
else
    echo "CHIPSEC non trouvé. Tentative d'installation via pip..."
    # Créer un venv temporaire pour éviter de polluer le système
    VENV_DIR="/tmp/chipsec_venv_$$"
    python3 -m venv "$VENV_DIR" 2>/dev/null || {
        echo "Impossible de créer un venv. Installez python3-venv."
        echo "CHIPSEC ne sera pas utilisé."
    }
    if [[ -d "$VENV_DIR" ]]; then
        source "$VENV_DIR/bin/activate"
        pip install chipsec 2>&1 | tail -5
        if command -v chipsec_util &>/dev/null; then
            echo "CHIPSEC installé dans le venv."
            CHIPSEC_OK=1
        fi
        # Ne pas désactiver le venv tout de suite, on en a besoin pour la suite
    fi
fi

if [[ $CHIPSEC_OK -eq 1 ]]; then
    echo "Tentative de dump SPI avec CHIPSEC..."
    SPI_DUMP="/tmp/spi_dump_$$.bin"
    if chipsec_util spi dump "$SPI_DUMP" 2>&1; then
        echo "Dump SPI réussi: $SPI_DUMP ($(stat -c%s "$SPI_DUMP" 2>/dev/null || echo "?") octets)"
        echo
        echo "Analyse du dump avec CHIPSEC decode (si possible)..."
        chipsec_util decode "$SPI_DUMP" 2>&1 | head -50 || true
    else
        echo "Échec du dump SPI (permissions, Secure Boot, ou matériel verrouillé)."
        echo "Ce n'est pas anormal sur les machines récentes."
    fi
    rm -f "$SPI_DUMP"
else
    echo "CHIPSEC non disponible. Le dump SPI n'a pas été tenté."
    echo "Pour un dump complet, installez CHIPSEC manuellement:"
    echo "  https://github.com/chipsec/chipsec"
fi

# Nettoyage du venv si créé
if [[ -n "${VENV_DIR:-}" && -d "${VENV_DIR:-}" ]]; then
    deactivate 2>/dev/null || true
    rm -rf "$VENV_DIR"
fi
echo

# --- Section 4: Informations complémentaires ---
echo "--- [4] Informations PCI détaillées (contrôleur MEI) ---"
if [[ -n "$MEI_PCI" ]]; then
    BDF=$(echo "$MEI_PCI" | cut -d' ' -f1)
    if [[ -d "/sys/bus/pci/devices/0000:$BDF" ]]; then
        for attr in vendor device class; do
            if [[ -f "/sys/bus/pci/devices/0000:$BDF/$attr" ]]; then
                echo "  $attr: $(cat /sys/bus/pci/devices/0000:$BDF/$attr)"
            fi
        done
    fi
fi
echo

echo "=============================================="
echo " Extraction terminée."
echo " Résultat sauvegardé dans: $OUTFILE"
echo "=============================================="
