# MOUSART
## Débogueur de port série complet

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **Français** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v2.0.0)

**MOUSART** est un débogueur de port série complet construit avec Qt5/QML, conçu pour le développement embarqué, le débogage matériel et la communication série. La version 2.0 ajoute la réponse automatique, le support du protocole Modbus, les commandes rapides, l'enregistrement et l'export de données, le contrôle des pins, le support multi-encodage et des dizaines de fonctionnalités professionnelles.

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

## Capture d'écran

<div align="center">
  <img src="img/d1.png" width="800" alt="Interface de débogage MOUSART">
  <br>
  <em>Interface de débogage série MOUSART (thème clair)</em>
</div>

---

## Démarrage rapide

### Binaires précompilés

Télécharger depuis [GitHub Releases](https://github.com/kryntx/MOUSART/releases) :

| Plateforme | Fichier | Taille |
|------------|---------|--------|
| **Linux x86_64 (deb)** | `mouserial_2.0.0-1_amd64.deb` | ~82KB |
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | ~105KB |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | ~23MB |

#### Installation Debian/Ubuntu (Recommandé)
```bash
# Télécharger et installer le paquet deb (les dépendances sont gérées automatiquement)
wget https://github.com/kryntx/MOUSART/releases/download/v2.0.0/mouserial_2.0.0-1_amd64.deb
sudo apt install ./mouserial_2.0.0-1_amd64.deb
```

> **Dépendances d'exécution Linux** : Le binaire précompilé nécessite les bibliothèques d'exécution Qt5 QML :
> ```bash
> sudo apt install qtdeclarative5-dev libqt5serialport5-dev \
>   qml-module-qtquick2 qml-module-qtquick-controls2 \
>   qml-module-qtquick-layouts qml-module-qtquick-window2 \
>   qml-module-qtquick-templates2 qml-module-qtqml-models2
> ```

### Compiler depuis les sources

```bash
# Ubuntu/Debian
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat

git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/MOUSART
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

### v2.0.0 (2026-05-29)
Contrôle des pins, réponse automatique, commandes rapides, multi-encodage, Modbus RTU, export de journal, statistiques RX/TX, filtrage de données, gestion de profils, outils de somme de contrôle, séquence d'envoi

### v1.0.0 (2026-05-27)
Première version

---

## FAQ

**Q: Impossible d'ouvrir le port ?** Problème de permissions. Utilisez `sudo` ou ajoutez l'utilisateur au groupe `dialout`.

**Q: Le port virtuel ne fonctionne pas ?** Installez `socat` : `sudo apt install socat`

---

## Licence

**Licence MIT** - voir [LICENSE](LICENSE).

**MOUSART** - Le débogage série plus simple et plus efficace !
