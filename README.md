# MOUSART
## 全功能串口调试工具

<div align="center">

**[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.1.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.1.0)

**MOUSART** 是一款全功能串口调试工具，专为嵌入式开发、硬件调试和串口通信场景设计。支持串口调试和虚拟串口两种独立模式，具备自动应答、Modbus 协议支持、快捷命令、数据录制与导出、引脚控制、多编码支持等数十项专业功能。

---

## 截图

### 串口调试模式

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 串口调试界面">
  <br>
  <em>串口调试模式 - 连接真实硬件串口进行数据收发</em>
</div>

### 虚拟串口模式

<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART 虚拟串口界面">
  <br>
  <em>虚拟串口模式 - 创建虚拟串口对供外部程序连接</em>
</div>

---

## 功能特性

### 串口调试模式
- 自动刷新可用串口列表（2秒轮询）
- 支持 USB 转串口、蓝牙串口等
- 波特率：300 ~ 921600 预设值 + 自定义值 (1-9999999)
- 数据位：5, 6, 7, 8 / 停止位：1, 1.5, 2
- 校验位：None, Even, Odd, Mark, Space
- 流控：无 / 硬件 (RTS/CTS) / 软件 (XON/XOFF)
- DTR/RTS 手动置位控制
- CTS/DSR/DCD/RI 引脚电平实时监视
- 自动应答（关键字匹配 + 延迟配置）

### 虚拟串口模式（仅 Linux）
- 基于 `socat` 一键创建虚拟串口对
- 外部程序通过 `/tmp/mousart_vport` 连接
- 独立的收发区域和统计信息

### 数据收发
- 文本 / HEX 发送模式切换
- 多编码支持：UTF-8, GBK, GB18030, Latin-1, ASCII
- 发送换行控制（CR / LF 独立开关）
- 定时发送（1ms ~ 3600000ms）
- 文件发送
- Modbus RTU 帧构建器（自动 CRC）
- 快捷命令栏（左键发送，右键编辑）
- Ctrl+Enter 快捷键发送

### 数据分析
- 校验和计算：Sum8 / XOR8 / CRC16-Modbus / CRC32
- 二进制 / 十进制 / 十六进制进制转换
- 文本 ↔ Hex 实时转换
- 关键字 / 正则表达式过滤

### 数据记录
- 一键保存日志到 TXT / CSV / HEX
- 自动录制（10MB/文件自动分割）
- 实时 RX/TX 字节计数和速率显示
- 可配置日志缓存上限（1000~100000 条）
- 导出文件自动附带串口参数元信息

### 波形显示
- UART 串口协议波形（起始位 + 数据位 + 停止位）
- 点击日志条目弹出波形窗口（支持滚轮缩放、拖拽平移）
- 实时接收数据波形显示（工具栏「波形」按钮）

### 界面
- 5 套内置主题（深色、浅色、Solarized、Monokai、高对比）
- 0.8x-2.0x 字体缩放
- 窗口布局自动保存与恢复
- 侧边栏可折叠
- 配置管理（Profile）

### 兼容性
- Linux 权限自动检测（dialout 组引导提示）
- socat 依赖自动检测（对应发行版安装命令）
- 编码自动识别（UTF-8/GBK 启发式检测）
- PyQt5/PyQt6 双版本兼容

---

## 安装教程

### Linux (Debian/Ubuntu)

#### 方法一：deb 包安装（推荐）

```bash
# 1. 下载 deb 包
wget https://github.com/kryntx/MOUSART/releases/download/v3.1.0/mouserial_3.1.0-1_amd64.deb

# 2. 安装（自动安装依赖）
sudo apt install ./mouserial_3.1.0-1_amd64.deb

# 3. 运行
mousart
```

#### 方法二：从源码运行

```bash
# 1. 安装系统依赖
sudo apt update
sudo apt install python3-pyqt6 python3-serial socat git

# 2. 克隆项目
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. 运行
python3 -m mousart
```

#### 方法三：pip 安装依赖后运行

```bash
# 1. 安装系统依赖
sudo apt install socat

# 2. 安装 Python 依赖
pip3 install PyQt6 pyserial

# 3. 克隆并运行
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### 方法一：从源码运行

```bash
# 1. 安装 Python 3.10+（从 python.org 下载）

# 2. 安装依赖
pip install PyQt5 pyserial

# 3. 克隆项目并运行
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### 方法二：构建 EXE

```bash
# 1. 安装依赖
pip install PyQt5 pyserial pyinstaller

# 2. 构建
pyinstaller pyinstaller.spec --noconfirm

# 3. 运行生成的 dist/MOUSART.exe
```

---

## 卸载教程

### Linux deb 包卸载

```bash
# 方法一：使用 apt 卸载
sudo apt remove mouserial

# 方法二：完全卸载（包括配置文件）
sudo apt purge mouserial

# 清理用户配置（可选）
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Linux 源码安装卸载

```bash
# 删除项目目录
rm -rf /path/to/MOUSART

# 清理用户配置（可选）
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Windows 卸载

```
# 删除项目目录即可

# 清理用户配置（可选）
# 删除 %USERPROFILE%\.mousart 目录
# 删除 %USERPROFILE%\mousart_logs 目录
```

---

## 使用指南

### 串口调试模式
1. 在左侧面板选择 **"串口调试"** 模式
2. 从下拉列表中选择串口
3. 配置串口参数（波特率、数据位、停止位、校验位、流控）
4. 点击 **"打开"** 建立连接
5. 在右侧发送区输入数据，点击 **"发送"** 或按 `Ctrl+Enter`
6. 接收区实时显示收到的数据

### 虚拟串口模式（仅 Linux）
1. 在左侧面板选择 **"模拟串口"** 模式
2. 点击 **"启动"** 创建虚拟串口对
3. 界面显示外部端口路径 `/tmp/mousart_vport`
4. 使用任意串口工具连接到此路径
5. 在发送区输入数据并发送

### 快捷命令
1. 点击底部快捷命令栏的 **"+"** 添加新命令
2. 输入名称和数据（支持文本和 HEX）
3. 左键点击命令按钮立即发送
4. 右键点击命令按钮编辑或删除

### 自动应答（串口调试模式）
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

### 引脚控制（串口调试模式）
1. 打开串口后，左侧面板显示引脚控制栏
2. 点击 DTR/RTS 按钮切换引脚电平
3. CTS/DSR/DCD/RI 状态灯实时显示

---

## 常见问题

**Q: 无法打开串口？**
A: 通常是权限问题。v3.1.0 会自动检测并弹出引导对话框，也可手动修复：
```bash
sudo usermod -aG dialout $USER
# 注销并重新登录生效
```

**Q: 虚拟串口无法使用？**
A: v3.1.0 会自动检测 socat 并显示安装命令。也可手动安装：
```bash
sudo apt install socat
```

**Q: 中文显示乱码？**
A: 在左侧面板选择正确的接收编码（如 GBK）。

**Q: 如何发送 Modbus 命令？**
A: 点击 **"Modbus"** 按钮，填写参数后点击 **"构建"**，帧数据会自动填入发送区。

**Q: 自动录制的文件保存在哪里？**
A: 默认保存在 `~/mousart_logs/`，文件名格式为 `mousart_rec_YYYYMMDD_HHmmss.log`。

---

## 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE)。

**MOUSART** - 让串口调试更简单、更高效！
