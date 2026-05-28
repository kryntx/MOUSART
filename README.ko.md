# MOUSART
## 풀 기능 시리얼 포트 디버거

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **한국어** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v2.0.0)

**MOUSART**는 Qt5/QML로 구축된 풀 기능 시리얼 포트 디버거입니다. 임베디드 개발, 하드웨어 디버깅, 시리얼 통신을 위해 설계되었습니다. v2.0에서는 자동 응답, Modbus 프로토콜 지원, 빠른 명령, 데이터 기록 및 내보내기, 핀 제어, 다중 인코딩 지원 등 수십 가지 전문 기능을 추가했습니다.

---

## 기능 개요

### 1. 연결 관리
- 사용 가능한 포트 목록 자동 갱신 (2초 간격)
- 가상 시리얼 포트, USB-시리얼, Bluetooth 지원
- 보드레이트: 300~921600 프리셋 + 사용자 정의 (1-9999999)
- 데이터 비트: 5, 6, 7, 8 / 스톱 비트: 1, 1.5, 2
- 패리티: None, Even, Odd, Mark, Space
- 흐름 제어: 없음 / 하드웨어 (RTS/CTS) / 소프트웨어 (XON/XOFF)
- DTR/RTS 수동 제어 / CTS/DSR/DCD/RI 핀 상태 모니터링

### 2. 데이터 수신
- 텍스트 모드 (UTF-8 / GBK / GB18030 / Latin-1 / ASCII)
- 16진수 (HEX) 표시 모드
- 타임스탬프 표시 (밀리초 정밀도)
- 방향 표시기 (`<<` RX / `>>` TX / `!!` ERR)
- 일시 정지 (백그라운드에서 수신 계속)
- 키워드 필터 (일반 텍스트 / 정규식)
- 로그 제한 2000개, 자동 스크롤

### 3. 데이터 전송
- 텍스트 / HEX 전송 모드 전환
- 줄 바꿈 제어 (CR / LF 개별 토글)
- 정시 전송 (1ms~3600000ms, 횟수 제한 지원)
- 파일 전송
- Modbus RTU 프레임 빌더 (CRC 자동 계산)
- 빠른 명령 표시줄 (추가/편집/삭제, 영구 저장)
- 전송 시퀀스/대기열 (루ープ 지원)

### 4. 자동 응답
- 특정 키워드 수신 시 자동 응답
- 응답 지연 설정 (밀리초)
- 원클릭 활성화/비활성화

### 5. 인코딩 및 변환 도구
- 텍스트 ↔ Hex 변환
- 다중 인코딩: UTF-8, GBK, GB18030, Latin-1, ASCII
- 체크섬: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Modbus RTU 프레임 빌더 및 파서
- 2진수 / 10진수 / 16진수 변환

### 6. 데이터 기록 및 내보내기
- 로그를 TXT / CSV로 저장
- 자동 기록 (10MB에서 파일 분할)
- 실시간 RX/TX 바이트 카운터

### 7. 가상 시리얼 포트 (Linux 전용)
- `socat` 기반 원클릭 가상 포트 생성
- `/tmp/mousart_vport`를 통한 외부 프로그램 연결

### 8. UI 및 설정
- 다크/라이트 테마
- 0.8x~1.5x 폰트 스케일링
- 프로필 관리 (여러 설정 저장/전환)

---

## 스크린샷

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 디버그 인터페이스">
  <br>
  <em>MOUSART 시리얼 디버그 인터페이스 (다크 테마)</em>
</div>

---

## 빠른 시작

### 빌드된 바이너리

[GitHub Releases](https://github.com/kryntx/MOUSART/releases)에서 다운로드:

| 플랫폼 | 파일 | 크기 |
|--------|------|------|
| **Linux x86_64** | `MOUSART-v2.0.0-linux-x86_64.tar.gz` | ~105KB |
| **Windows x86_64** | `MOUSART-v2.0.0-windows-x86_64.zip` | ~23MB |

### 소스에서 빌드

```bash
# Ubuntu/Debian
sudo apt install qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev cmake socat

git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/MOUSART
```

---

## 사용법

### 가상 시리얼 포트 모드
1. 왼쪽 패널에서 **"Virtual"** 모드 선택
2. **"Start"** 클릭하여 가상 포트 생성
3. 외부 포트 경로 `/tmp/mousart_vport` 표시
4. 모든 시리얼 도구에서 이 경로로 연결

### 하드웨어 시리얼 디버그 모드
1. **"Debug"** 모드 선택
2. 포트 선택 및 매개변수 설정
3. **"Open"**으로 연결
4. 전송 영역에 입력 후 **"전송"** 또는 `Ctrl+Enter`

### 빠른 명령
1. 하단 빠른 명령 표시줄에서 **"+"** 클릭
2. 이름과 데이터 입력
3. 왼쪽 클릭으로 전송, 오른쪽 클릭으로 편집

### 자동 응답
1. 왼쪽 패널의 **"자동 응답"** 섹션
2. 토글 활성화 후 키워드와 응답 데이터 설정

### Modbus 프레임 빌더
1. 전송 도구 모음에서 **"Modbus"** 클릭
2. 슬레이브 주소, 기능 코드, 시작 주소, 수량 설정
3. **"빌드"**로 CRC 포함 프레임 자동 생성

---

## 시리얼 매개변수

| 매개변수 | 값 |
|---------|-----|
| **보드레이트** | 300~921600 + 사용자 정의 (1-9999999) |
| **데이터 비트** | 5, 6, 7, 8 |
| **스톱 비트** | 1, 1.5, 2 |
| **패리티** | None, Odd, Even, Mark, Space |
| **흐름 제어** | None, Hardware, Software |
| **수신 인코딩** | UTF-8, GBK, GB18030, Latin-1, ASCII |

---

## 변경 로그

### v2.0.0 (2026-05-29)
핀 제어, 자동 응답, 빠른 명령, 다중 인코딩, Modbus RTU, 로그 내보내기, RX/TX 통계, 데이터 필터링, 프로필 관리, 체크섬 도구, 전송 시퀀스 추가

### v1.0.0 (2026-05-27)
최초 릴리스

---

## FAQ

**Q: 포트를 열 수 없나요?** 권한 문제입니다. `sudo`로 실행하거나 `dialout` 그룹에 사용자를 추가하세요.

**Q: 가상 시리얼 포트가 작동하지 않나요?** `socat`이 설치되어 있는지 확인: `sudo apt install socat`

---

## 라이선스

**MIT 라이선스** - [LICENSE](LICENSE) 참조.

**MOUSART** - 시리얼 디버깅을 더 간단하고 효율적으로!
