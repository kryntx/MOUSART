# MOUSART
## フル機能シリアルポートデバッガー

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **日本語** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-PyQt6%20%7C%20Python-green)](https://www.riverbankcomputing.com/software/pyqt/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

**MOUSART** は Python/PyQt6 で構築されたフル機能シリアルポートデバッガーです。組み込み開発、ハードウェアデバッグ、シリアル通信向けに設計されています。v3.0 は完全な Python 書き換え版であり、自動応答、Modbus プロトコルサポート、クイックコマンド、データ記録・エクスポート、ピン制御、マルチエンコーディング対応など多数のプロフェッショナル機能を追加しました。

---

## 機能概要

### 1. 接続管理
- 利用可能ポート一覧の自動更新（2秒間隔）
- 仮想シリアルポート、USB-シリアル、Bluetooth対応
- ボーレート：300〜921600 プリセット + カスタム (1-9999999)
- データビット：5, 6, 7, 8 / ストップビット：1, 1.5, 2
- パリティ：None, Even, Odd, Mark, Space
- フロー制御：なし / ハードウェア (RTS/CTS) / ソフトウェア (XON/XOFF)
- DTR/RTS 手動制御 / CTS/DSR/DCD/RI ピン状態監視

### 2. データ受信
- テキストモード（UTF-8 / GBK / GB18030 / Latin-1 / ASCII）
- 16進数 (HEX) 表示モード
- タイムスタンプ表示（ミリ秒精度）
- 方向インジケーター（`<<` RX / `>>` TX / `!!` ERR）
- 表示一時停止（バックグラウンドで受信継続）
- キーワードフィルター（テキスト / 正規表現）
- ログ上限 2000 件、自動スクロール

### 3. データ送信
- テキスト / HEX 送信モード切替
- 改行制御（CR / LF 個別切替）
- 定時送信（1ms〜3600000ms、回数制限対応）
- ファイル送信
- Modbus RTU フレームビルダー（CRC自動計算）
- クイックコマンドバー（追加/編集/削除、永続保存）
- 送信シーケンス/キュー（ループ対応）

### 4. 自動応答
- 特定キーワード受信時に自動応答
- 応答遅延設定（ミリ秒）
- ワンクリック有効/無効切替

### 5. エンコーディング・変換ツール
- テキスト ↔ Hex 変換
- マルチエンコーディング：UTF-8, GBK, GB18030, Latin-1, ASCII
- チェックサム：Sum8 / XOR8 / CRC16-Modbus / CRC32
- Modbus RTU フレーム構築・解析
- 2進数 / 10進数 / 16進数変換

### 6. データ記録・エクスポート
- ログの TXT / CSV 保存
- 自動記録（10MB でファイル分割）
- リアルタイム RX/TX バイトカウンター

### 7. 仮想シリアルポート（Linux のみ）
- `socat` ベースのワンクリック仮想ポート作成
- `/tmp/mousart_vport` 経由で外部プログラム接続

### 8. UI・設定
- ダーク/ライトテーマ
- 0.8x〜1.5x フォントスケーリング
- プロファイル管理（複数設定の保存/切替）

---

---

## クイックスタート

### ビルド済みバイナリ

[GitHub Releases](https://github.com/kryntx/MOUSART/releases) からダウンロード：

| プラットフォーム | ファイル | サイズ |
|-----------------|---------|--------|
| **Linux x86_64 (deb)** | `mouserial_3.0.0-1_amd64.deb` | ~82KB |
| **Windows x86_64** | `MOUSART-v3.0.0-windows-x86_64.exe` | ~23MB |

#### Debian/Ubuntu インストール（推奨）
```bash
# deb パッケージをダウンロードしてインストール（依存関係は自動処理）
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb
sudo apt install ./mouserial_3.0.0-1_amd64.deb
```

### ソースからビルド

```bash
# Ubuntu/Debian 依存パッケージ
sudo apt install python3-pyqt6 python3-serial socat

git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# Python 依存関係をインストール
pip3 install PyQt6 pyserial

# 実行
python3 -m mousart
```

#### Windows EXE をビルド

```bash
pip3 install pyinstaller
pyinstaller pyinstaller.spec --noconfirm
# 出力: dist/MOUSART.exe
```

#### Debian パッケージをビルド

```bash
sudo apt install dh-python python3-setuptools debhelper
dpkg-buildpackage -us -uc -b
```

---

## 使い方

### 仮想シリアルポートモード
1. 左パネルで **「Virtual」** モードを選択
2. **「Start」** をクリックして仮想ポートを作成
3. 外部ポートパス `/tmp/mousart_vport` が表示される
4. 任意のシリアルツールでこのパスに接続
5. データの送受信が可能

### ハードウェアシリアルデバッグモード
1. **「Debug」** モードを選択
2. ポートを選択してパラメータを設定
3. **「Open」** で接続
4. 送信エリアに入力して **「送信」** または `Ctrl+Enter`

### クイックコマンド
1. 下部のクイックコマンドバーで **「+」** をクリック
2. 名前とデータを入力
3. 左クリックで送信、右クリックで編集

### 自動応答
1. 左パネルの **「自動応答」** セクション
2. トグルを有効にしてキーワードと応答データを設定

### Modbus フレーム構築
1. 送信ツールバーの **「Modbus」** をクリック
2. スレーブアドレス、ファンクションコード、開始アドレス、数量を設定
3. **「構築」** で CRC 付きフレームを自動生成

---

## シリアルパラメータ

| パラメータ | 値 |
|-----------|-----|
| **ボーレート** | 300〜921600 + カスタム (1-9999999) |
| **データビット** | 5, 6, 7, 8 |
| **ストップビット** | 1, 1.5, 2 |
| **パリティ** | None, Odd, Even, Mark, Space |
| **フロー制御** | None, Hardware, Software |
| **受信エンコーディング** | UTF-8, GBK, GB18030, Latin-1, ASCII |

---

## 変更履歴

### v3.0.0 (2026-05-29)
**完全書き換え - Python/PyQt6 版**

- C++/Qt5/QML から Python/PyQt6 への完全な Python 書き換え
- よりシンプルなコード構造、保守と拡張が容易
- v2.0.0 の全機能を完全に保持
- クロスプラットフォーム対応を最適化（Windows EXE + Linux deb）
- 新しいアプリケーションアイコンデザイン

### v2.0.0 (2026-05-29)
ピン制御、自動応答、クイックコマンド、マルチエンコーディング、Modbus RTU、ログエクスポート、RX/TX統計、データフィルタリング、プロファイル管理、チェックサムツール、送信シーケンスを追加

### v1.0.0 (2026-05-27)
初回リリース

---

## FAQ

**Q: ポートが開けない？** 権限の問題です。`sudo python3 -m mousart` で実行するか、`dialout` グループにユーザーを追加してください。

**Q: 仮想シリアルポートが動作しない？** `socat` がインストールされているか確認：`sudo apt install socat`

---

## ライセンス

**MIT ライセンス** - [LICENSE](LICENSE) を参照。

**MOUSART** - シリアルデバッグをもっとシンプルに、もっと効率的に！
