# MOUSART
## 全功能序列埠偵錯工具

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)

**MOUSART** 是一款全功能序列埠偵錯工具，專為嵌入式開發、硬體偵錯和序列埠通訊場景設計。支援序列埠偵錯和虛擬序列埠兩種獨立模式，具備自動應答、Modbus 協定支援、快捷命令、資料錄製與匯出、腳位控制、多編碼支援等數十項專業功能。

---

## 截圖

### 序列埠偵錯模式

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 序列埠偵錯介面">
  <br>
  <em>序列埠偵錯模式 - 連接真實硬體序列埠進行資料收發</em>
</div>

### 虛擬序列埠模式

<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART 虛擬序列埠介面">
  <br>
  <em>虛擬序列埠模式 - 建立虛擬序列埠對供外部程式連接</em>
</div>

---

## 功能特性

### 序列埠偵錯模式
- 自動重新整理可用序列埠列表（2秒輪詢）
- 支援 USB 轉序列埠、藍牙序列埠等
- 波特率：300 ~ 921600 預設值 + 自訂值 (1-9999999)
- 資料位元：5, 6, 7, 8 / 停止位元：1, 1.5, 2
- 同位元：None, Even, Odd, Mark, Space
- 流量控制：無 / 硬體 (RTS/CTS) / 軟體 (XON/XOFF)
- DTR/RTS 手動置位控制
- CTS/DSR/DCD/RI 腳位電位即時監視
- 自動應答（關鍵字匹配 + 延遲設定）

### 虛擬序列埠模式（僅限 Linux）
- 基於 `socat` 一鍵建立虛擬序列埠對
- 外部程式透過 `/tmp/mousart_vport` 連接
- 獨立的收發區域和統計資訊

### 資料收發
- 文字 / HEX 傳送模式切換
- 多編碼支援：UTF-8, GBK, GB18030, Latin-1, ASCII
- 傳送換行控制（CR / LF 獨立開關）
- 定時傳送（1ms ~ 3600000ms）
- 檔案傳送
- Modbus RTU 幀構建器（自動 CRC）
- 快捷命令列（左鍵傳送，右鍵編輯）
- Ctrl+Enter 快捷鍵傳送

### 資料分析
- 校驗和計算：Sum8 / XOR8 / CRC16-Modbus / CRC32
- 二進位 / 十進位 / 十六進位進制轉換
- 文字 ↔ Hex 即時轉換
- 關鍵字 / 正規表示式過濾

### 資料記錄
- 一鍵儲存紀錄檔至 TXT / CSV
- 自動錄製（10MB/檔案自動分割）
- 即時 RX/TX 位元組計數和速率顯示

### 介面
- 深色/淺色雙主題
- 0.8x-1.5x 字型縮放
- 設定檔管理（Profile）

---

## 安裝教學

### Linux (Debian/Ubuntu)

#### 方法一：deb 套件安裝（推薦）

```bash
# 1. 下載 deb 套件
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb

# 2. 安裝（自動安裝相依套件）
sudo apt install ./mouserial_3.0.0-1_amd64.deb

# 3. 執行
mousart
```

#### 方法二：從原始碼執行

```bash
# 1. 安裝系統相依套件
sudo apt update
sudo apt install python3-pyqt5 python3-serial socat git

# 2. 複製專案
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. 執行
python3 -m mousart
```

#### 方法三：pip 安裝相依套件後執行

```bash
# 1. 安裝系統相依套件
sudo apt install socat

# 2. 安裝 Python 相依套件
pip3 install PyQt5 pyserial

# 3. 複製並執行
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### 方法一：從原始碼執行

```bash
# 1. 安裝 Python 3.10+（從 python.org 下載）

# 2. 安裝相依套件
pip install PyQt5 pyserial

# 3. 複製專案並執行
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### 方法二：建置 EXE

```bash
# 1. 安裝相依套件
pip install PyQt5 pyserial pyinstaller

# 2. 建置
pyinstaller pyinstaller.spec --noconfirm

# 3. 執行生成的 dist/MOUSART.exe
```

---

## 移除教學

### Linux deb 套件移除

```bash
# 方法一：使用 apt 移除
sudo apt remove mouserial

# 方法二：完全移除（包含設定檔）
sudo apt purge mouserial

# 清理使用者設定（可選）
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Linux 原始碼安裝移除

```bash
# 刪除專案目錄
rm -rf /path/to/MOUSART

# 清理使用者設定（可選）
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Windows 移除

```
# 刪除專案目錄即可

# 清理使用者設定（可選）
# 刪除 %USERPROFILE%\.mousart 目錄
# 刪除 %USERPROFILE%\mousart_logs 目錄
```

---

## 使用指南

### 序列埠偵錯模式
1. 在左側面板選擇 **「序列埠偵錯」** 模式
2. 從下拉式選單中選擇序列埠
3. 設定序列埠參數（波特率、資料位元、停止位元、同位元、流量控制）
4. 點擊 **「開啟」** 建立連線
5. 在右側傳送區輸入資料，點擊 **「傳送」** 或按 `Ctrl+Enter`
6. 接收區即時顯示收到的資料

### 虛擬序列埠模式（僅限 Linux）
1. 在左側面板選擇 **「模擬序列埠」** 模式
2. 點擊 **「啟動」** 建立虛擬序列埠對
3. 介面顯示外部連接埠路徑 `/tmp/mousart_vport`
4. 使用任意序列埠工具連接到此路徑
5. 在傳送區輸入資料並傳送

### 快捷命令
1. 點擊底部快捷命令列的 **「+」** 新增命令
2. 輸入名稱和資料（支援文字和 HEX）
3. 左鍵點擊命令按鈕立即傳送
4. 右鍵點擊命令按鈕編輯或刪除

### 自動應答（序列埠偵錯模式）
1. 在左側面板找到 **「自動應答」** 區域
2. 啟用開關，設定匹配關鍵字和應答資料
3. 可選設定應答延遲（毫秒）

### Modbus 幀構建
1. 在傳送工具列點擊 **「Modbus」** 按鈕
2. 設定從站位址、功能碼、起始位址、數量
3. 點擊 **「構建」** 自動生成帶 CRC 的 Modbus RTU 幀

### 紀錄錄製與匯出
1. 點擊接收區工具列的 **「錄製」** 按鈕開始自動錄製
2. 所有收發資料自動儲存到 `~/mousart_logs/`
3. 點擊 **「儲存」** 可手動匯出為 TXT 或 CSV

### 腳位控制（序列埠偵錯模式）
1. 開啟序列埠後，左側面板顯示腳位控制列
2. 點擊 DTR/RTS 按鈕切換腳位電位
3. CTS/DSR/DCD/RI 狀態燈即時顯示

---

## 常見問題

**Q: 無法開啟序列埠？**
A: 通常是權限問題，將使用者加入 `dialout` 群組：
```bash
sudo usermod -aG dialout $USER
# 登出並重新登入生效
```

**Q: 虛擬序列埠無法使用？**
A: 請確保已安裝 `socat`：
```bash
sudo apt install socat
```

**Q: 中文顯示亂碼？**
A: 在左側面板選擇正確的接收編碼（如 GBK）。

**Q: 如何傳送 Modbus 命令？**
A: 點擊 **「Modbus」** 按鈕，填寫參數後點擊 **「構建」**，幀資料會自動填入傳送區。

**Q: 自動錄製的檔案儲存在哪裡？**
A: 預設儲存在 `~/mousart_logs/`，檔案名稱格式為 `mousart_rec_YYYYMMDD_HHmmss.log`。

---

## 授權條款

本專案採用 **MIT 授權條款** - 詳見 [LICENSE](LICENSE)。

**MOUSART** - 讓序列埠偵錯更簡單、更高效！
