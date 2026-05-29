# MOUSART
## Full-Featured Serial Port Debugger

<div align="center">

**[简体中文](README.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)

**MOUSART** is a full-featured serial port debugging tool designed for embedded development, hardware debugging, and serial communication. It supports two independent modes: Serial Debug and Virtual Serial Port, with features including auto-reply, Modbus protocol support, quick commands, data recording & export, pin control, and multi-encoding support.

---

## Screenshots

### Serial Debug Mode

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART Serial Debug Interface">
  <br>
  <em>Serial Debug Mode - Connect to real hardware serial ports</em>
</div>

### Virtual Serial Port Mode

<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART Virtual Serial Port Interface">
  <br>
  <em>Virtual Serial Port Mode - Create virtual port pairs for external programs</em>
</div>

---

## Features

### Serial Debug Mode
- Auto-refresh available port list (2s polling)
- USB-to-serial, Bluetooth serial support
- Baud rate: 300 ~ 921600 presets + custom (1-9999999)
- Data bits: 5, 6, 7, 8 / Stop bits: 1, 1.5, 2
- Parity: None, Even, Odd, Mark, Space
- Flow control: None / Hardware (RTS/CTS) / Software (XON/XOFF)
- DTR/RTS manual control
- CTS/DSR/DCD/RI pin state monitoring
- Auto-reply (keyword match + delay config)

### Virtual Serial Port Mode (Linux only)
- One-click virtual port pair creation via `socat`
- External programs connect via `/tmp/mousart_vport`
- Independent send/receive area and statistics

### Data Send/Receive
- Text / HEX send mode toggle
- Multi-encoding: UTF-8, GBK, GB18030, Latin-1, ASCII
- Newline control (CR / LF independent toggle)
- Timed auto-send (1ms ~ 3600000ms)
- File send
- Modbus RTU frame builder (auto CRC)
- Quick command bar (left-click send, right-click edit)
- Ctrl+Enter shortcut

### Data Analysis
- Checksum: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Binary / Decimal / Hex conversion
- Text <-> Hex conversion
- Keyword / Regex filtering

### Data Recording
- One-click save log to TXT / CSV
- Auto-recording (10MB/file auto-split)
- Real-time RX/TX byte counter and rate display

### UI
- Dark/Light theme
- 0.8x-1.5x font scaling
- Profile management

---

## Installation

### Linux (Debian/Ubuntu)

#### Method 1: deb package (Recommended)

```bash
# 1. Download deb package
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb

# 2. Install (dependencies installed automatically)
sudo apt install ./mouserial_3.0.0-1_amd64.deb

# 3. Run
mousart
```

#### Method 2: Run from source

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install python3-pyqt5 python3-serial socat git

# 2. Clone project
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. Run
python3 -m mousart
```

#### Method 3: Install with pip

```bash
# 1. Install system dependencies
sudo apt install socat

# 2. Install Python dependencies
pip3 install PyQt5 pyserial

# 3. Clone and run
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### Method 1: Run from source

```bash
# 1. Install Python 3.10+ from python.org

# 2. Install dependencies
pip install PyQt5 pyserial

# 3. Clone and run
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### Method 2: Build EXE

```bash
# 1. Install dependencies
pip install PyQt5 pyserial pyinstaller

# 2. Build
pyinstaller pyinstaller.spec --noconfirm

# 3. Run dist/MOUSART.exe
```

---

## Uninstallation

### Linux deb package

```bash
# Method 1: Uninstall with apt
sudo apt remove mouserial

# Method 2: Complete uninstall (including config files)
sudo apt purge mouserial

# Clean user config (optional)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Linux source installation

```bash
# Delete project directory
rm -rf /path/to/MOUSART

# Clean user config (optional)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Windows

```
# Delete project directory

# Clean user config (optional)
# Delete %USERPROFILE%\.mousart
# Delete %USERPROFILE%\mousart_logs
```

---

## Usage Guide

### Serial Debug Mode
1. Select **"Debug"** mode in the left panel
2. Select a port from the dropdown
3. Configure serial parameters (baud rate, data bits, stop bits, parity, flow control)
4. Click **"Open"** to connect
5. Type in the send area, click **"Send"** or press `Ctrl+Enter`
6. Receive area shows incoming data in real-time

### Virtual Serial Port Mode (Linux only)
1. Select **"Virtual"** mode in the left panel
2. Click **"Start"** to create a virtual port pair
3. The external port path `/tmp/mousart_vport` is displayed
4. Connect any serial tool to this path
5. Type in the send area and send

### Quick Commands
1. Click **"+"** in the quick command bar to add a new command
2. Enter name and data (text or HEX supported)
3. Left-click a command button to send immediately
4. Right-click to edit or delete

### Auto-Reply (Serial Debug Mode)
1. Find the **"Auto Reply"** section in the left panel
2. Enable the toggle
3. Set the match keyword and response data
4. Optionally set a reply delay (ms)

### Modbus Frame Builder
1. Click **"Modbus"** in the send toolbar
2. Set slave address, function code, start address, quantity
3. Click **"Build"** to generate a Modbus RTU frame with CRC

### Log Recording & Export
1. Click **"Record"** in the receive toolbar to start auto-recording
2. All data is saved to `~/mousart_logs/`
3. Click **"Save"** to manually export as TXT or CSV

### Pin Control (Serial Debug Mode)
1. After opening a port, the pin control bar appears in the left panel
2. Click DTR/RTS buttons to toggle pin levels
3. CTS/DSR/DCD/RI status LEDs show real-time pin states

---

## FAQ

**Q: Why can't I open the port?**
A: Usually a permissions issue. Add your user to the `dialout` group:
```bash
sudo usermod -aG dialout $USER
# Log out and back in for changes to take effect
```

**Q: Virtual serial port doesn't work?**
A: Make sure `socat` is installed:
```bash
sudo apt install socat
```

**Q: Chinese characters appear as garbled text?**
A: Select the correct encoding in the **"Encoding"** dropdown (e.g., GBK).

**Q: How to send Modbus commands?**
A: Click **"Modbus"**, fill in parameters, click **"Build"** to auto-generate the frame.

**Q: Where are auto-recorded files saved?**
A: Default location is `~/mousart_logs/`, filenames follow `mousart_rec_YYYYMMDD_HHmmss.log`.

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

**MOUSART** - Making serial debugging simpler and more efficient!
