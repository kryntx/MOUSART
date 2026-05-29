# MOUSART
## 全功能串口调试工具

<div align="center">

**[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-PyQt6%20%7C%20Python-green)](https://www.riverbankcomputing.com/software/pyqt/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

**MOUSART** 是一款基于 Python/PyQt6 构建的全功能串口调试工具，专为嵌入式开发、硬件调试和串口通信场景设计。v3.0 为完全重构版本，采用 Python 重写，支持 Windows 和 Linux 双平台，包含自动应答、Modbus 协议支持、快捷命令、数据录制与导出、引脚控制、多编码支持等数十项专业功能。

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

| 平台 | 下载文件 | 说明 |
|------|---------|------|
| **Linux x86_64 (deb)** | `mouserial_3.0.0-1_amd64.deb` | Debian/Ubuntu 安装包 |
| **Windows x86_64** | `MOUSART-v3.0.0-windows-x86_64.exe` | 单文件便携版 |

#### Debian/Ubuntu 安装 (推荐)
```bash
# 下载并安装 deb 包（自动处理依赖）
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb
sudo apt install ./mouserial_3.0.0-1_amd64.deb
```

> Windows 版本为单文件 exe，双击即可运行，无需安装。

### 从源码运行

```bash
# Ubuntu/Debian 依赖安装
sudo apt update
sudo apt install python3-pyqt6 python3-serial socat

# 克隆项目
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 安装 Python 依赖
pip3 install PyQt6 pyserial

# 运行
python3 -m mousart
```

#### 构建 Windows EXE

```bash
pip3 install pyinstaller
pyinstaller pyinstaller.spec --noconfirm
# 输出: dist/MOUSART.exe
```

#### 构建 Debian 包

```bash
sudo apt install dh-python python3-setuptools debhelper
dpkg-buildpackage -us -uc -b
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
├── pyproject.toml                   # Python 项目配置
├── pyinstaller.spec                 # PyInstaller 打包配置
├── Makefile                         # 构建自动化
├── scripts/                         # 构建脚本
│   ├── build_exe.sh                 # Windows EXE 构建
│   ├── build_deb.sh                 # Debian 包构建
│   └── build_icons.sh              # 图标生成
├── resources/icons/                 # 应用图标
│   ├── mousart.svg                  # 源 SVG 图标
│   └── mousart_*.png               # 各尺寸 PNG
├── mousart/                         # Python 源代码
│   ├── __main__.py                  # 入口点
│   ├── app.py                       # 应用启动
│   ├── core/                        # 核心模块
│   │   ├── theme_manager.py         # 主题管理
│   │   ├── serial_manager.py        # 串口 I/O、引脚、自动应答
│   │   ├── virtual_serial_manager.py # 虚拟串口
│   │   ├── config_manager.py        # 配置管理、Profile
│   │   ├── data_analyzer.py         # 编码、校验和、Modbus
│   │   └── log_file_manager.py      # 日志保存、导出
│   ├── ui/                          # 界面模块
│   │   ├── main_window.py           # 主窗口
│   │   ├── title_bar.py             # 标题栏
│   │   ├── settings_panel.py        # 左侧设置面板
│   │   ├── data_panel.py            # 右侧数据面板
│   │   ├── widgets/                 # 可复用组件
│   │   └── dialogs/                 # 对话框
│   └── utils/                       # 工具模块
│       ├── constants.py             # 常量定义
│       ├── encoding.py              # 编码转换
│       ├── checksum.py              # 校验和计算
│       ├── modbus.py                # Modbus 帧构建/解析
│       ├── number_convert.py        # 进制转换
│       ├── hex_display.py           # HEX 显示格式化
│       └── stylesheet.py            # QSS 样式生成
└── debian/                          # Debian 打包配置
```

---

## 更新日志

### v3.0.0 (2026-05-29)
**完全重构 - Python/PyQt6 版本**

- 完全使用 Python 重写，从 C++/Qt5/QML 迁移到 Python/PyQt6
- 更简洁的代码结构，更易于维护和扩展
- 保持所有 v2.0.0 功能完整
- 优化跨平台支持（Windows EXE + Linux deb）
- 新增应用图标设计

### v2.0.0 (2026-05-29)
**重大功能更新**

新增：引脚控制、自动应答、快捷命令栏、多编码支持、发送换行控制、文件发送、Modbus RTU 帧构建器与解析器、日志保存导出、RX/TX 实时统计、数据过滤、配置管理、校验和工具、发送序列/队列、发送次数限制

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
