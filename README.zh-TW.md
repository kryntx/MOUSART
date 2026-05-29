# MOUSART
## 全功能串列埠偵錯工具

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-PyQt6%20%7C%20Python-green)](https://www.riverbankcomputing.com/software/pyqt/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

**MOUSART** 是一款基於 Python/PyQt6 構建的全功能串列埠偵錯工具，專為嵌入式開發、硬體偵錯和串列通訊場景設計。v3.0 為完全重構版本，採用 Python 重寫，支援 Windows 和 Linux 雙平臺，包含自動應答、Modbus 協定支援、快捷命令、資料錄製與匯出、腳位控制、多編碼支援等數十項專業功能。

---

## 功能總覽

### 一、串列埠連線管理
- 自動重新整理可用串列埠列表（2秒輪詢）
- 支援虛擬串列埠、USB轉串列埠、藍牙串列埠
- 波特率：300 ~ 921600 預設值 + 自訂值 (1-9999999)
- 資料位元：5, 6, 7, 8 / 停止位元：1, 1.5, 2
- 同位元：None, Even, Odd, Mark, Space
- 流量控制：無 / 硬體 (RTS/CTS) / 軟體 (XON/XOFF)
- DTR/RTS 手動設定控制
- CTS/DSR/DCD/RI 腳位電平即時監視

### 二、資料接收
- 文字模式（UTF-8 / GBK / GB18030 / Latin-1 / ASCII 編碼可選）
- 十六進位 (HEX) 顯示模式
- 時間戳記顯示（精確到毫秒 hh:mm:ss.zzz）
- 資料方向標識（`<<` RX / `>>` TX / `!!` ERR）
- 暫停顯示（背景仍接收，介面不重新整理）
- 關鍵字過濾（一般文字 / 正規表示式）
- 日誌條目上限 2000 條，自動捲動

### 三、資料傳送
- 文字 / HEX 傳送模式切換
- 傳送換行控制（CR / LF 獨立開關）
- 定時傳送（1ms ~ 3600000ms 可調，支援次數限制）
- 檔案傳送（選擇任意檔案傳送原始內容）
- 傳送回顯控制
- Modbus RTU 幀構建器（位址/功能碼/起始位址/數量，自動 CRC）
- 快捷命令列（可新增/編輯/刪除，左鍵傳送，右鍵編輯，持久化儲存）
- 傳送序列/佇列（按順序依序傳送多筆資料，支援迴圈）
- Ctrl+Enter 快速鍵傳送

### 四、自動應答
- 收到特定關鍵字時自動傳送預設資料
- 支援設定應答延遲（毫秒級）
- 一鍵啟用/停用，規則持久化儲存

### 五、編碼與轉換工具
- 文字 ↔ Hex 即時轉換
- 多編碼支援：UTF-8, GBK, GB18030, Latin-1, ASCII
- 特殊字元轉義/反轉義（`\r\n`, `\x00` 等）
- 校驗和計算：Sum8 / XOR8 / CRC16-Modbus / CRC32
- Modbus RTU 幀構建與解析
- 二進位 / 十進位 / 十六進位進制轉換

### 六、資料記錄與匯出
- 一鍵儲存日誌到 TXT / CSV 檔案
- 自動錄製功能（帶檔案大小自動分割，10MB/檔案）
- 即時 RX/TX 位元組計數和速率顯示 (B/s, KB/s, MB/s)

### 七、虛擬串列埠（僅 Linux）
- 基於 `socat` 一鍵建立虛擬串列埠對
- 自動發現多實例建立的虛擬串列埠
- 外部程式透過 `/tmp/mousart_vport` 連線

### 八、介面與設定
- 內建深色/淺色雙主題，平滑切換
- 0.8x-1.5x 連續字體縮放
- 設定管理：儲存/載入/切換多套設定（Profile）

---

---

## 快速開始

### 預建構版本

從 [GitHub Releases](https://github.com/kryntx/MOUSART/releases) 下載：

| 平台 | 下載檔案 | 大小 |
|------|---------|------|
| **Linux x86_64 (deb)** | `mouserial_3.0.0-1_amd64.deb` | ~82KB |
| **Windows x86_64** | `MOUSART-v3.0.0-windows-x86_64.exe` | ~23MB |

#### Debian/Ubuntu 安裝（推薦）
```bash
# 下載並安裝 deb 套件（自動處理依賴）
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb
sudo apt install ./mouserial_3.0.0-1_amd64.deb
```

> Windows 版本為單檔 exe，雙擊即可執行，無需安裝。

### 從原始碼建構

```bash
# Ubuntu/Debian 依賴安裝
sudo apt update
sudo apt install python3-pyqt6 python3-serial socat

# 複製專案
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 安裝 Python 依賴
pip3 install PyQt6 pyserial

# 執行
python3 -m mousart
```

#### 建構 Windows EXE

```bash
pip3 install pyinstaller
pyinstaller pyinstaller.spec --noconfirm
# 輸出: dist/MOUSART.exe
```

#### 建構 Debian 套件

```bash
sudo apt install dh-python python3-setuptools debhelper
dpkg-buildpackage -us -uc -b
```

---

## 使用指南

### 虛擬串列埠模式
1. 在左側面板切換到 **「模擬串列埠」** 模式
2. 點擊 **「啟動」** 按鈕建立虛擬串列埠
3. 介面顯示外部埠路徑 `/tmp/mousart_vport`
4. 使用任意串列埠工具連線到此路徑
5. 在傳送區輸入資料並點擊 **「傳送」** 或按 `Ctrl+Enter`

### 硬體串列偵錯模式
1. 切換到 **「串列偵錯」** 模式
2. 從下拉列表中選擇串列埠
3. 設定串列埠參數：波特率、資料位元、停止位元、同位元、流量控制
4. 點擊 **「開啟」** 建立連線
5. 在傳送區輸入資料並傳送

### 快捷命令
1. 在底部快捷命令列點擊 **「+」** 新增命令
2. 輸入名稱和資料（支援文字和 HEX）
3. 左鍵點擊命令按鈕立即傳送
4. 右鍵點擊命令按鈕編輯或刪除

### 自動應答
1. 在左側面板找到 **「自動應答」** 區域
2. 啟用開關，設定匹配關鍵字和應答資料
3. 可選設定應答延遲（毫秒）

### Modbus 幀構建
1. 在傳送工具列點擊 **「Modbus」** 按鈕
2. 設定從站位址、功能碼、起始位址、數量
3. 點擊 **「構建」** 自動產生帶 CRC 的 Modbus RTU 幀

### 日誌錄製與匯出
1. 點擊接收區工具列的 **「錄製」** 按鈕開始自動錄製
2. 所有收發資料自動儲存到 `~/mousart_logs/`
3. 點擊 **「儲存」** 可手動匯出為 TXT 或 CSV

### 腳位控制
1. 開啟串列埠後，左側面板顯示腳位控制列
2. 點擊 DTR/RTS 按鈕切換腳位電平
3. CTS/DSR/DCD/RI 狀態燈即時顯示

### 設定管理
1. 在左側面板底部找到 **「設定 Profile」** 區域
2. 點擊 **「儲存」** 儲存當前設定
3. 下拉列表切換不同的 Profile

---

## 串列埠參數

| 參數 | 可選值 |
|------|--------|
| **波特率** | 300 ~ 921600 預設 + 自訂 (1-9999999) |
| **資料位元** | 5, 6, 7, 8 |
| **停止位元** | 1, 1.5, 2 |
| **同位元** | None, Odd, Even, Mark, Space |
| **流量控制** | None, Hardware, Software |
| **接收編碼** | UTF-8, GBK, GB18030, Latin-1, ASCII |
| **定時傳送間隔** | 1 - 3600000 ms |

---

## 專案結構

```
MOUSART/
├── pyproject.toml                   # Python 專案設定
├── pyinstaller.spec                 # PyInstaller 打包設定
├── Makefile                         # 建構自動化
├── scripts/                         # 建構腳本
│   ├── build_exe.sh                 # Windows EXE 建構
│   ├── build_deb.sh                 # Debian 套件建構
│   └── build_icons.sh              # 圖示生成
├── resources/icons/                 # 應用圖示
│   ├── mousart.svg                  # 原始 SVG 圖示
│   └── mousart_*.png               # 各尺寸 PNG
├── mousart/                         # Python 原始碼
│   ├── __main__.py                  # 進入點
│   ├── app.py                       # 應用啟動
│   ├── core/                        # 核心模組
│   │   ├── theme_manager.py         # 主題管理
│   │   ├── serial_manager.py        # 串列 I/O、腳位、自動應答
│   │   ├── virtual_serial_manager.py # 虛擬串列埠
│   │   ├── config_manager.py        # 設定管理、Profile
│   │   ├── data_analyzer.py         # 編碼、校驗和、Modbus
│   │   └── log_file_manager.py      # 日誌儲存、匯出
│   ├── ui/                          # 介面模組
│   │   ├── main_window.py           # 主視窗
│   │   ├── title_bar.py             # 標題列
│   │   ├── settings_panel.py        # 左側設定面板
│   │   ├── data_panel.py            # 右側資料面板
│   │   ├── widgets/                 # 可複用元件
│   │   └── dialogs/                 # 對話框
│   └── utils/                       # 工具模組
│       ├── constants.py             # 常數定義
│       ├── encoding.py              # 編碼轉換
│       ├── checksum.py              # 校驗和計算
│       ├── modbus.py                # Modbus 幀構建/解析
│       ├── number_convert.py        # 進制轉換
│       ├── hex_display.py           # HEX 顯示格式化
│       └── stylesheet.py            # QSS 樣式生成
└── debian/                          # Debian 打包設定
```

---

## 更新日誌

### v3.0.0 (2026-05-29)
**完全重構 - Python/PyQt6 版本**

- 完全使用 Python 重寫，從 C++/Qt5/QML 遷移到 Python/PyQt6
- 更簡潔的程式碼結構，更易於維護和擴展
- 保持所有 v2.0.0 功能完整
- 最佳化跨平臺支援（Windows EXE + Linux deb）
- 新增應用圖示設計

### v2.0.0 (2026-05-29)
**重大功能更新**

新增：腳位控制、自動應答、快捷命令列、多編碼支援、傳送換行控制、檔案傳送、Modbus RTU 幀構建器與解析器、日誌儲存匯出、RX/TX 即時統計、資料過濾、設定管理、校驗和工具、傳送序列/佇列、傳送次數限制

改進：波特率預設擴展至 300-921600，日誌上限提升至 2000，虛擬串列埠新增編碼和統計支援

### v1.0.0 (2026-05-27)
- 初始發布

---

## 常見問題

**Q: 無法開啟串列埠？** 通常是權限問題，使用 `sudo python3 -m mousart` 或將使用者新增到 `dialout` 群組。

**Q: 虛擬串列埠無法使用？** 請確保已安裝 `socat`：`sudo apt install socat`

**Q: 中文顯示亂碼？** 在左側面板選擇正確的接收編碼（如 GBK）。

---

## 授權條款

本專案採用 **MIT 授權條款** - 詳見 [LICENSE](LICENSE)。

**MOUSART** - 讓串列偵錯更簡單、更高效！
