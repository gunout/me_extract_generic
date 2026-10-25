<!-- ============================================================ -->
<!--  GUNOUT — ME EXTRACT GENERIC — NEON ROSE README              -->
<!-- ============================================================ -->

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h1 align="center">
  <samp>🛡️ ME Extract Generic</samp>
</h1>

<p align="center">
  <samp>
    <span style="color:#FF2D95;">Extraction & exploration génériques de l'Intel Management Engine sur Linux</span><br>
    <span style="color:#FF69B4;">Script CLI + interface TUI interactive</span>
  </samp>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&weight=700&size=22&pause=800&color=FF2D95&background=0D001A00&center=true&vCenter=true&random=true&width=800&lines=%E2%96%B6+Initializing+IME+protocol...;%E2%96%B6+Reading+sysfs+registers...;%E2%96%B6+Decoding+HFSTS+status...;%E2%96%B6+Connecting+MKHI+client...;%E2%96%B6+System+online.+Welcome." alt="Typing SVG" />
</p>

<!-- 👇 INSERTION DU SCREENSHOT PNG 👇 -->
<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/me_extract_generic/main/assets/images/preview.png" alt="ME Explorer TUI Preview" width="800" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/Intel-0071C5?style=for-the-badge&logo=intel&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" />
  <img src="https://img.shields.io/badge/Textual-000000?style=for-the-badge&logo=textual&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/gunout/me_extract_generic?style=for-the-badge&logo=github&color=FF2D95" />
  <img src="https://img.shields.io/github/repo-size/gunout/me_extract_generic?style=for-the-badge&logo=github&color=FF69B4" />
  <img src="https://img.shields.io/github/stars/gunout/me_extract_generic?style=for-the-badge&logo=github&color=FFB6D9" />
  <img src="https://img.shields.io/github/forks/gunout/me_extract_generic?style=for-the-badge&logo=github&color=FF2D95" />
  <img src="https://img.shields.io/github/issues/gunout/me_extract_generic?style=for-the-badge&logo=github&color=FF69B4" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">⚡ <code>about</code></h2>

<p align="center">
  <samp>
    <span style="color:#FF2D95;">🛡️ IME Audit</span> — Extraction des données exposées par l'Intel Management Engine<br>
    <span style="color:#FF69B4;">📊 HFSTS Decoding</span> — Décodage des registres de statut firmware<br>
    <span style="color:#FFB6D9;">🔌 MKHI Protocol</span> — Communication via /dev/mei0 et GUID client<br>
    <span style="color:#FF2D95;">🖥️ Textual TUI</span> — Interface terminal interactive et colorée<br>
    <span style="color:#FF69B4;">📦 Export</span> — Dumps horodatés au format <code>.txt</code><br>
    <span style="color:#FFB6D9;">🔭 Scope</span> — Forensique, éducatif, tests matériels
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🛠️ <code>tech_stack</code></h2>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/icons/PythonIcon.svg" width="60" height="60" alt="Python" title="Python"/>
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/icons/BackBoxIcon.svg" width="60" height="60" alt="Linux" title="Linux"/>
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/icons/DockerIcon.svg" width="60" height="60" alt="Bash" title="Bash"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🚀 <code>features</code></h2>

<h3 align="center">🔧 Script CLI — <code>me_extract_generic.sh</code></h3>
<p align="center">
  <samp>
    ✅ Détection automatique du contrôleur MEI via <code>lspci</code><br>
    ✅ Lecture sysfs : <code>dev_state</code>, <code>fw_ver</code>, <code>fw_status</code>, <code>hbm_ver</code><br>
    ✅ Décodage des registres HFSTS<br>
    ✅ Scan PCI du contrôleur MEI<br>
    ✅ Installation isolée de CHIPSEC dans un venv temporaire<br>
    ✅ Tentative de dump SPI (si firmware le permet)<br>
    ✅ Sortie horodatée dans <code>me_dump_&lt;hostname&gt;_&lt;date&gt;.txt</code>
  </samp>
</p>

<h3 align="center">🖥️ Interface TUI — <code>me_tui.py</code></h3>
<p align="center">
  <samp>
    ✅ Tableau de bord temps réel (état, version, debugfs)<br>
    ✅ Connexion MKHI via <code>/dev/mei0</code> et GUID <code>8e6a6715-…</code><br>
    ✅ Commandes GEN : <code>GET_FW_VERSION</code>, <code>GET_PLATFORM_TYPE</code>, <code>GET_FW_CAPS</code>, <code>GET_SKU</code><br>
    ✅ Commandes FWUPDATE et CRASH<br>
    ✅ Liste des clients ME via debugfs<br>
    ✅ Export complet vers <code>me_dump_*.txt</code><br>
    ✅ Log persistant dans <code>/tmp/me_tui.log</code><br>
    ✅ Raccourcis clavier : <code>s</code>, <code>m</code>, <code>c</code>, <code>e</code>, <code>f</code>, <code>Ctrl+S</code>, <code>q</code>
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">📋 <code>prerequisites</code></h2>

<p align="center">
  <samp>
    <span style="color:#FF2D95;">Linux</span> — Noyau ≥ 4.18 (pour <code>/sys/class/mei/mei0/fw_ver</code>)<br>
    <span style="color:#FF69B4;">Python</span> — 3.9+ (pour la TUI)<br>
    <span style="color:#FFB6D9;">Textual</span> — 8.x (<code>pip install textual</code>)<br>
    <span style="color:#FF2D95;">Module noyau</span> — <code>mei_me</code> (<code>sudo modprobe mei_me</code>)<br>
    <span style="color:#FF69B4;">Droits</span> — <code>root</code> (accès à <code>/dev/mei0</code>)
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🚀 <code>installation</code></h2>

<p align="center">
  <samp>1. Cloner le dépôt</samp>
</p>

    git clone https://github.com/gunout/me_extract_generic.git
    cd me_extract_generic

<p align="center">
  <samp>2. Rendre les scripts exécutables</samp>
</p>

    chmod +x me_extract_generic.sh

<p align="center">
  <samp>3. Créer un environnement virtuel pour la TUI</samp>
</p>

    python3 -m venv venv
    source venv/bin/activate
    pip install textual

<p align="center">
  <samp>4. (Optionnel) Monter debugfs</samp>
</p>

    sudo mount -t debugfs none /sys/kernel/debug

<p align="center">
  <samp>💡 Sur Ubuntu, <code>debugfs</code> est généralement déjà monté. Vérifiez avec <code>mount | grep debugfs</code>.</samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🎮 <code>usage</code></h2>

<h3 align="center">🔧 Script CLI</h3>

    sudo ./me_extract_generic.sh

<p align="center">
  <samp>Sortie : un fichier <code>me_dump_&lt;hostname&gt;_&lt;date&gt;.txt</code> contenant :</samp>
</p>

<p align="center">
  <samp>
    • Détection du contrôleur MEI<br>
    • Données sysfs décodées<br>
    • Informations PCI<br>
    • Tentative de dump SPI via CHIPSEC<br>
    • Informations complémentaires
  </samp>
</p>

<h3 align="center">🖥️ Interface TUI</h3>

    sudo ./venv/bin/python me_tui.py

<p align="center">
  <samp>Raccourcis clavier :</samp>
</p>

<p align="center">
  <samp>
    <code>s</code> — Version firmware (sysfs)<br>
    <code>m</code> — Connexion et commandes MKHI<br>
    <code>c</code> — Liste des clients ME (debugfs)<br>
    <code>f</code> — Exploration FWUPDATE et CRASH<br>
    <code>e</code> — Extraction complète vers <code>me_dump_*.txt</code><br>
    <code>Ctrl+S</code> — Sauvegarde du log dans <code>/tmp/me_tui.log</code><br>
    <code>q</code> — Quitter
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">📊 <code>extracted_data</code></h2>

<p align="center">
  <samp>
    <span style="color:#FF2D95;">sysfs</span> — Version firmware, état, HFSTS, HBM<br>
    <span style="color:#FF69B4;">PCI</span> — Vendor / Device / Class du contrôleur MEI<br>
    <span style="color:#FFB6D9;">MKHI</span> — Version, plateforme, capacités, SKU, FWUPDATE, CRASH
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🧩 <code>hfsts_decoding</code></h2>

<p align="center">
  <samp>
    <span style="color:#FF2D95;">HFSTS1</span> — Working State, Operation State, Operation Mode, Error Code, Update In Progress<br>
    <span style="color:#FF69B4;">HFSTS2</span> — Progress Code, PM Event<br>
    <span style="color:#FFB6D9;">HFSTS3-6</span> — Recovery mode, update disabled, crash dump, operation mode
  </samp>
</p>

<p align="center">
  <samp>💡 Les définitions exactes varient selon la génération du ME. Le décodeur cible ME 11 (Skylake/Kaby Lake) et s'appuie sur coreboot.</samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">⚠️ <code>known_limitations</code></h2>

<p align="center">
  <samp>
    ❌ Commandes avancées sur plateformes consumer (non-vPro)<br>
    ❌ Contenu du firmware ME (code MINIX, modules internes)<br>
    ❌ Mémoire interne du ME<br>
    ❌ Dump SPI complet si Secure Boot ou protections firmware le bloquent
  </samp>
</p>

<p align="center">
  <samp>💡 Pour un dump SPI complet, utilisez <code>flashrom</code> ou <code>CHIPSEC</code>, puis analysez avec <code>ME Analyzer</code>.</samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">⚠️ <code>warning</code></h2>

<p align="center">
  <samp>
    <span style="color:#FF2D95;">Cet outil est destiné à un usage forensique, éducatif ou de test.</span><br>
    • L'accès à <code>/dev/mei0</code> nécessite les privilèges <code>root</code>.<br>
    • CHIPSEC charge un module noyau et peut provoquer des instabilités système.<br>
    • Ne l'utilisez pas sur une machine de production.<br>
    • L'auteur décline toute responsabilité en cas de dommage matériel ou logiciel.
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🤝 <code>contribution</code></h2>

<p align="center">
  <samp>Les contributions sont les bienvenues !</samp>
</p>

<p align="center">
  <samp>
    1. <b>Fork</b> le dépôt<br>
    2. Créez une branche (<code>git checkout -b feature/ma-fonctionnalite</code>)<br>
    3. <b>Commit</b> vos changements (<code>git commit -m 'Ajout de ma fonctionnalité'</code>)<br>
    4. <b>Push</b> (<code>git push origin feature/ma-fonctionnalite</code>)<br>
    5. Ouvrez une <b>Pull Request</b>
  </samp>
</p>

<h3 align="center">💡 Idées d'amélioration</h3>

<p align="center">
  <samp>
    🌐 Support d'autres générations ME (ME 12, 13, 14…)<br>
    📦 Export JSON structuré<br>
    🧪 Tests automatisés sur différentes plateformes<br>
    📚 Documentation des codes d'erreur MKHI<br>
    🖥️ Support Windows (via driver MEI)
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">📄 <code>license</code></h2>

<p align="center">
  <samp>Distribué sous licence <b>MIT</b>. Voir <code>LICENSE</code> pour plus d'informations.</samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<h2 align="center">🙏 <code>credits</code></h2>

<p align="center">
  <samp>
    <a href="https://www.coreboot.org/">coreboot</a> — Définitions des registres HFSTS<br>
    <a href="https://github.com/chipsec/chipsec">CHIPSEC</a> — Dump SPI bas niveau<br>
    <a href="https://github.com/platomav/MEAnalyzer">ME Analyzer</a> — Analyse de firmware<br>
    <a href="https://textual.textualize.io/">Textual</a> — Framework TUI<br>
    <a href="https://github.com/Jatinkapilaq1/intel-me-research">Intel ME Research</a> — Inspiration
  </samp>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>

<div align="center">
  <h3>💖 Support my work</h3>

  <a href="https://ko-fi.com/gunout">
    <img height='50' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' alt='Support me on Ko-fi' />
  </a>
  &nbsp;&nbsp;
  <a href="https://www.buymeacoffee.com/gunout">
    <img height='50' src='https://cdn.buymeacoffee.com/buttons/v2/default-blue.png' alt='Buy Me A Coffee' />
  </a>

  <br/><br/>

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/footer_neon.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/footer_neon.svg">
    <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/footer_neon.svg" alt="Footer" width="100%" />
  </picture>
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/gunout/gunout/main/assets/images/divider_neon.svg" alt="Divider" />
</p>
