# MOUSART
## 全功能串口调试工具 | Full-Featured Serial Port Debugger

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v2.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-Qt5%20%7C%20CMake-green)](https://www.qt.io/)
[![C++](https://img.shields.io/badge/C%2B%2B-17-blue)](https://isocpp.org/)

**MOUSART** 是一款基于 Qt5/QML 构建的全功能串口调试工具，专为嵌入式开发、硬件调试和串口通信场景设计。v2.0 新增了自动应答、Modbus 协议支持、快捷命令、数据录制与导出、引脚控制、多编码支持等数十项专业功能。

---

## 功能总览

### 一、串口连接管理
- 自动刷新可用串口列表（2秒轮询）
- 支持虚拟串口、USB转串口、蓝牙串口
- 波特率：300 ~ 921600 预设值 + 自定义值 (1-9999999)
- 数据位：5, 6, 7, 8
- 停止位：1, 1.5, 2
- 校验位：None, Even, Odd, Mark, Space
- 流控：无 / 硬件 (RTS/CTS) / 软件 (XON/XOFF)
- DTR/RTS 手动置位控制
- CTS/DSR/DCD/RI 引脚电平实时监视
- 连接/断开状态指示
- 打开失败错误提示，关闭后自动释放资源

### 二、数据接收
- 文本模式（UTF-8 / GBK / GB18030 / Latin-1 / ASCII 编码可选）
- 十六进制 (HEX) 显示模式
- 时间戳显示（精确到毫秒 hh:mm:ss.zzz）
- 数据方向标识（`<<` RX / `>>` TX / `!!` ERR）
- 暂停显示（后台仍接收，界面不刷新）
- 关键字过滤（普通文本 / 正则表达式）
- 搜索功能
- 日志条目上限 2000 条，自动滚动

### 三、数据发送
- 文本 / HEX 发送模式切换
- 发送换行控制（CR / LF 独立开关）
- 定时发送（1ms ~ 3600000ms 可调，支持次数限制）
- 文件发送（选择任意文件发送原始内容）
- 发送回显控制
- Modbus RTU 帧构建器（地址/功能码/起始地址/数量，自动 CRC）
- 快捷命令栏（可添加/编辑/删除，左键发送，右键编辑，持久化保存）
- 发送序列/队列（按顺序依次发送多条数据，支持循环）
- Ctrl+Enter 快捷键发送

### 四、自动应答
- 收到特定关键字时自动发送预设数据
- 支持配置应答延迟（毫秒级）
- 一键启用/禁用
- 匹配规则持久化保存

### 五、编码与转换工具
- 文本 ↔ Hex 实时转换
- 多编码支持：UTF-8, GBK, GB18030, Latin-1, ASCII
- 特殊字符转义/反转义（`\r\n`, `\x00` 等）
- 校验和计算：Sum8 / XOR8 / CRC16-Modbus / CRC32
- Modbus RTU 帧构建与解析
- 二进制 / 十进制 / 十六进制进制转换

### 六、数据记录与导出
- 一键保存日志到 TXT / CSV 文件
- 自动录制功能（带文件大小自动分割，10MB/文件）
- 实时 RX/TX 字节计数和速率显示 (B/s, KB/s, MB/s)
- 完整收发日志（带时间戳和方向标识）

### 七、虚拟串口（仅 Linux）
- 基于 `socat` 一键创建虚拟串口对
- 自动发现多实例创建的虚拟串口
- 外部程序通过 `/tmp/mousart_vport` 连接
- 独立的 RX/TX 统计和编码设置

### 八、界面与配置
- 内置深色/浅色双主题，平滑切换
- 0.8x-1.5x 连续字体缩放
- 自定义无边框窗口（拖拽移动、双击最大化、边缘调整大小）
- 配置管理：保存/加载/切换多套配置（Profile）
- 串口参数、快捷命令、自动应答规则随 Profile 持久化

---

## 截图

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 串口调试界面">
  <br>
  <em>MOUSART 串口调试界面（深色主题）</em>
</div>
<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART 虚拟串口界面">
  <br>
  <em>MOUSART 虚拟串口界面（深色主题）</em>
</div>

---

## 快速开始

### 预构建版本

从 [GitHub Releases](https://github.com/kryntx/MOUSART/releases) 下载对应平台的预构建版本：

| 平台 | 下载文件 | 说明 |
|------|---------|------|
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | 解压运行 |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | 含全部 Qt5 运行时依赖，解压即用 |

> Windows 版本已包含所有运行时依赖（Qt5 DLL），解压即可运行。硬件串口调试功能完全可用，虚拟串口功能暂仅支持 Linux。

### 从源码构建

#### 系统要求
- Qt 5 (Core, Gui, Qml, Quick, Widgets, SerialPort)
- CMake >= 3.16
- C++17 兼容编译器
- socat (仅 Linux 虚拟串口功能需要)

#### Linux 构建

```bash
# Ubuntu/Debian 依赖安装
sudo apt update
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat

# 克隆仓库
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 编译
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# 运行（如遇串口权限问题，使用 sudo 或将用户添加到 dialout 组）
./build/MOUSART
```

#### Windows 交叉编译（Linux → Windows）

```bash
# 安装 MinGW-w64
sudo apt install mingw-w64

# 下载 Qt5 Windows MinGW 预编译库（需要 Python 3）
pip3 install aqtinstall
aqt install-qt windows desktop 5.15.2 win64_mingw81 -O qt5-win

# 交叉编译
cmake -B build-win \
  -DCMAKE_TOOLCHAIN_FILE=cmake/mingw-w64-toolchain.cmake \
  -DCMAKE_PREFIX_PATH=qt5-win/5.15.2/mingw81_64 \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build-win

# 运行时需将 Qt5 DLL 和 qml/ 目录放到 MOUSART.exe 同级目录
```

---

## 使用指南

### 虚拟串口模式
1. 在左侧面板切换到 **"模拟串口 Virtual"** 模式
2. 点击 **"启动 Start"** 按钮创建虚拟串口
3. 界面将显示外部端口路径 `/tmp/mousart_vport`
4. 使用任意串口工具连接到此路径
5. 在发送区输入数据并点击 **"发送 Send"** 或按 `Ctrl+Enter`
6. 点击 **"停止 Stop"** 关闭虚拟串口

### 硬件串口调试模式
1. 在左侧面板切换到 **"串口调试 Debug"** 模式
2. 从下拉列表中选择要连接的串口
3. 配置串口参数：波特率、数据位、停止位、校验位、流控制
4. 点击 **"打开 Open"** 建立连接
5. 在发送区输入数据并发送
6. 接收区将实时显示接收到的数据

### 快捷命令
1. 在底部快捷命令栏点击 **"+"** 添加新命令
2. 输入名称和数据（支持文本和 HEX）
3. 左键点击命令按钮立即发送
4. 右键点击命令按钮编辑或删除
5. 所有命令自动保存，下次启动时恢复

### 自动应答
1. 在左侧面板找到 **"自动应答"** 区域
2. 启用开关
3. 设置匹配关键字（接收到包含此关键字的数据时触发）
4. 设置应答数据（自动发送的内容）
5. 可选设置应答延迟（毫秒）

### Modbus 帧构建
1. 在发送工具栏点击 **"Modbus"** 按钮展开 Modbus 面板
2. 设置从站地址、功能码、起始地址、数量
3. 点击 **"构建"** 自动生成带 CRC 的 Modbus RTU 帧
4. 帧数据自动填入发送区，点击发送即可

### 日志录制与导出
1. 点击接收区工具栏的 **"录制"** 按钮开始自动录制
2. 所有收发数据自动保存到 `~/mousart_logs/` 目录
3. 文件超过 10MB 自动分割
4. 点击 **"保存"** 可手动导出当前日志为 TXT 或 CSV 格式

### 引脚控制
1. 打开串口后，左侧面板显示引脚控制栏
2. 点击 DTR/RTS 按钮切换引脚电平
3. CTS/DSR/DCD/RI 状态灯实时显示对方引脚电平

### 配置管理
1. 在左侧面板底部找到 **"配置 Profile"** 区域
2. 点击 **"保存"** 保存当前所有设置到 Profile
3. 下拉列表切换不同的 Profile
4. Profile 保存内容：串口参数、快捷命令、自动应答规则

---

## 串口参数配置

| 参数 | 可选值 |
|------|--------|
| **波特率** | 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600<br>或自定义值 (1 - 9999999) |
| **数据位** | 5, 6, 7, 8 |
| **停止位** | 1, 1.5, 2 |
| **校验位** | None, Odd, Even, Mark, Space |
| **流控制** | None, Hardware (RTS/CTS), Software (XON/XOFF) |
| **接收编码** | UTF-8, GBK, GB18030, Latin-1, ASCII |
| **定时发送间隔** | 1 - 3600000 ms（默认 1000ms） |

---

## 项目结构

```
MOUSART/
├── CMakeLists.txt                   # CMake 构建配置 (v2.0.0)
├── qml.qrc                          # QML 资源文件
├── cmake/
│   └── mingw-w64-toolchain.cmake    # MinGW-w64 交叉编译工具链
├── img/                             # 项目截图
├── src/                             # C++ 源代码
│   ├── main.cpp                     # 程序入口点
│   └── core/                        # 核心功能模块
│       ├── thememanager.h/.cpp      # 主题和字体缩放管理
│       ├── serialportmanager.h/.cpp # 硬件串口 I/O、引脚控制、自动应答、统计
│       ├── virtualserialmanager.h/.cpp # 虚拟串口管理 (基于 socat)
│       ├── configmanager.h/.cpp     # 配置管理、快捷命令、Profile
│       ├── dataanalyzer.h/.cpp      # 编码转换、校验和、Modbus、进制转换
│       └── logfilemanager.h/.cpp    # 日志保存、导出、自动录制
└── qml/                             # QML 界面代码
    ├── main.qml                     # 主窗口 (无边框)
    ├── TitleBar.qml                 # 标题栏 (主题/字体控制)
    ├── SettingsPanel.qml            # 左侧设置面板 (串口配置/引脚/自动应答/Profile)
    ├── DataPanel.qml                # 右侧数据面板 (日志/发送/Modbus/快捷命令)
    └── components/                  # 可复用 QML 组件
        ├── WindowButton.qml
        ├── ModeButton.qml
        ├── ActionButton.qml
        ├── StyledComboBox.qml
        ├── EditableComboBox.qml
        ├── SmallButton.qml
        ├── SmallToggle.qml
        ├── DataStatsBar.qml         # RX/TX 统计栏
        ├── QuickCommandBar.qml      # 快捷命令栏
        ├── PinControlBar.qml        # DTR/RTS/CTS/DSR 引脚控制
        └── AutoReplyPanel.qml       # 自动应答配置面板
```

---

## 更新日志

### v2.0.0 (2026-05-29)
**重大功能更新**

**新增功能：**
- 引脚控制：DTR/RTS 手动置位，CTS/DSR/DCD/RI 实时监视
- 自动应答：收到特定关键字自动回复，支持延迟配置
- 快捷命令栏：可编辑的快捷发送按钮，持久化保存
- 多编码支持：UTF-8 / GBK / GB18030 / Latin-1 / ASCII
- 发送换行控制：CR / LF 独立开关
- 文件发送：选择任意文件直接发送
- Modbus RTU 帧构建器：自动生成带 CRC 的 Modbus 帧
- Modbus 帧解析器：解析 Modbus RTU 响应帧
- 日志保存：导出为 TXT / CSV 格式
- 自动录制：数据自动保存到文件，支持文件分割
- RX/TX 实时统计：字节计数和速率显示
- 发送回显控制
- 数据过滤：关键字 / 正则表达式过滤接收数据
- 搜索功能
- 暂停显示（后台仍接收）
- 数据方向标识（RX/TX/ERR）
- 配置管理：多套 Profile 保存/加载/切换
- 校验和工具：Sum8 / XOR8 / CRC16-Modbus / CRC32
- 发送序列/队列（按顺序发送多条数据，支持循环）
- 发送次数限制

**改进：**
- 波特率预设扩展至 300-921600
- 日志条目上限从 500 提升至 2000
- 虚拟串口模式新增编码和统计支持
- 引脚状态读取增加设备未打开保护
- 版本号升级至 2.0.0

### v1.0.0 (2026-05-27)
- 初始发布
- 虚拟串口和硬件串口调试双模式
- HEX 显示和发送
- 定时发送
- 时间戳控制
- 深色/浅色主题
- Windows 交叉编译支持

---

## 常见问题

### Q: 为什么我无法打开串口？
A: 这通常是权限问题。尝试使用 `sudo ./build/MOUSART` 运行程序，或者将当前用户添加到 `dialout` 组：
```bash
sudo usermod -aG dialout $USER
```
注销并重新登录后生效。

### Q: 虚拟串口功能无法使用？
A: 请确保已安装 `socat` 工具：
```bash
sudo apt install socat
```

### Q: 接收到的中文显示乱码？
A: 在左侧面板的 **"接收编码"** 下拉菜单中选择正确的编码（如 GBK）。

### Q: 如何发送 Modbus 指令？
A: 在发送工具栏点击 **"Modbus"** 按钮，填写从站地址、功能码、起始地址和数量，点击 **"构建"** 自动生成帧数据，然后点击发送。

### Q: 自动录制的文件保存在哪里？
A: 默认保存在 `~/mousart_logs/` 目录下，文件名格式为 `mousart_rec_YYYYMMDD_HHmmss.log`。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

---

## 许可证

本项目采用 **MIT 许可证** 开源 - 详见 [LICENSE](LICENSE) 文件。

---

## 支持与反馈

如果您在使用过程中遇到任何问题或有改进建议，请通过以下方式联系我们：
- 提交 [GitHub Issue](https://github.com/kryntx/MOUSART/issues)

**MOUSART** - 让串口调试更简单、更高效！
