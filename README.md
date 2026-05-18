# MOUSART
## 现代串口调试工具 | Modern Serial Port Debugger

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-blue)](https://www.linux.org/)
[![Toolchain](https://img.shields.io/badge/toolchain-Qt5%20%7C%20CMake-green)](https://www.qt.io/)
[![C++](https://img.shields.io/badge/C%2B%2B-17-blue)](https://isocpp.org/)

**MOUSART** 是一款基于 Qt5/QML 构建的现代化串口调试工具，专为嵌入式开发、硬件调试和串口通信场景设计。它不仅支持传统的硬件串口调试，还集成了强大的虚拟串口功能，让您在没有实际硬件的情况下也能进行串口通信测试。

---

## 核心特性

### 虚拟串口支持
- 一键创建虚拟串口对，无需额外安装复杂工具
- 基于 `socat` 实现，稳定可靠
- 自动发现多实例创建的虚拟串口
- 外部程序可通过 `/tmp/mousart_vport` 连接
- 支持多实例间直接通信

### 专业串口调试
- 完整的串口参数配置：波特率、数据位、停止位、校验位、流控制
- 波特率支持 1200-921600 预设值及 1-9999999 自定义值
- 独立的接收日志区和发送输入区
- 支持实时数据监控和历史记录查看

### 十六进制模式
- 一键切换接收数据的十六进制/ASCII显示
- 支持十六进制格式数据发送
- 自动解析十六进制字符串，支持空格分隔

### 现代化界面
- 内置深色/浅色双主题，平滑切换
- 主题和设置自动持久化保存
- 0.8x-1.5x 连续字体缩放
- 自定义无边框窗口，支持拖拽移动、双击最大化和边缘调整大小
- 精心设计的控件和视觉效果

---

## 截图

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 串口调试界面">
  <br>
  <em>MOUSART 串口调试界面（深色主题）</em>
</div>
<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 虚拟串口界面">
  <br>
  <em>MOUSART 虚拟串口界面（深色主题）</em>
</div>

---

## 快速开始

### 预构建版本
目前项目尚未发布预构建版本，请从源码编译使用。

### 从源码构建

#### 系统要求
- Qt 5 (Core, Gui, Qml, Quick, Widgets, SerialPort)
- CMake >= 3.16
- C++17 兼容编译器
- socat (仅虚拟串口功能需要)

#### Ubuntu/Debian 依赖安装
```bash
sudo apt update
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat
```

#### 编译步骤
```bash
# 克隆仓库
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 创建构建目录并编译
cmake -B build
cmake --build build

# 运行程序
./build/MOUSART

# 如遇串口权限问题，使用sudo运行
sudo ./build/MOUSART
```

---

## 使用指南

### 虚拟串口模式
1. 在左侧面板切换到 **"模拟串口 Virtual"** 模式
2. 点击 **"启动 Start"** 按钮创建虚拟串口
3. 界面将显示外部端口路径 `/tmp/mousart_vport`
4. 使用任意串口工具连接到此路径
5. 外部程序发送的数据将显示在接收区
6. 在发送区输入数据并点击 **"发送 Send"** 或按 `Ctrl+Enter`
7. 点击 **"停止 Stop"** 关闭虚拟串口

### 硬件串口调试模式
1. 在左侧面板切换到 **"串口调试 Debug"** 模式
2. 从下拉列表中选择要连接的串口
3. 配置串口参数：波特率、数据位、停止位、校验位、流控制
4. 点击 **"打开 Open"** 建立连接
5. 在发送区输入数据并发送
6. 接收区将实时显示接收到的数据
7. 点击 **"关闭 Close"** 断开连接

### 多实例通信
1. 打开两个 MOUSART 窗口
2. 在第一个窗口中启动虚拟串口
3. 第二个窗口将自动在串口列表中发现 `/tmp/mousart_vport`
4. 在第二个窗口中选择此虚拟串口并打开
5. 两个窗口之间即可互相发送和接收数据

---

## 串口参数配置

| 参数 | 可选值 |
|------|--------|
| **波特率** | 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600<br>或自定义值 (1 - 9999999) |
| **数据位** | 5, 6, 7, 8 |
| **停止位** | 1, 1.5, 2 |
| **校验位** | None, Odd, Even, Mark, Space |
| **流控制** | None, Hardware (RTS/CTS), Software (XON/XOFF) |

---

## 项目结构

```
MOUSART/
├── CMakeLists.txt          # CMake 构建配置
├── qml.qrc                 # QML 资源文件
├── img/                    # 项目截图和图片资源
│   └── d1.png              # 主界面截图
├── src/                    # C++ 源代码
│   ├── main.cpp            # 程序入口点
│   └── core/               # 核心功能模块
│       ├── thememanager.h/.cpp     # 主题和字体缩放管理
│       ├── serialportmanager.h/.cpp # 硬件串口I/O管理
│       └── virtualserialmanager.h/.cpp # 虚拟串口管理(基于socat)
└── qml/                    # QML 界面代码
    ├── main.qml            # 主窗口(无边框)
    ├── TitleBar.qml        # 标题栏(主题/字体控制)
    ├── SettingsPanel.qml   # 左侧设置面板(模式+串口配置)
    ├── DataPanel.qml       # 右侧数据面板(日志+发送)
    └── components/         # 可复用QML组件
        ├── WindowButton.qml
        ├── ModeButton.qml
        ├── ActionButton.qml
        ├── StyledComboBox.qml
        ├── EditableComboBox.qml
        ├── SmallButton.qml
        └── SmallToggle.qml
```

---

## 常见问题

### Q: 为什么我无法打开串口？
A: 这通常是权限问题。尝试使用 `sudo ./build/MOUSART` 运行程序，或者将当前用户添加到 `dialout` 组：
```bash
sudo usermod -aG dialout $USER
```
注销并重新登录后生效。

### Q: 虚拟串口功能无法使用？
A: 请确保已安装 `socat` 工具。在 Ubuntu/Debian 上可以通过以下命令安装：
```bash
sudo apt install socat
```

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