# MOUSART
## 全功能串列埠偵錯工具

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v2.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-Qt5%20%7C%20CMake-green)](https://www.qt.io/)
[![C++](https://img.shields.io/badge/C%2B%2B-17-blue)](https://isocpp.org/)

**MOUSART** 是一款基於 Qt5/QML 構建的全功能串列埠偵錯工具，專為嵌入式開發、硬體偵錯和串列通訊場景設計。v2.0 新增了自動應答、Modbus 協定支援、快捷命令、資料錄製與匯出、腳位控制、多編碼支援等數十項專業功能。

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

## 截圖

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 串列偵錯介面">
  <br>
  <em>MOUSART 串列偵錯介面（淺色主題）</em>
</div>
<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART 虛擬串列埠介面">
  <br>
  <em>MOUSART 虛擬串列埠介面（淺色主題）</em>
</div>

---

## 快速開始

### 預建構版本

從 [GitHub Releases](https://github.com/kryntx/MOUSART/releases) 下載：

| 平台 | 下載檔案 | 大小 |
|------|---------|------|
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | ~105KB |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | ~23MB |

> Windows 版本已包含所有執行時依賴，解壓縮即可執行。

### 從原始碼建構

```bash
# Ubuntu/Debian 依賴安裝
sudo apt update
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat

# 複製並編譯
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# 執行
./build/MOUSART
```

#### Windows 交叉編譯

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
├── CMakeLists.txt                   # CMake 建構設定
├── qml.qrc                          # QML 資源檔案
├── cmake/                           # 交叉編譯工具鏈
├── img/                             # 截圖
├── src/                             # C++ 原始碼
│   ├── main.cpp                     # 進入點
│   └── core/                        # 核心模組
│       ├── thememanager.h/.cpp      # 主題管理
│       ├── serialportmanager.h/.cpp # 串列 I/O、腳位、自動應答、統計
│       ├── virtualserialmanager.h/.cpp # 虛擬串列埠
│       ├── configmanager.h/.cpp     # 設定管理、Profile
│       ├── dataanalyzer.h/.cpp      # 編碼、校驗和、Modbus
│       └── logfilemanager.h/.cpp    # 日誌儲存、匯出
└── qml/                             # QML 介面
    ├── main.qml                     # 主視窗
    ├── TitleBar.qml                 # 標題列
    ├── SettingsPanel.qml            # 左側設定面板
    ├── DataPanel.qml                # 右側資料面板
    └── components/                  # 可複用元件
```

---

## 更新日誌

### v2.0.0 (2026-05-29)
**重大功能更新**

新增：腳位控制、自動應答、快捷命令列、多編碼支援、傳送換行控制、檔案傳送、Modbus RTU 幀構建器與解析器、日誌儲存匯出、RX/TX 即時統計、資料過濾、設定管理、校驗和工具、傳送序列/佇列、傳送次數限制

改進：波特率預設擴展至 300-921600，日誌上限提升至 2000，虛擬串列埠新增編碼和統計支援

### v1.0.0 (2026-05-27)
- 初始發布

---

## 常見問題

**Q: 無法開啟串列埠？** 通常是權限問題，使用 `sudo` 或將使用者新增到 `dialout` 群組。

**Q: 虛擬串列埠無法使用？** 請確保已安裝 `socat`：`sudo apt install socat`

**Q: 中文顯示亂碼？** 在左側面板選擇正確的接收編碼（如 GBK）。

---

## 授權條款

本專案採用 **MIT 授權條款** - 詳見 [LICENSE](LICENSE)。

**MOUSART** - 讓串列偵錯更簡單、更高效！
