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
  - [Script CLI](#-script-cli--me_extract_genericsh)
  - [Interface TUI](#-interface-tui--me_tuipy)
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

```bash
# Vérifier la présence du contrôleur MEI
lspci -nn | grep -i "communication controller"

# Vérifier que le module est chargé
lsmod | grep mei_me

# Vérifier l'accès au device
ls -l /dev/mei0
```

