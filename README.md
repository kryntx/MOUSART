# MOUSART
## 全功能串口调试工具

<div align="center">

**[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

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
- 数据位：5, 6, 7, 8 / 停止位：1, 1.5, 2
- 校验位：None, Even, Odd, Mark, Space
- 流控：无 / 硬件 (RTS/CTS) / 软件 (XON/XOFF)
- DTR/RTS 手动置位控制
- CTS/DSR/DCD/RI 引脚电平实时监视

### 二、数据接收
- 文本模式（UTF-8 / GBK / GB18030 / Latin-1 / ASCII 编码可选）
- 十六进制 (HEX) 显示模式
- 时间戳显示（精确到毫秒 hh:mm:ss.zzz）
- 数据方向标识（`<<` RX / `>>` TX / `!!` ERR）
- 暂停显示（后台仍接收，界面不刷新）
- 关键字过滤（普通文本 / 正则表达式）
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
- 一键启用/禁用，规则持久化保存

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

### 七、虚拟串口（仅 Linux）
- 基于 `socat` 一键创建虚拟串口对
- 自动发现多实例创建的虚拟串口
- 外部程序通过 `/tmp/mousart_vport` 连接

### 八、界面与配置
- 内置深色/浅色双主题，平滑切换
- 0.8x-1.5x 连续字体缩放
- 配置管理：保存/加载/切换多套配置（Profile）

---

## 截图

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 串口调试界面">
  <br>
  <em>MOUSART 串口调试界面（浅色主题）</em>
</div>
<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART 虚拟串口界面">
  <br>
  <em>MOUSART 虚拟串口界面（浅色主题）</em>
</div>

---

## 快速开始

### 预构建版本

从 [GitHub Releases](https://github.com/kryntx/MOUSART/releases) 下载：

| 平台 | 下载文件 | 大小 |
|------|---------|------|
| **Linux x86_64 (deb)** | `mouserial_2.0.0-1_amd64.deb` | ~82KB |
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | ~105KB |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | ~23MB |

#### Debian/Ubuntu 安装 (推荐)
```bash
# 下载并安装 deb 包
wget https://github.com/kryntx/MOUSART/releases/download/v2.0.0/mouserial_2.0.0-1_amd64.deb
sudo dpkg -i mouserial_2.0.0-1_amd64.deb
sudo apt-get install -f  # 自动修复依赖
```

> Windows 版本已包含所有运行时依赖，解压即可运行。

> **Linux 运行依赖**：预构建版本需要系统安装 Qt5 QML 运行时库：
> ```bash
> sudo apt install qtdeclarative5-dev libqt5serialport5-dev \
>   qml-module-qtquick2 qml-module-qtquick-controls2 \
>   qml-module-qtquick-layouts qml-module-qtquick-window2 \
>   qml-module-qtquick-templates2 qml-module-qtqml-models2
> ```

### 从源码构建

```bash
# Ubuntu/Debian 依赖安装
sudo apt update
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat

# 克隆并编译
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# 运行
./build/MOUSART
```

#### Windows 交叉编译

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

## 使用指南

### 虚拟串口模式
1. 在左侧面板切换到 **"模拟串口"** 模式
2. 点击 **"启动"** 按钮创建虚拟串口
3. 界面显示外部端口路径 `/tmp/mousart_vport`
4. 使用任意串口工具连接到此路径
5. 在发送区输入数据并点击 **"发送"** 或按 `Ctrl+Enter`

### 硬件串口调试模式
1. 切换到 **"串口调试"** 模式
2. 从下拉列表中选择串口
3. 配置串口参数：波特率、数据位、停止位、校验位、流控制
4. 点击 **"打开"** 建立连接
5. 在发送区输入数据并发送

### 快捷命令
1. 在底部快捷命令栏点击 **"+"** 添加新命令
2. 输入名称和数据（支持文本和 HEX）
3. 左键点击命令按钮立即发送
4. 右键点击命令按钮编辑或删除

### 自动应答
1. 在左侧面板找到 **"自动应答"** 区域
2. 启用开关，设置匹配关键字和应答数据
3. 可选设置应答延迟（毫秒）

### Modbus 帧构建
1. 在发送工具栏点击 **"Modbus"** 按钮
2. 设置从站地址、功能码、起始地址、数量
3. 点击 **"构建"** 自动生成带 CRC 的 Modbus RTU 帧

### 日志录制与导出
1. 点击接收区工具栏的 **"录制"** 按钮开始自动录制
2. 所有收发数据自动保存到 `~/mousart_logs/`
3. 点击 **"保存"** 可手动导出为 TXT 或 CSV

### 引脚控制
1. 打开串口后，左侧面板显示引脚控制栏
2. 点击 DTR/RTS 按钮切换引脚电平
3. CTS/DSR/DCD/RI 状态灯实时显示

### 配置管理
1. 在左侧面板底部找到 **"配置 Profile"** 区域
2. 点击 **"保存"** 保存当前设置
3. 下拉列表切换不同的 Profile

---

## 串口参数

| 参数 | 可选值 |
|------|--------|
| **波特率** | 300 ~ 921600 预设 + 自定义 (1-9999999) |
| **数据位** | 5, 6, 7, 8 |
| **停止位** | 1, 1.5, 2 |
| **校验位** | None, Odd, Even, Mark, Space |
| **流控制** | None, Hardware, Software |
| **接收编码** | UTF-8, GBK, GB18030, Latin-1, ASCII |
| **定时发送间隔** | 1 - 3600000 ms |

---

## 项目结构

```
MOUSART/
├── CMakeLists.txt                   # CMake 构建配置
├── qml.qrc                          # QML 资源文件
├── cmake/                           # 交叉编译工具链
├── img/                             # 截图
├── src/                             # C++ 源代码
│   ├── main.cpp                     # 入口点
│   └── core/                        # 核心模块
│       ├── thememanager.h/.cpp      # 主题管理
│       ├── serialportmanager.h/.cpp # 串口 I/O、引脚、自动应答、统计
│       ├── virtualserialmanager.h/.cpp # 虚拟串口
│       ├── configmanager.h/.cpp     # 配置管理、Profile
│       ├── dataanalyzer.h/.cpp      # 编码、校验和、Modbus
│       └── logfilemanager.h/.cpp    # 日志保存、导出
└── qml/                             # QML 界面
    ├── main.qml                     # 主窗口
    ├── TitleBar.qml                 # 标题栏
    ├── SettingsPanel.qml            # 左侧设置面板
    ├── DataPanel.qml                # 右侧数据面板
    └── components/                  # 可复用组件
```

---

## 更新日志

### v2.0.0 (2026-05-29)
**重大功能更新**

新增：引脚控制、自动应答、快捷命令栏、多编码支持、发送换行控制、文件发送、Modbus RTU 帧构建器与解析器、日志保存导出、RX/TX 实时统计、数据过滤、配置管理、校验和工具、发送序列/队列、发送次数限制

改进：波特率预设扩展至 300-921600，日志上限提升至 2000，虚拟串口新增编码和统计支持

### v1.0.0 (2026-05-27)
- 初始发布

---

## 常见问题

**Q: 无法打开串口？** 通常是权限问题，使用 `sudo` 或将用户添加到 `dialout` 组。

**Q: 虚拟串口无法使用？** 请确保已安装 `socat`：`sudo apt install socat`

**Q: 中文显示乱码？** 在左侧面板选择正确的接收编码（如 GBK）。

---

## 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE)。

**MOUSART** - 让串口调试更简单、更高效！
