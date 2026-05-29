# MOUSART
## フル機能シリアルポートデバッグツール

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)

**MOUSART** は、組込み開発、ハードウェアデバッグ、シリアル通信のシナリオに設計されたフル機能シリアルポートデバッグツールです。シリアルデバッグとバーチャルシリアルポートの2つの独立したモードをサポートし、自動応答、Modbus プロトコルサポート、クイックコマンド、データの記録とエクスポート、ピン制御、複数エンコーディング対応など数十の専門機能を備えています。

---

## スクリーンショット

### シリアルデバッグモード

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART シリアルデバッグ画面">
  <br>
  <em>シリアルデバッグモード - 実際のハードウェアシリアルポートに接続してデータ送受信</em>
</div>

### バーチャルシリアルポートモード

<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART バーチャルシリアルポート画面">
  <br>
  <em>バーチャルシリアルポートモード - 外部プログラム接続用のバーチャルシリアルポートペアを作成</em>
</div>

---

## 機能一覧

### シリアルデバッグモード
- 利用可能なシリアルポートリストの自動更新（2秒間隔ポーリング）
- USB-シリアル変換、Bluetooth シリアルポート対応
- ボーレート：300 ~ 921600 プリセット値 + カスタム値 (1-9999999)
- データビット：5, 6, 7, 8 / ストップビット：1, 1.5, 2
- パリティ：None, Even, Odd, Mark, Space
- フロー制御：なし / ハードウェア (RTS/CTS) / ソフトウェア (XON/XOFF)
- DTR/RTS 手動セット制御
- CTS/DSR/DCD/RI ピンレベルリアルタイム監視
- 自動応答（キーワード一致 + 遅延設定）

### バーチャルシリアルポートモード（Linux のみ）
- `socat` ベースのワンクリックバーチャルシリアルポートペア作成
- 外部プログラムは `/tmp/mousart_vport` を介して接続
- 独立した送受信エリアと統計情報

### データ送受信
- テキスト / HEX 送信モード切替
- 複数エンコーディング対応：UTF-8, GBK, GB18030, Latin-1, ASCII
- 送信改行制御（CR / LF 個別スイッチ）
- タイマー送信（1ms ~ 3600000ms）
- ファイル送信
- Modbus RTU フレームビルダー（自動 CRC）
- クイックコマンドバー（左クリック送信、右クリック編集）
- Ctrl+Enter ショートカット送信

### データ分析
- チェックサム計算：Sum8 / XOR8 / CRC16-Modbus / CRC32
- 2進数 / 10進数 / 16進数変換
- テキスト ↔ Hex リアルタイム変換
- キーワード / 正規表現フィルタ

### データ記録
- ワンクリックでログを TXT / CSV に保存
- 自動記録（10MB/ファイル自動分割）
- リアルタイム RX/TX バイトカウントとレート表示

### インターフェース
- ダーク/ライトデュアルテーマ
- 0.8x-1.5x フォントスケーリング
- プロファイル管理

---

## インストールガイド

### Linux (Debian/Ubuntu)

#### 方法1：deb パッケージインストール（推奨）

```bash
# 1. deb パッケージをダウンロード
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb

# 2. インストール（依存関係を自動インストール）
sudo apt install ./mouserial_3.0.0-1_amd64.deb

# 3. 実行
mousart
```

#### 方法2：ソースコードから実行

```bash
# 1. システム依存関係をインストール
sudo apt update
sudo apt install python3-pyqt5 python3-serial socat git

# 2. プロジェクトをクローン
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. 実行
python3 -m mousart
```

#### 方法3：pip で依存関係をインストール後実行

```bash
# 1. システム依存関係をインストール
sudo apt install socat

# 2. Python 依存関係をインストール
pip3 install PyQt5 pyserial

# 3. クローンして実行
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### 方法1：ソースコードから実行

```bash
# 1. Python 3.10+ をインストール（python.org からダウンロード）

# 2. 依存関係をインストール
pip install PyQt5 pyserial

# 3. プロジェクトをクローンして実行
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### 方法2：EXE をビルド

```bash
# 1. 依存関係をインストール
pip install PyQt5 pyserial pyinstaller

# 2. ビルド
pyinstaller pyinstaller.spec --noconfirm

# 3. 生成された dist/MOUSART.exe を実行
```

---

## アンインストールガイド

### Linux deb パッケージのアンインストール

```bash
# 方法1：apt を使用してアンインストール
sudo apt remove mouserial

# 方法2：完全アンインストール（設定ファイル含む）
sudo apt purge mouserial

# ユーザー設定をクリーンアップ（オプション）
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Linux ソースインストールのアンインストール

```bash
# プロジェクトディレクトリを削除
rm -rf /path/to/MOUSART

# ユーザー設定をクリーンアップ（オプション）
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Windows のアンインストール

```
# プロジェクトディレクトリを削除するだけ

# ユーザー設定をクリーンアップ（オプション）
# %USERPROFILE%\.mousart ディレクトリを削除
# %USERPROFILE%\mousart_logs ディレクトリを削除
```

---

## 使い方ガイド

### シリアルデバッグモード
1. 左側パネルで **「シリアルデバッグ」** モードを選択
2. ドロップダウンリストからシリアルポートを選択
3. シリアルポートパラメータを設定（ボーレート、データビット、ストップビット、パリティ、フロー制御）
4. **「開く」** をクリックして接続を確立
5. 右側の送信エリアに入力し、**「送信」** をクリックするか `Ctrl+Enter` を押す
6. 受信エリアにデータがリアルタイムで表示される

### バーチャルシリアルポートモード（Linux のみ）
1. 左側パネルで **「シミュレーションシリアルポート」** モードを選択
2. **「起動」** をクリックしてバーチャルシリアルポートペアを作成
3. 画面に外部ポートパス `/tmp/mousart_vport` が表示される
4. 任意のシリアルツールでこのパスに接続
5. 送信エリアに入力して送信

### クイックコマンド
1. 画面下部のクイックコマンドバーの **「+」** をクリックして新しいコマンドを追加
2. 名前とデータを入力（テキストと HEX に対応）
3. コマンドボタンを左クリックで即時送信
4. コマンドボタンを右クリックで編集または削除

### 自動応答（シリアルデバッグモード）
1. 左側パネルの **「自動応答」** エリアを見つける
2. スイッチを有効にし、一致キーワードと応答データを設定
3. 応答遅延を設定可能（ミリ秒）

### Modbus フレーム構築
1. 送信ツールバーの **「Modbus」** ボタンをクリック
2. スレーブアドレス、ファンクションコード、開始アドレス、数量を設定
3. **「構築」** をクリックすると CRC 付きの Modbus RTU フレームが自動生成される

### ログ記録とエクスポート
1. 受信エリアのツールバーの **「記録」** ボタンをクリックして自動記録を開始
2. すべての送受信データが `~/mousart_logs/` に自動保存される
3. **「保存」** をクリックすると TXT または CSV に手動エクスポートできる

### ピン制御（シリアルデバッグモード）
1. シリアルポートを開くと、左側パネルにピン制御バーが表示される
2. DTR/RTS ボタンをクリックしてピンレベルを切り替え
3. CTS/DSR/DCD/RI ステータスランプがリアルタイムで表示される

---

## よくある質問

**Q: シリアルポートを開けませんか？**
A: 通常は権限の問題です。ユーザーを `dialout` グループに追加してください：
```bash
sudo usermod -aG dialout $USER
# ログアウトして再ログインすると有効になります
```

**Q: バーチャルシリアルポートが使えませんか？**
A: `socat` がインストールされていることを確認してください：
```bash
sudo apt install socat
```

**Q: 中国語の表示が文字化けしますか？**
A: 左側パネルで正しい受信エンコーディング（例：GBK）を選択してください。

**Q: Modbus コマンドを送信するには？**
A: **「Modbus」** ボタンをクリックし、パラメータを入力して **「構築」** をクリックすると、フレームデータが自動的に入力されます。

**Q: 自動記録ファイルの保存場所は？**
A: デフォルトでは `~/mousart_logs/` に保存され、ファイル名の形式は `mousart_rec_YYYYMMDD_HHmmss.log` です。

---

## ライセンス

本プロジェクトは **MIT ライセンス** を採用しています - 詳細は [LICENSE](LICENSE) をご覧ください。

**MOUSART** - シリアルデバッグをもっとシンプルに、もっと効率的に！
