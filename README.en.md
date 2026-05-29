# MOUSART
## Full-Featured Serial Port Debugger

<div align="center">

**[简体中文](README.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v2.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-Qt5%20%7C%20CMake-green)](https://www.qt.io/)
[![C++](https://img.shields.io/badge/C%2B%2B-17-blue)](https://isocpp.org/)

**MOUSART** is a full-featured serial port debugging tool built with Qt5/QML, designed for embedded development, hardware debugging, and serial communication. Version 2.0 adds auto-reply, Modbus protocol support, quick commands, data recording & export, pin control, multi-encoding support, and dozens of professional features.

---

## Feature Overview

### 1. Connection Management
- Auto-refresh available port list (2s polling)
- Virtual serial port, USB-to-serial, Bluetooth serial support
- Baud rate: 300 ~ 921600 presets + custom (1-9999999)
- Data bits: 5, 6, 7, 8
- Stop bits: 1, 1.5, 2
- Parity: None, Even, Odd, Mark, Space
- Flow control: None / Hardware (RTS/CTS) / Software (XON/XOFF)
- DTR/RTS manual control
- CTS/DSR/DCD/RI pin state monitoring
- Connection status indicator

### 2. Data Reception
- Text mode (UTF-8 / GBK / GB18030 / Latin-1 / ASCII encoding)
- Hexadecimal (HEX) display mode
- Timestamp display (millisecond precision hh:mm:ss.zzz)
- Direction indicator (`<<` RX / `>>` TX / `!!` ERR)
- Pause display (background still receives)
- Keyword filter (plain text / regex)
- Search function
- Log limit: 2000 entries with auto-scroll

### 3. Data Transmission
- Text / HEX send mode toggle
- Newline control (CR / LF independent toggle)
- Timed auto-send (1ms ~ 3600000ms, with count limit)
- File send (send any file's raw content)
- Send echo control
- Modbus RTU frame builder (auto CRC)
- Quick command bar (add/edit/delete, left-click send, right-click edit, persistent)
- Send sequence/queue (sequential send with loop support)
- Ctrl+Enter shortcut

### 4. Auto-Reply
- Auto-respond when specific keyword is received
- Configurable reply delay (ms)
- One-click enable/disable
- Rules persist across sessions

### 5. Encoding & Conversion Tools
- Text <-> Hex conversion
- Multi-encoding: UTF-8, GBK, GB18030, Latin-1, ASCII
- Special character escape/unescape (`\r\n`, `\x00`, etc.)
- Checksum: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Modbus RTU frame builder & parser
- Binary / Decimal / Hex number conversion

### 6. Data Recording & Export
- One-click save log to TXT / CSV
- Auto-recording with file rotation (10MB/file)
- Real-time RX/TX byte counter and rate display (B/s, KB/s, MB/s)
- Full send/receive log with timestamps and direction

### 7. Virtual Serial Port (Linux only)
- One-click virtual port pair creation via `socat`
- Auto-detect virtual ports from other MOUSART instances
- External programs connect via `/tmp/mousart_vport`
- Independent RX/TX stats and encoding settings

### 8. UI & Configuration
- Dark / Light theme with smooth switching
- 0.8x-1.5x continuous font scaling
- Custom frameless window (drag, double-click maximize, edge resize)
- Profile management: save/load/switch multiple configurations
- Serial params, quick commands, auto-reply rules persist with profiles

---

## Screenshots

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART Debug Interface">
  <br>
  <em>MOUSART Serial Debug Interface (Light Theme)</em>
</div>
<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART Virtual Port Interface">
  <br>
  <em>MOUSART Virtual Port Interface (Light Theme)</em>
</div>

---

## Quick Start

### Pre-built Releases

Download from [GitHub Releases](https://github.com/kryntx/MOUSART/releases):

| Platform | File | Size |
|----------|------|------|
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | ~105KB |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | ~23MB |

> Windows version includes all Qt5 runtime dependencies. Extract and run. Hardware serial debug fully functional; virtual serial port is Linux-only.

> **Linux runtime dependencies**: The pre-built Linux binary requires Qt5 QML runtime libraries:
> ```bash
> sudo apt install qtdeclarative5-dev libqt5serialport5-dev \
>   qml-module-qtquick2 qml-module-qtquick-controls2 \
>   qml-module-qtquick-layouts qml-module-qtquick-window2 \
>   qml-module-qtquick-templates2 qml-module-qtqml-models2
> ```

### Build from Source

#### Requirements
- Qt 5 (Core, Gui, Qml, Quick, Widgets, SerialPort)
- CMake >= 3.16
- C++17 compiler
- socat (Linux, for virtual serial port only)

#### Linux Build

```bash
# Ubuntu/Debian dependencies
sudo apt update
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat

# Clone and build
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# Run
./build/MOUSART
```

#### Windows Cross-Compile (Linux -> Windows)

```bash
sudo apt install mingw-w64
pip3 install aqtinstall
aqt install-qt windows desktop 5.15.2 win64_mingw81 -O qt5-win

cmake -B build-win \
  -DCMAKE_TOOLCHAIN_FILE=cmake/mingw-w64-toolchain.cmake \
  -DCMAKE_PREFIX_PATH=qt5-win/5.15.2/mingw81_64 \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build-win
```

---

## Usage Guide

### Virtual Serial Port Mode
1. Switch to **"Virtual"** mode in the left panel
2. Click **"Start"** to create a virtual port pair
3. The external port path `/tmp/mousart_vport` is displayed
4. Connect any serial tool to this path
5. Send/receive data between MOUSART and the external program
6. Click **"Stop"** to close

### Hardware Serial Debug Mode
1. Switch to **"Debug"** mode in the left panel
2. Select a port from the dropdown
3. Configure: baud rate, data bits, stop bits, parity, flow control
4. Click **"Open"** to connect
5. Type in the send area and click **"Send"** or press `Ctrl+Enter`
6. Received data appears in real-time in the log area

### Quick Commands
1. Click **"+"** in the quick command bar to add a new command
2. Enter name and data (text or HEX supported)
3. Left-click a command button to send immediately
4. Right-click to edit or delete
5. All commands are auto-saved and restored on next launch

### Auto-Reply
1. Find the **"Auto Reply"** section in the left panel
2. Enable the toggle
3. Set the match keyword (triggers when received data contains this)
4. Set the response data (auto-sent content)
5. Optionally set a reply delay (ms)

### Modbus Frame Builder
1. Click **"Modbus"** in the send toolbar to expand the Modbus panel
2. Set slave address, function code, start address, quantity
3. Click **"Build"** to generate a Modbus RTU frame with CRC
4. Frame data auto-fills the send area

### Log Recording & Export
1. Click **"Record"** in the receive toolbar to start auto-recording
2. All data is saved to `~/mousart_logs/`
3. Files auto-split at 10MB
4. Click **"Save"** to manually export as TXT or CSV

### Pin Control
1. After opening a port, the pin control bar appears in the left panel
2. Click DTR/RTS buttons to toggle pin levels
3. CTS/DSR/DCD/RI status LEDs show real-time pin states

### Profile Management
1. Find **"Profile"** at the bottom of the left panel
2. Click **"Save"** to save current settings to a profile
3. Use the dropdown to switch profiles
4. Profiles save: serial params, quick commands, auto-reply rules

---

## Serial Parameters

| Parameter | Values |
|-----------|--------|
| **Baud Rate** | 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600 or custom (1-9999999) |
| **Data Bits** | 5, 6, 7, 8 |
| **Stop Bits** | 1, 1.5, 2 |
| **Parity** | None, Odd, Even, Mark, Space |
| **Flow Control** | None, Hardware (RTS/CTS), Software (XON/XOFF) |
| **Receive Encoding** | UTF-8, GBK, GB18030, Latin-1, ASCII |
| **Timed Send Interval** | 1 - 3600000 ms (default 1000ms) |

---

## Project Structure

```
MOUSART/
├── CMakeLists.txt                   # CMake build config (v2.0.0)
├── qml.qrc                          # QML resource file
├── cmake/
│   └── mingw-w64-toolchain.cmake    # MinGW-w64 cross-compile toolchain
├── img/                             # Screenshots
├── src/                             # C++ source code
│   ├── main.cpp                     # Entry point
│   └── core/                        # Core modules
│       ├── thememanager.h/.cpp      # Theme & font scaling
│       ├── serialportmanager.h/.cpp # Serial I/O, pin control, auto-reply, stats
│       ├── virtualserialmanager.h/.cpp # Virtual port (socat-based)
│       ├── configmanager.h/.cpp     # Config, quick commands, profiles
│       ├── dataanalyzer.h/.cpp      # Encoding, checksums, Modbus, conversion
│       └── logfilemanager.h/.cpp    # Log save, export, auto-recording
└── qml/                             # QML UI code
    ├── main.qml                     # Main window (frameless)
    ├── TitleBar.qml                 # Title bar
    ├── SettingsPanel.qml            # Left panel (config, pins, auto-reply, profiles)
    ├── DataPanel.qml                # Right panel (log, send, Modbus, quick commands)
    └── components/                  # Reusable QML components
```

---

## Changelog

### v2.0.0 (2026-05-29)
**Major feature update**

**New:**
- Pin control: DTR/RTS manual toggle, CTS/DSR/DCD/RI real-time monitoring
- Auto-reply: auto-respond on keyword match with configurable delay
- Quick command bar: editable send buttons with persistent storage
- Multi-encoding: UTF-8 / GBK / GB18030 / Latin-1 / ASCII
- Newline control: CR / LF independent toggle
- File send: send any file directly
- Modbus RTU frame builder & parser
- Log export: TXT / CSV format with auto-recording
- RX/TX real-time stats: byte count and rate display
- Data filtering: keyword / regex
- Profile management: save/load/switch configurations
- Checksum tools: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Send sequence/queue with loop support
- Send count limit

**Improved:**
- Baud rate presets extended to 300-921600
- Log limit raised from 500 to 2000
- Virtual port mode gains encoding and stats support

### v1.0.0 (2026-05-27)
- Initial release
- Virtual and hardware serial port dual mode
- HEX display and send
- Timed auto-send
- Timestamp control
- Dark/Light theme
- Windows cross-compilation support

---

## FAQ

**Q: Why can't I open the port?**
A: Usually a permissions issue. Try `sudo ./build/MOUSART` or add your user to the `dialout` group:
```bash
sudo usermod -aG dialout $USER
```
Log out and back in for changes to take effect.

**Q: Virtual serial port doesn't work?**
A: Make sure `socat` is installed:
```bash
sudo apt install socat
```

**Q: Chinese characters appear as garbled text?**
A: Select the correct encoding in the **"Encoding"** dropdown in the left panel (e.g., GBK).

**Q: How to send Modbus commands?**
A: Click **"Modbus"** in the send toolbar, fill in slave address, function code, start address, and quantity, click **"Build"** to auto-generate the frame, then click Send.

**Q: Where are auto-recorded files saved?**
A: Default location is `~/mousart_logs/`, filenames follow `mousart_rec_YYYYMMDD_HHmmss.log`.

---

## Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

---

## Support

If you encounter any issues or have suggestions:
- Submit a [GitHub Issue](https://github.com/kryntx/MOUSART/issues)

**MOUSART** - Making serial debugging simpler and more efficient!
