# MOUSART
## Vollwertiges seriellen Debugging-Tool

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)

**MOUSART** ist ein vollwertiges seriellen Debugging-Tool, das fur Embedded-Entwicklung, Hardware-Debugging und serielle Kommunikationsszenarien entwickelt wurde. Es unterstutzt zwei unabhangige Modi: Serielles Debugging und Virtueller serieller Port, und verfugt uber Dutzende professioneller Funktionen wie automatische Antwort, Modbus-Protokoll-Unterstutzung, Schnellbefehle, Datenaufzeichnung und -export, Pin-Steuerung und Multi-Encoding-Unterstutzung.

---

## Screenshots

### Serielles Debugging-Modus

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART Serielles Debugging-Interface">
  <br>
  <em>Serielles Debugging-Modus - Verbindung mit echter Hardware-Schnittstelle zum Senden und Empfangen</em>
</div>

### Virtueller serieller Port Modus

<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART Virtueller serieller Port Interface">
  <br>
  <em>Virtueller serieller Port Modus - Erstellung eines virtuellen seriellen Port-Paars fur externe Programme</em>
</div>

---

## Funktionen

### Serielles Debugging-Modus
- Automatische Aktualisierung der verfugbaren seriellen Port-Liste (2-Sekunden-Polling)
- Unterstutzung von USB-Seriell-Adaptern, Bluetooth-Seriell etc.
- Baudrate: 300 ~ 921600 Voreinstellungen + Benutzerdefinierte Werte (1-9999999)
- Datenbits: 5, 6, 7, 8 / Stoppbits: 1, 1.5, 2
- Paritat: None, Even, Odd, Mark, Space
- Flusskontrolle: Keine / Hardware (RTS/CTS) / Software (XON/XOFF)
- DTR/RTS manuelle Setzung
- CTS/DSR/DCD/RI Pin-Level Echtzeituberwachung
- Automatische Antwort (Schlusselwortabgleich + Verzogerungskonfiguration)

### Virtueller serieller Port Modus (nur Linux)
- Ein-Klick-Erstellung eines virtuellen seriellen Port-Paars basierend auf `socat`
- Externe Programme verbinden sich uber `/tmp/mousart_vport`
- Unabhangige Sende-/Empfangsbereiche und Statistiken

### Datensenden und -empfangen
- Text / HEX Sendemodus-Umschaltung
- Multi-Encoding-Unterstutzung: UTF-8, GBK, GB18030, Latin-1, ASCII
- Sendezeilenumbruch-Steuerung (CR / LF unabhangige Schalter)
- Zeitsender (1ms ~ 3600000ms)
- Dateisenden
- Modbus RTU Frame-Builder (automatische CRC)
- Schnellbefehlsleiste (Linksklick senden, Rechtsklick bearbeiten)
- Ctrl+Enter Tastenkombination Senden

### Datenanalyse
- Prufsummenberechnung: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Binar / Dezimal / Hexadezimal Umrechnung
- Text <-> Hex Echtzeitkonvertierung
- Schlusselwort / Regulärer Ausdruck Filter

### Datenaufzeichnung
- Ein-Klick-Protokollspeicherung als TXT / CSV
- Automatische Aufzeichnung (10MB/Datei automatische Aufteilung)
- Echtzeit RX/TX Byte-Zahler und Rate-Anzeige

### Benutzeroberflache
- Dunkles/Helles Dual-Theme
- 0.8x-1.5x Schriftskalierung
- Konfigurationsverwaltung (Profile)

---

## Installationsanleitung

### Linux (Debian/Ubuntu)

#### Methode 1: deb-Paket-Installation (empfohlen)

```bash
# 1. deb-Paket herunterladen
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb

# 2. Installieren (Abhängigkeiten werden automatisch installiert)
sudo apt install ./mouserial_3.0.0-1_amd64.deb

# 3. Ausführen
mousart
```

#### Methode 2: Aus dem Quellcode ausfuhren

```bash
# 1. Systemabhāngigkeiten installieren
sudo apt update
sudo apt install python3-pyqt5 python3-serial socat git

# 2. Projekt klonen
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. Ausfuhren
python3 -m mousart
```

#### Methode 3: Abhāngigkeiten mit pip installieren und ausfuhren

```bash
# 1. Systemabhāngigkeiten installieren
sudo apt install socat

# 2. Python-Abhāngigkeiten installieren
pip3 install PyQt5 pyserial

# 3. Klonen und ausfuhren
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### Methode 1: Aus dem Quellcode ausfuhren

```bash
# 1. Python 3.10+ installieren (von python.org herunterladen)

# 2. Abhāngigkeiten installieren
pip install PyQt5 pyserial

# 3. Projekt klonen und ausfuhren
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### Methode 2: EXE erstellen

```bash
# 1. Abhāngigkeiten installieren
pip install PyQt5 pyserial pyinstaller

# 2. Erstellen
pyinstaller pyinstaller.spec --noconfirm

# 3. Die generierte dist/MOUSART.exe ausfuhren
```

---

## Deinstallationsanleitung

### Linux deb-Paket-Deinstallation

```bash
# Methode 1: Mit apt deinstallieren
sudo apt remove mouserial

# Methode 2: Vollstāndige Deinstallation (einschlieߓlich Konfigurationsdateien)
sudo apt purge mouserial

# Benutzerkonfiguration bereinigen (optional)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Linux Quellcode-Installation deinstallieren

```bash
# Projektverzeichnis loschen
rm -rf /path/to/MOUSART

# Benutzerkonfiguration bereinigen (optional)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Windows-Deinstallation

```
# Projektverzeichnis loschen

# Benutzerkonfiguration bereinigen (optional)
# %USERPROFILE%\.mousart Verzeichnis loschen
# %USERPROFILE%\mousart_logs Verzeichnis loschen
```

---

## Benutzerhandbuch

### Serielles Debugging-Modus
1. Wahlen Sie im linken Panel den **"Seriellen Debugging"** Modus
2. Wahlen Sie den seriellen Port aus der Dropdown-Liste
3. Konfigurieren Sie die seriellen Port-Parameter (Baudrate, Datenbits, Stoppbits, Paritat, Flusskontrolle)
4. Klicken Sie auf **"Offnen"** um die Verbindung herzustellen
5. Geben Sie Daten im rechten Sendebereich ein und klicken Sie auf **"Senden"** oder drucken Sie `Ctrl+Enter`
6. Der Empfangsbereich zeigt die empfangenen Daten in Echtzeit an

### Virtueller serieller Port Modus (nur Linux)
1. Wahlen Sie im linken Panel den **"Simulations-Seriell-Port"** Modus
2. Klicken Sie auf **"Starten"** um das virtuelle seriellen Port-Paar zu erstellen
3. Die Oberflache zeigt den externen Port-Pfad `/tmp/mousart_vport` an
4. Verbinden Sie sich mit einem beliebigen seriellen Tool uber diesen Pfad
5. Geben Sie Daten im Sendebereich ein und senden Sie

### Schnellbefehle
1. Klicken Sie auf **"+"** in der Schnellbefehlsleiste am unteren Rand, um einen neuen Befehl hinzuzufugen
2. Geben Sie Name und Daten ein (Text und HEX werden unterstutzt)
3. Linksklick auf die Befehlsschaltflache zum sofortigen Senden
4. Rechtsklick auf die Befehlsschaltflache zum Bearbeiten oder Loschen

### Automatische Antwort (Serielles Debugging-Modus)
1. Finden Sie den **"Automatische Antwort"** Bereich im linken Panel
2. Aktivieren Sie den Schalter und konfigurieren Sie Schlusselwortabgleich und Antwortdaten
3. Optional konnen Sie die Antwortverzogerung einstellen (Millisekunden)

### Modbus-Frame-Erstellung
1. Klicken Sie in der Sendewerkzeugleiste auf die **"Modbus"** Schaltflache
2. Konfigurieren Sie Slave-Adresse, Funktionscode, Startadresse und Anzahl
3. Klicken Sie auf **"Erstellen"**, um automatisch ein Modbus RTU Frame mit CRC zu generieren

### Protokollaufzeichnung und -export
1. Klicken Sie in der Empfangswerkzeugleiste auf die **"Aufzeichnen"** Schaltflache, um die automatische Aufzeichnung zu starten
2. Alle gesendeten und empfangenen Daten werden automatisch in `~/mousart_logs/` gespeichert
3. Klicken Sie auf **"Speichern"**, um manuell als TXT oder CSV zu exportieren

### Pin-Steuerung (Serielles Debugging-Modus)
1. Nach dem Offnen des seriellen Ports wird im linken Panel die Pin-Steuerungsleiste angezeigt
2. Klicken Sie auf die DTR/RTS-Schaltflachen, um den Pinpegel umzuschalten
3. CTS/DSR/DCD/RI Statusanzeigen werden in Echtzeit angezeigt

---

## Haufig gestellte Fragen

**Q: Serieller Port kann nicht geoffnet werden?**
A: Normalerweise ein Berechtigungsproblem. Fugen Sie den Benutzer zur `dialout` Gruppe hinzu:
```bash
sudo usermod -aG dialout $USER
# Abmelden und erneut anmelden, damit es wirksam wird
```

**Q: Virtueller serieller Port funktioniert nicht?**
A: Stellen Sie sicher, dass `socat` installiert ist:
```bash
sudo apt install socat
```

**Q: Chinesische Zeichen werden falsch dargestellt?**
A: Wahlen Sie im linken Panel die richtige Empfangskodierung (z.B. GBK).

**Q: Wie sende ich einen Modbus-Befehl?**
A: Klicken Sie auf die **"Modbus"** Schaltflache, fullen Sie die Parameter aus und klicken Sie auf **"Erstellen"**. Die Framedaten werden automatisch in den Sendebereich eingefugt.

**Q: Wo werden die automatisch aufgezeichneten Dateien gespeichert?**
A: Standardmaߥig in `~/mousart_logs/`, das Dateinamensformat ist `mousart_rec_YYYYMMDD_HHmmss.log`.

---

## Lizenz

Dieses Projekt verwendet die **MIT-Lizenz** - siehe [LICENSE](LICENSE) fur Details.

**MOUSART** - Serielles Debugging einfacher und effizienter machen!
