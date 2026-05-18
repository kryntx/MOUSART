# MOUSART

A modern serial port debugging tool with virtual serial port support, built with Qt5/QML.

## Features

**Virtual Serial Port** — Create a virtual serial port pair using socat. MOUSART acts as one end while external programs connect to the other end at `/tmp/mousart_vport`. Multiple MOUSART instances can discover each other's virtual ports automatically.

**Serial Debug** — Connect to real hardware serial ports with full parameter configuration. Independently receive and send data with dedicated log and input areas per mode.

**HEX Mode** — Toggle HEX display for received data and HEX send for transmitted data. HEX strings are parsed with `QByteArray::fromHex()`.

**Dark / Light Theme** — Two built-in themes with smooth switching. Settings persist across sessions.

**Font Scaling** — Continuous zoom from 0.8x to 1.5x via the title bar slider.

**Custom Frameless Window** — Drag to move, double-click to maximize, edge and corner resize handles, Canvas-drawn window control buttons.

## Screenshot

<!-- Add screenshot here -->

## Requirements

- Qt 5 (Core, Gui, Qml, Quick, Widgets, SerialPort)
- CMake >= 3.16
- C++17 compiler
- socat (for virtual serial port feature)

### Install dependencies (Ubuntu/Debian)

```bash
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat
```

## Build

```bash
cmake -B build
cmake --build build
```

## Run

```bash
./build/MOUSART
# or with sudo if serial port permissions are needed
sudo ./build/MOUSART
```

## Usage

### Virtual Serial Port Mode

1. Switch to "模拟串口 Virtual" mode in the left panel
2. Click "启动 Start" to create the virtual port
3. The external port path `/tmp/mousart_vport` is displayed — connect to it from any serial tool
4. Data sent from the external program appears in the receive area; data typed in the send area goes to the external program
5. Click "停止 Stop" to tear down

### Serial Debug Mode

1. Switch to "串口调试 Debug" mode
2. Select a port, configure baud rate / data bits / stop bits / parity / flow control
3. Click "打开 Open" to connect
4. Type in the send area and press **Ctrl+Enter** or click "发送 Send"

### Multi-instance

Open two MOUSART windows. Start the virtual port in window 1 — window 2 will automatically detect `/tmp/mousart_vport` in its port list and can connect to it in debug mode.

## Serial Port Parameters

| Setting       | Options                                                       |
| ------------- | ------------------------------------------------------------- |
| Baud Rate     | 1200 – 921600 (preset list) or custom value (1 – 9999999)    |
| Data Bits     | 5, 6, 7, 8                                                   |
| Stop Bits     | 1, 1.5, 2                                                    |
| Parity        | None, Odd, Even, Mark, Space                                 |
| Flow Control  | None, Hardware, Software                                      |

## Project Structure

```
MOUSART/
├── CMakeLists.txt
├── qml.qrc
├── src/
│   ├── main.cpp                    # Entry point
│   └── core/
│       ├── thememanager.h/.cpp     # Theme and font scaling
│       ├── serialportmanager.h/.cpp # Real serial port I/O
│       └── virtualserialmanager.h/.cpp # Virtual serial port via socat
└── qml/
    ├── main.qml                    # Root frameless window
    ├── TitleBar.qml                # Title bar with theme/font controls
    ├── SettingsPanel.qml           # Left sidebar: mode + port config
    ├── DataPanel.qml               # Right area: log display + send input
    └── components/                 # Reusable QML components
        ├── WindowButton.qml
        ├── ModeButton.qml
        ├── ActionButton.qml
        ├── StyledComboBox.qml
        ├── EditableComboBox.qml
        ├── SmallButton.qml
        └── SmallToggle.qml
```

## License

<!-- Add license here -->
