# MOUSART
## Vollständiger serieller Port-Debugger

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **Deutsch** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v2.0.0)

**MOUSART** ist ein vollständiger serieller Port-Debugger, der mit Qt5/QML erstellt wurde und für Embedded-Entwicklung, Hardware-Debugging und serielle Kommunikation konzipiert ist. Version 2.0 fügt Auto-Reply, Modbus-Protokollunterstützung, Schnellbefehle, Datenaufzeichnung & Export, Pin-Steuerung, Multi-Encoding-Unterstützung und dutzende professionelle Funktionen hinzu.

---

## Funktionsübersicht

### 1. Verbindungsverwaltung
- Automatische Aktualisierung der verfügbaren Ports (2s Intervall)
- Virtueller serieller Port, USB-zu-Seriell, Bluetooth-Unterstützung
- Baudrate: 300–921600 Voreinstellungen + Benutzerdefiniert (1-9999999)
- Datenbits: 5, 6, 7, 8 / Stoppbits: 1, 1.5, 2
- Parität: None, Even, Odd, Mark, Space
- Flusssteuerung: Keine / Hardware (RTS/CTS) / Software (XON/XOFF)
- DTR/RTS manuelle Steuerung / CTS/DSR/DCD/RI Pin-Überwachung

### 2. Datenempfang
- Textmodus (UTF-8 / GBK / GB18030 / Latin-1 / ASCII)
- Hexadezimal (HEX) Anzeigemodus
- Zeitstempel (Millisekundengenauigkeit)
- Richtungsanzeige (`<<` RX / `>>` TX / `!!` ERR)
- Anzeige pausieren (Empfang im Hintergrund)
- Keyword-Filter (Text / Regex)
- Log-Limit: 2000 Einträge

### 3. Datensendung
- Text / HEX Sendemodus
- Zeilenumbruch-Steuerung (CR / LF unabhängig)
- Zeitgesteuertes Senden (1ms–3600000ms, mit Zähllimit)
- Dateisendung
- Modbus RTU Frame-Builder (CRC automatisch)
- Schnellbefehlsleiste (Hinzufügen/Bearbeiten/Löschen, persistent)
- Sendesequenz/Queue (Schleifenunterstützung)

### 4. Auto-Reply
- Automatische Antwort bei bestimmtem Keyword
- Konfigurierbare Antwortverzögerung (ms)
- Ein-Klick Aktivierung/Deaktivierung

### 5. Encoding & Konvertierung
- Text ↔ Hex Konvertierung
- Multi-Encoding: UTF-8, GBK, GB18030, Latin-1, ASCII
- Prüfsummen: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Modbus RTU Frame-Builder & Parser
- Binär / Dezimal / Hex Konvertierung

### 6. Datenaufzeichnung & Export
- Log als TXT / CSV speichern
- Automatische Aufzeichnung (10MB Dateigröße)
- Echtzeit RX/TX Byte-Zähler

### 7. Virtueller serieller Port (nur Linux)
- Ein-Klick virtueller Port via `socat`
- Externe Programme verbinden über `/tmp/mousart_vport`

### 8. UI & Konfiguration
- Dunkles / Helles Thema
- 0.8x–1.5x Schriftskalierung
- Profilverwaltung (mehrere Konfigurationen)

---

## Screenshots

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART Debug-Oberfläche">
  <br>
  <em>MOUSART Seriell-Debug-Oberfläche (Helles Thema)</em>
</div>

---

## Schnellstart

### Vorgefertigte Binärdateien

Download bei [GitHub Releases](https://github.com/kryntx/MOUSART/releases):

| Plattform | Datei | Größe |
|-----------|-------|-------|
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | ~105KB |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | ~23MB |

### Aus dem Quellcode bauen

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

## Verwendung

### Virtueller serieller Port
1. **"Virtual"** Modus im linken Panel wählen
2. **"Start"** klicken
3. Externer Port-Pfad `/tmp/mousart_vport` wird angezeigt
4. Serielle Tools verbinden sich mit diesem Pfad

### Hardware-Seriell-Debug
1. **"Debug"** Modus wählen
2. Port auswählen und Parameter konfigurieren
3. **"Open"** zum Verbinden
4. Im Sendebereich eingeben und **"Senden"** oder `Ctrl+Enter`

### Schnellbefehle
1. **"+"** in der Schnellbefehlsleiste klicken
2. Name und Daten eingeben
3. Linksklick zum Senden, Rechtsklick zum Bearbeiten

### Auto-Reply
1. **"Auto Reply"** im linken Panel
2. Toggle aktivieren, Keyword und Antwortdaten setzen

### Modbus Frame-Builder
1. **"Modbus"** in der Sendewerkzeugleiste klicken
2. Slave-Adresse, Funktionscode, Startadresse, Menge setzen
3. **"Erstellen"** für automatische CRC-Generierung

---

## Serielle Parameter

| Parameter | Werte |
|-----------|-------|
| **Baudrate** | 300–921600 + Benutzerdefiniert (1-9999999) |
| **Datenbits** | 5, 6, 7, 8 |
| **Stoppbits** | 1, 1.5, 2 |
| **Parität** | None, Odd, Even, Mark, Space |
| **Flusssteuerung** | None, Hardware, Software |
| **Empfangs-Encoding** | UTF-8, GBK, GB18030, Latin-1, ASCII |

---

## Änderungsprotokoll

### v2.0.0 (2026-05-29)
Pin-Steuerung, Auto-Reply, Schnellbefehle, Multi-Encoding, Modbus RTU, Log-Export, RX/TX-Statistiken, Datenfilterung, Profilverwaltung, Prüfsummen-Tools, Sendesequenz

### v1.0.0 (2026-05-27)
Erstveröffentlichung

---

## FAQ

**Q: Port kann nicht geöffnet werden?** Meist ein Berechtigungsproblem. `sudo` verwenden oder Benutzer zur `dialout`-Gruppe hinzufügen.

**Q: Virtueller Port funktioniert nicht?** `socat` installieren: `sudo apt install socat`

---

## Lizenz

**MIT-Lizenz** - siehe [LICENSE](LICENSE).

**MOUSART** - Serielles Debugging einfacher und effizienter!
