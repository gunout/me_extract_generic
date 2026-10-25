# 🛡️ ME Extract Generic

![GitHub last commit](https://img.shields.io/github/last-commit/gunout/me_extract_generic?style=for-the-badge&logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/gunout/me_extract_generic?style=for-the-badge&logo=github)
![GitHub stars](https://img.shields.io/github/stars/gunout/me_extract_generic?style=for-the-badge&logo=github)
![GitHub forks](https://img.shields.io/github/forks/gunout/me_extract_generic?style=for-the-badge&logo=github)
![GitHub issues](https://img.shields.io/github/issues/gunout/me_extract_generic?style=for-the-badge&logo=github)

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Intel](https://img.shields.io/badge/Intel-0071C5?style=for-the-badge&logo=intel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Textual](https://img.shields.io/badge/Textual-000000?style=for-the-badge&logo=textual&logoColor=white)

> **Extraction et exploration génériques de l'Intel Management Engine (ME) sur Linux.**
> Script CLI + interface TUI interactive pour auditer, diagnostiquer et dumper les données exposées par l'IME, sur n'importe quelle machine Intel.

---

## 📖 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Données extraites](#-données-extraites)
- [Décodage des registres HFSTS](#-décodage-des-registres-hfsts)
- [Limites connues](#-limites-connues)
- [Avertissement](#️-avertissement)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🔍 Présentation

**ME Extract Generic** est une boîte à outils open source conçue pour **extraire, décoder et archiver les informations de l'Intel Management Engine** (IME) sur les systèmes Linux.

L'IME est un sous-système autonome embarqué dans les chipsets Intel depuis 2008, fonctionnant sur un MINIX modifié à un niveau de privilège extrême (Ring -3). Cet outil permet d'en **auditer l'état**, d'en **extraire les données lisibles** et de **documenter sa configuration** — sans recourir à des outils propriétaires.

Le dépôt contient deux composants complémentaires :

| Fichier | Description |
| :--- | :--- |
| `me_extract_generic.sh` | Script Bash **universel** pour toute machine Intel sous Linux |
| `me_tui.py` | Interface **TUI interactive** (Textual) pour explorer le ME en temps réel |

---

## ✨ Fonctionnalités

### 🔧 Script CLI (`me_extract_generic.sh`)

- ✅ **Détection automatique** du contrôleur MEI via `lspci`
- ✅ **Lecture sysfs** : `dev_state`, `fw_ver`, `fw_status`, `hbm_ver`
- ✅ **Décodage des registres HFSTS** (Working State, Operation Mode, Error Code…)
- ✅ **Scan PCI** du contrôleur MEI (Vendor, Device, Class)
- ✅ **Installation isolée de CHIPSEC** dans un venv temporaire
- ✅ **Tentative de dump SPI** (si le firmware le permet)
- ✅ **Sortie horodatée** dans un fichier `me_dump_<hostname>_<date>.txt`

### 🖥️ Interface TUI (`me_tui.py`)

- ✅ **Tableau de bord** temps réel (état, version, debugfs)
- ✅ **Connexion MKHI** via `/dev/mei0` et le GUID `8e6a6715-…`
- ✅ **Commandes GEN** : `GET_FW_VERSION`, `GET_PLATFORM_TYPE`, `GET_FW_CAPS`, `GET_SKU`
- ✅ **Commandes FWUPDATE et CRASH** (groupes `0x04` et `0x03`)
- ✅ **Liste des clients ME** via debugfs
- ✅ **Export complet** vers `me_dump_*.txt`
- ✅ **Log persistant** dans `/tmp/me_tui.log`
- ✅ **Raccourcis clavier** : `s`, `m`, `c`, `e`, `f`, `Ctrl+S`, `q`

---

## 📋 Prérequis

| Composant | Version minimale | Notes |
| :--- | :--- | :--- |
| **Linux** | Noyau ≥ 4.18 | Pour `/sys/class/mei/mei0/fw_ver` |
| **Python** | 3.9+ | Pour la TUI |
| **Textual** | 8.x | `pip install textual` |
| **Module noyau** | `mei_me` | `sudo modprobe mei_me` |
| **Droits** | `root` | Accès à `/dev/mei0` |

### Vérification rapide

    # Vérifier la présence du contrôleur MEI
    lspci -nn | grep -i "communication controller"

    # Vérifier que le module est chargé
    lsmod | grep mei_me

    # Vérifier l'accès au device
    ls -l /dev/mei0

---

## 🚀 Installation

### 1. Cloner le dépôt

    git clone https://github.com/gunout/me_extract_generic.git
    cd me_extract_generic

### 2. Rendre les scripts exécutables

    chmod +x me_extract_generic.sh

### 3. Créer un environnement virtuel pour la TUI

    python3 -m venv venv
    source venv/bin/activate
    pip install textual

### 4. (Optionnel) Monter debugfs

    sudo mount -t debugfs none /sys/kernel/debug

> 💡 Sur Ubuntu, `debugfs` est généralement déjà monté. Vérifiez avec `mount | grep debugfs`.

---

## 🎮 Utilisation

### 🔧 Script CLI : `me_extract_generic.sh`

    sudo ./me_extract_generic.sh

**Sortie** : un fichier `me_dump_<hostname>_<date>.txt` contenant :

- Détection du contrôleur MEI
- Données sysfs décodées
- Informations PCI
- Tentative de dump SPI via CHIPSEC (si installable)
- Informations complémentaires

### 🖥️ Interface TUI : `me_tui.py`

    sudo ./venv/bin/python me_tui.py

**Raccourcis clavier** :

| Touche | Action |
| :---: | :--- |
| `s` | Version firmware (sysfs) |
| `m` | Connexion et commandes MKHI |
| `c` | Liste des clients ME (debugfs) |
| `f` | Exploration FWUPDATE et CRASH |
| `e` | **Extraction complète vers `me_dump_*.txt`** |
| `Ctrl+S` | Sauvegarde du log dans `/tmp/me_tui.log` |
| `q` | Quitter |

**Navigation** : `Tab` pour passer d'un bouton à l'autre, `Entrée` pour activer. La souris est également supportée.

---

## 📊 Données extraites

| Source | Donnée | Chemin / Méthode |
| :--- | :--- | :--- |
| **sysfs** | Version firmware | `/sys/class/mei/mei0/fw_ver` |
| **sysfs** | État du device | `/sys/class/mei/mei0/dev_state` |
| **sysfs** | Registres HFSTS | `/sys/class/mei/mei0/fw_status` |
| **sysfs** | Version HBM (firmware) | `/sys/class/mei/mei0/hbm_ver` |
| **sysfs** | Version HBM (driver) | `/sys/class/mei/mei0/hbm_ver_drv` |
| **PCI** | Vendor/Device/Class | `/sys/bus/pci/devices/*/` |
| **MKHI** | Version firmware | Groupe `0xFF`, cmd `0x02` |
| **MKHI** | Type de plateforme | Groupe `0xFF`, cmd `0x03` |
| **MKHI** | Capacités firmware | Groupe `0xFF`, cmd `0x04` |
| **MKHI** | SKU commercial | Groupe `0xFF`, cmd `0x08` |
| **MKHI** | Version FWUPDATE | Groupe `0x04`, cmd `0x01` |
| **MKHI** | Info crash dump | Groupe `0x03`, cmd `0x01` |

---

## 🧩 Décodage des registres HFSTS

Pour les plateformes **ME 11 / Skylake**, les registres `fw_status` sont décodés comme suit :

### HFSTS1 (`0x90000245` → exemple)

| Champ | Bits | Valeur | Signification |
| :--- | :---: | :---: | :--- |
| **Working State** | 3:0 | `5` | Normal |
| **Operation State** | 8:6 | `1` | M0 with UMA |
| **Operation Mode** | 19:16 | `0` | Normal |
| **Error Code** | 15:12 | `0` | No Error |
| **Update In Progress** | 11 | `1` | YES |

### HFSTS2 (`0x82210506` → exemple)

| Champ | Bits | Valeur | Signification |
| :--- | :---: | :---: | :--- |
| **Progress Code** | 31:28 | `8` | UMA/kernel interne |
| **PM Event** | 27:24 | `2` | — |

> 💡 Les définitions exactes varient selon la génération du ME. Le décodeur implémenté cible ME 11 (Skylake/Kaby Lake) et s'appuie sur les définitions de coreboot.

---

## ⚠️ Limites connues

Cet outil ne peut **pas** extraire ce que le firmware ME refuse d'exposer :

- ❌ **Commandes avancées** (`GET_FW_CAPS`, `GET_SKU`, `FWCAPS`) sur les plateformes **consumer** (non-vPro)
- ❌ **Contenu du firmware ME** (code MINIX, modules internes)
- ❌ **Mémoire interne** du ME
- ❌ **Dump SPI complet** si Secure Boot ou les protections firmware le bloquent

> 💡 Pour un dump SPI complet, utilisez `flashrom` ou `CHIPSEC` (inclus dans le script CLI), puis analysez le fichier avec `ME Analyzer`.

---

## ⚠️ Avertissement

> **Cet outil est destiné à un usage forensique, éducatif ou de test.**
>
> - L'accès à `/dev/mei0` nécessite les privilèges **root**.
> - CHIPSEC charge un module noyau et peut provoquer des **instabilités système**.
> - Ne l'utilisez **pas** sur une machine de production.
> - L'auteur décline toute responsabilité en cas de dommage matériel ou logiciel.

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. **Fork** le dépôt
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`)
3. **Commit** vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. **Push** (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une **Pull Request**

### Idées d'amélioration

- 🌐 Support d'autres générations ME (ME 12, 13, 14…)
- 📦 Export JSON structuré
- 🧪 Tests automatisés sur différentes plateformes
- 📚 Documentation des codes d'erreur MKHI
- 🖥️ Support Windows (via `MEI` driver)

---

## 📄 Licence

Distribué sous licence **MIT**. Voir `LICENSE` pour plus d'informations.

---

## 🙏 Remerciements

- [coreboot](https://www.coreboot.org/) — Définitions des registres HFSTS
- [CHIPSEC](https://github.com/chipsec/chipsec) — Dump SPI bas niveau
- [ME Analyzer](https://github.com/platomav/MEAnalyzer) — Analyse de firmware
- [Textual](https://textual.textualize.io/) — Framework TUI
- [Intel ME Research](https://github.com/Jatinkapilaq1/intel-me-research) — Inspiration

---

<div align="center">

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile ! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/gunout/me_extract_generic?style=social)](https://github.com/gunout/me_extract_generic)

</div>
