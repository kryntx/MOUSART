# MOUSART
## 풀기능 시리얼 포트 디버그 도구

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)

**MOUSART** 은 임베디드 개발, 하드웨어 디버깅, 시리얼 통신 시나리오를 위해 설계된 풀기능 시리얼 포트 디버그 도구입니다. 시리얼 디버그와 가상 시리얼 포트의 두 가지 독립 모드를 지원하며, 자동 응답, Modbus 프로토콜 지원, 빠른 명령, 데이터 기록 및 내보내기, 핀 제어, 다중 인코딩 지원 등 수십 가지 전문 기능을 갖추고 있습니다.

---

## 스크린샷

### 시리얼 디버그 모드

<div align="center">
  <img src="img/d1.png" width="800" alt="MOUSART 시리얼 디버그 인터페이스">
  <br>
  <em>시리얼 디버그 모드 - 실제 하드웨어 시리얼 포트에 연결하여 데이터 송수신</em>
</div>

### 가상 시리얼 포트 모드

<div align="center">
  <img src="img/v1.png" width="800" alt="MOUSART 가상 시리얼 포트 인터페이스">
  <br>
  <em>가상 시리얼 포트 모드 - 외부 프로그램 연결용 가상 시리얼 포트 쌍 생성</em>
</div>

---

## 기능 목록

### 시리얼 디버그 모드
- 사용 가능한 시리얼 포트 목록 자동 갱신 (2초 폴링)
- USB-시리얼 변환, 블루투스 시리얼 포트 지원
- 보드레이트: 300 ~ 921600 프리셋 값 + 사용자 정의 값 (1-9999999)
- 데이터 비트: 5, 6, 7, 8 / 스톱 비트: 1, 1.5, 2
- 패리티: None, Even, Odd, Mark, Space
- 흐름 제어: 없음 / 하드웨어 (RTS/CTS) / 소프트웨어 (XON/XOFF)
- DTR/RTS 수동 설정 제어
- CTS/DSR/DCD/RI 핀 레벨 실시간 모니터링
- 자동 응답 (키워드 매칭 + 지연 설정)

### 가상 시리얼 포트 모드 (Linux 전용)
- `socat` 기반 원클릭 가상 시리얼 포트 쌍 생성
- 외부 프로그램은 `/tmp/mousart_vport`를 통해 연결
- 독립적인 송수신 영역 및 통계 정보

### 데이터 송수신
- 텍스트 / HEX 전송 모드 전환
- 다중 인코딩 지원: UTF-8, GBK, GB18030, Latin-1, ASCII
- 전송 줄 바꿈 제어 (CR / LF 개별 스위치)
- 타이머 전송 (1ms ~ 3600000ms)
- 파일 전송
- Modbus RTU 프레임 빌더 (자동 CRC)
- 빠른 명령 표시줄 (왼쪽 클릭 전송, 오른쪽 클릭 편집)
- Ctrl+Enter 단축키 전송

### 데이터 분석
- 체크섬 계산: Sum8 / XOR8 / CRC16-Modbus / CRC32
- 2진수 / 10진수 / 16진수 변환
- 텍스트 ↔ Hex 실시간 변환
- 키워드 / 정규 표현식 필터

### 데이터 기록
- 원클릭으로 로그를 TXT / CSV에 저장
- 자동 기록 (10MB/파일 자동 분할)
- 실시간 RX/TX 바이트 카운트 및 속도 표시

### 인터페이스
- 다크/라이트 듀얼 테마
- 0.8x-1.5x 폰트 스케일링
- 프로파일 관리

---

## 설치 가이드

### Linux (Debian/Ubuntu)

#### 방법 1: deb 패키지 설치 (권장)

```bash
# 1. deb 패키지 다운로드
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb

# 2. 설치 (의존성 자동 설치)
sudo apt install ./mouserial_3.0.0-1_amd64.deb

# 3. 실행
mousart
```

#### 방법 2: 소스 코드에서 실행

```bash
# 1. 시스템 의존성 설치
sudo apt update
sudo apt install python3-pyqt5 python3-serial socat git

# 2. 프로젝트 클론
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. 실행
python3 -m mousart
```

#### 방법 3: pip로 의존성 설치 후 실행

```bash
# 1. 시스템 의존성 설치
sudo apt install socat

# 2. Python 의존성 설치
pip3 install PyQt5 pyserial

# 3. 클론 및 실행
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### 방법 1: 소스 코드에서 실행

```bash
# 1. Python 3.10+ 설치 (python.org에서 다운로드)

# 2. 의존성 설치
pip install PyQt5 pyserial

# 3. 프로젝트 클론 및 실행
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### 방법 2: EXE 빌드

```bash
# 1. 의존성 설치
pip install PyQt5 pyserial pyinstaller

# 2. 빌드
pyinstaller pyinstaller.spec --noconfirm

# 3. 생성된 dist/MOUSART.exe 실행
```

---

## 제거 가이드

### Linux deb 패키지 제거

```bash
# 방법 1: apt를 사용하여 제거
sudo apt remove mouserial

# 방법 2: 완전 제거 (설정 파일 포함)
sudo apt purge mouserial

# 사용자 설정 정리 (선택 사항)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Linux 소스 설치 제거

```bash
# 프로젝트 디렉토리 삭제
rm -rf /path/to/MOUSART

# 사용자 설정 정리 (선택 사항)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Windows 제거

```
# 프로젝트 디렉토리 삭제

# 사용자 설정 정리 (선택 사항)
# %USERPROFILE%\.mousart 디렉토리 삭제
# %USERPROFILE%\mousart_logs 디렉토리 삭제
```

---

## 사용 가이드

### 시리얼 디버그 모드
1. 왼쪽 패널에서 **"시리얼 디버그"** 모드 선택
2. 드롭다운 목록에서 시리얼 포트 선택
3. 시리얼 포트 매개변수 설정 (보드레이트, 데이터 비트, 스톱 비트, 패리티, 흐름 제어)
4. **"열기"** 클릭하여 연결 확립
5. 오른쪽 전송 영역에 데이터 입력 후 **"전송"** 클릭 또는 `Ctrl+Enter` 누르기
6. 수신 영역에 데이터가 실시간으로 표시됨

### 가상 시리얼 포트 모드 (Linux 전용)
1. 왼쪽 패널에서 **"시뮬레이션 시리얼 포트"** 모드 선택
2. **"시작"** 클릭하여 가상 시리얼 포트 쌍 생성
3. 화면에 외부 포트 경로 `/tmp/mousart_vport` 표시
4. 임의의 시리얼 도구로 이 경로에 연결
5. 전송 영역에 데이터 입력 후 전송

### 빠른 명령
1. 하단 빠른 명령 표시줄의 **"+"** 클릭하여 새 명령 추가
2. 이름과 데이터 입력 (텍스트 및 HEX 지원)
3. 명령 버튼 왼쪽 클릭으로 즉시 전송
4. 명령 버튼 오른쪽 클릭으로 편집 또는 삭제

### 자동 응답 (시리얼 디버그 모드)
1. 왼쪽 패널에서 **"자동 응답"** 영역 찾기
2. 스위치 활성화 후 매칭 키워드 및 응답 데이터 설정
3. 응답 지연 설정 가능 (밀리초)

### Modbus 프레임 빌드
1. 전송 도구 모음의 **"Modbus"** 버튼 클릭
2. 슬레이브 주소, 기능 코드, 시작 주소, 수량 설정
3. **"빌드"** 클릭하면 CRC가 포함된 Modbus RTU 프레임이 자동 생성됨

### 로그 기록 및 내보내기
1. 수신 영역 도구 모음의 **"기록"** 버튼 클릭하여 자동 기록 시작
2. 모든 송수신 데이터가 `~/mousart_logs/`에 자동 저장됨
3. **"저장"** 클릭하면 TXT 또는 CSV로 수동 내보내기 가능

### 핀 제어 (시리얼 디버그 모드)
1. 시리얼 포트를 열면 왼쪽 패널에 핀 제어 표시줄이 표시됨
2. DTR/RTS 버튼 클릭하여 핀 레벨 전환
3. CTS/DSR/DCD/RI 상태 표시등이 실시간으로 표시됨

---

## 자주 묻는 질문

**Q: 시리얼 포트를 열 수 없나요?**
A: 일반적으로 권한 문제입니다. 사용자를 `dialout` 그룹에 추가하세요:
```bash
sudo usermod -aG dialout $USER
# 로그아웃 후 다시 로그인하면 적용됩니다
```

**Q: 가상 시리얼 포트를 사용할 수 없나요?**
A: `socat`이 설치되어 있는지 확인하세요:
```bash
sudo apt install socat
```

**Q: 중국어 표시가 깨지나요?**
A: 왼쪽 패널에서 올바른 수신 인코딩 (예: GBK)을 선택하세요.

**Q: Modbus 명령을 전송하려면?**
A: **"Modbus"** 버튼을 클릭하고 매개변수를 입력한 후 **"빌드"**를 클릭하면 프레임 데이터가 자동으로 입력됩니다.

**Q: 자동 기록 파일의 저장 위치는?**
A: 기본적으로 `~/mousart_logs/`에 저장되며, 파일 이름 형식은 `mousart_rec_YYYYMMDD_HHmmss.log`입니다.

---

## 라이선스

본 프로젝트는 **MIT 라이선스**를 사용합니다 - 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

**MOUSART** - 시리얼 디버깅을 더 간단하고 효율적으로!
