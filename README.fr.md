# MOUSART
## Débogueur de port série complet

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **Français** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-PyQt6%20%7C%20Python-green)](https://www.riverbankcomputing.com/software/pyqt/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

**MOUSART** est un débogueur de port série complet construit avec Python/PyQt6, conçu pour le développement embarqué, le débogage matériel et la communication série. La version 3.0 est une réécriture complète en Python qui ajoute la réponse automatique, le support du protocole Modbus, les commandes rapides, l'enregistrement et l'export de données, le contrôle des pins, le support multi-encodage et des dizaines de fonctionnalités professionnelles.

---

## Aperçu des fonctionnalités

### 1. Gestion des connexions
- Actualisation automatique des ports disponibles (intervalle 2s)
- Port série virtuel, USB-vers-série, Bluetooth
- Débit : 300–921600 préréglages + personnalisé (1-9999999)
- Bits de données : 5, 6, 7, 8 / Bits d'arrêt : 1, 1.5, 2
- Parité : None, Even, Odd, Mark, Space
- Contrôle de flux : Aucun / Matériel (RTS/CTS) / Logiciel (XON/XOFF)
- Contrôle manuel DTR/RTS / Surveillance CTS/DSR/DCD/RI

### 2. Réception de données
- Mode texte (UTF-8 / GBK / GB18030 / Latin-1 / ASCII)
- Mode hexadécimal (HEX)
- Horodatage (précision milliseconde)
- Indicateur de direction (`<<` RX / `>>` TX / `!!` ERR)
- Pause d'affichage (réception en arrière-plan)
- Filtre par mot-clé (texte / regex)
- Limite de journal : 2000 entrées

### 3. Envoi de données
- Mode envoi Texte / HEX
- Contrôle de saut de ligne (CR / LF indépendant)
- Envoi temporisé (1ms–3600000ms, avec limite de compteur)
- Envoi de fichier
- Constructeur de trame Modbus RTU (CRC automatique)
- Barre de commandes rapides (ajout/édition/suppression, persistant)
- Séquence/file d'envoi (support boucle)

### 4. Réponse automatique
- Réponse automatique lors de la réception d'un mot-clé spécifique
- Délai de réponse configurable (ms)
- Activation/désactivation en un clic

### 5. Encodage et conversion
- Conversion Texte ↔ Hex
- Multi-encodage : UTF-8, GBK, GB18030, Latin-1, ASCII
- Sommes de contrôle : Sum8 / XOR8 / CRC16-Modbus / CRC32
- Constructeur et analyseur de trame Modbus RTU
- Conversion binaire / décimal / hexadécimal

### 6. Enregistrement et export
- Sauvegarde du journal en TXT / CSV
- Enregistrement automatique (fichier de 10MB)
- Compteur d'octets RX/TX en temps réel

### 7. Port série virtuel (Linux uniquement)
- Création de port virtuel via `socat`
- Connexion externe via `/tmp/mousart_vport`

### 8. Interface et configuration
- Thème sombre / clair
- Mise à l'échelle de police 0.8x–1.5x
- Gestion des profils (plusieurs configurations)

---

---

## Démarrage rapide

### Binaires précompilés

Télécharger depuis [GitHub Releases](https://github.com/kryntx/MOUSART/releases) :

| Plateforme | Fichier | Taille |
|------------|---------|--------|
| **Linux x86_64 (deb)** | `mouserial_3.0.0-1_amd64.deb` | ~82KB |
| **Windows x86_64** | `MOUSART-v3.0.0-windows-x86_64.exe` | ~23MB |

#### Installation Debian/Ubuntu (Recommandé)
```bash
# Télécharger et installer le paquet deb (les dépendances sont gérées automatiquement)
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb
sudo apt install ./mouserial_3.0.0-1_amd64.deb
```

### Compiler depuis les sources

```bash
# Ubuntu/Debian dépendances
sudo apt install python3-pyqt6 python3-serial socat

git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# Installer les dépendances Python
pip3 install PyQt6 pyserial

# Exécuter
python3 -m mousart
```

#### Construire l'EXE Windows

```bash
pip3 install pyinstaller
pyinstaller pyinstaller.spec --noconfirm
# Sortie : dist/MOUSART.exe
```

#### Construire le paquet Debian

```bash
sudo apt install dh-python python3-setuptools debhelper
dpkg-buildpackage -us -uc -b
```

---

## Utilisation

### Mode port série virtuel
1. Sélectionner le mode **"Virtual"** dans le panneau gauche
2. Cliquer sur **"Start"**
3. Le chemin du port `/tmp/mousart_vport` s'affiche
4. Connecter tout outil série à ce chemin

### Mode débogage série matériel
1. Sélectionner le mode **"Debug"**
2. Choisir un port et configurer les paramètres
3. Cliquer sur **"Open"** pour se connecter
4. Saisir dans la zone d'envoi et cliquer **"Envoyer"** ou `Ctrl+Enter`

### Commandes rapides
1. Cliquer sur **"+"** dans la barre de commandes rapides
2. Saisir le nom et les données
3. Clic gauche pour envoyer, clic droit pour éditer

### Réponse automatique
1. Section **"Réponse auto"** dans le panneau gauche
2. Activer le toggle, définir le mot-clé et les données de réponse

### Constructeur Modbus
1. Cliquer sur **"Modbus"** dans la barre d'outils
2. Définir l'adresse esclave, le code fonction, l'adresse de début, la quantité
3. Cliquer sur **"Construire"** pour générer la trame avec CRC

---

## Paramètres série

| Paramètre | Valeurs |
|-----------|---------|
| **Débit** | 300–921600 + personnalisé (1-9999999) |
| **Bits de données** | 5, 6, 7, 8 |
| **Bits d'arrêt** | 1, 1.5, 2 |
| **Parité** | None, Odd, Even, Mark, Space |
| **Contrôle de flux** | None, Hardware, Software |
| **Encodage réception** | UTF-8, GBK, GB18030, Latin-1, ASCII |

---

## Journal des modifications

### v3.0.0 (2026-05-29)
**Réécriture complète - Version Python/PyQt6**

- Réécriture complète en Python, migration de C++/Qt5/QML vers Python/PyQt6
- Structure de code plus simple, plus facile à maintenir et étendre
- Toutes les fonctionnalités v2.0.0 entièrement conservées
- Support multiplateforme optimisé (Windows EXE + Linux deb)
- Nouveau design d'icône d'application

### v2.0.0 (2026-05-29)
Contrôle des pins, réponse automatique, commandes rapides, multi-encodage, Modbus RTU, export de journal, statistiques RX/TX, filtrage de données, gestion de profils, outils de somme de contrôle, séquence d'envoi

### v1.0.0 (2026-05-27)
Première version

---

## FAQ

**Q: Impossible d'ouvrir le port ?** Problème de permissions. Utilisez `sudo python3 -m mousart` ou ajoutez l'utilisateur au groupe `dialout`.

**Q: Le port virtuel ne fonctionne pas ?** Installez `socat` : `sudo apt install socat`

---

## Licence

**Licence MIT** - voir [LICENSE](LICENSE).

**MOUSART** - Le débogage série plus simple et plus efficace !
