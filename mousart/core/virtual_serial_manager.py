"""Virtual serial port management via socat (Linux only)."""
import os
import sys
import subprocess
import threading
import time
from mousart.qt_compat import *

from mousart.utils.encoding import decode_data


class VirtualSerialManager(QObject):
    """Manages a virtual serial port pair using socat on Linux."""

    is_active_changed = pyqtSignal()
    external_port_changed = pyqtSignal()
    data_received = pyqtSignal(str, bytes)
    error_occurred = pyqtSignal(str)
    timed_send_active_changed = pyqtSignal()
    timed_send_completed = pyqtSignal(str)
    stats_changed = pyqtSignal()
    echo_enabled_changed = pyqtSignal()
    newline_changed = pyqtSignal()
    receive_encoding_changed = pyqtSignal()

    VPORT_SYMLINK = "/tmp/mousart_vport"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._socat_proc = None
        self._pty_a = ""
        self._pty_b = ""
        self._fd = -1
        self._active = False
        self._running = False
        self._read_thread = None

        # Timed send
        self._timed_send_timer = QTimer(self)
        self._timed_send_timer.timeout.connect(self._on_timed_send_tick)
        self._timed_send_data = ""
        self._timed_send_hex = False
        self._timed_send_count = -1
        self._timed_send_sent = 0

        # Stats
        self._rx_bytes = 0
        self._tx_bytes = 0
        self._rx_bytes_snapshot = 0
        self._tx_bytes_snapshot = 0
        self._stats_timer = QElapsedTimer()
        self._stats_timer.start()
        self._stats_update_timer = QTimer(self)
        self._stats_update_timer.setInterval(1000)
        self._stats_update_timer.timeout.connect(self._on_stats_timer)
        self._stats_update_timer.start()

        # Settings
        self._echo_enabled = False
        self._newline_cr = True
        self._newline_lf = True
        self._receive_encoding = "UTF-8"

    @pyqtProperty(bool, notify=is_active_changed)
    def isActive(self):
        return self._active

    @pyqtProperty(str, notify=external_port_changed)
    def externalPort(self):
        return self.VPORT_SYMLINK if self._active else ""

    # Stats
    @pyqtProperty(int, notify=stats_changed)
    def rxBytes(self):
        return self._rx_bytes

    @pyqtProperty(int, notify=stats_changed)
    def txBytes(self):
        return self._tx_bytes

    @pyqtProperty(float, notify=stats_changed)
    def rxRate(self):
        elapsed = self._stats_timer.elapsed()
        if elapsed < 100:
            return 0.0
        return (self._rx_bytes - self._rx_bytes_snapshot) * 1000.0 / elapsed

    @pyqtProperty(float, notify=stats_changed)
    def txRate(self):
        elapsed = self._stats_timer.elapsed()
        if elapsed < 100:
            return 0.0
        return (self._tx_bytes - self._tx_bytes_snapshot) * 1000.0 / elapsed

    @pyqtProperty(bool, notify=timed_send_active_changed)
    def timedSendActive(self):
        return self._timed_send_timer.isActive()

    # Settings
    @pyqtProperty(bool, notify=echo_enabled_changed)
    def echoEnabled(self):
        return self._echo_enabled

    @echoEnabled.setter
    def echoEnabled(self, v):
        if self._echo_enabled == v:
            return
        self._echo_enabled = v
        self.echo_enabled_changed.emit()

    @pyqtProperty(bool, notify=newline_changed)
    def newlineCr(self):
        return self._newline_cr

    @newlineCr.setter
    def newlineCr(self, v):
        if self._newline_cr == v:
            return
        self._newline_cr = v
        self.newline_changed.emit()

    @pyqtProperty(bool, notify=newline_changed)
    def newlineLf(self):
        return self._newline_lf

    @newlineLf.setter
    def newlineLf(self, v):
        if self._newline_lf == v:
            return
        self._newline_lf = v
        self.newline_changed.emit()

    @pyqtProperty(str, notify=receive_encoding_changed)
    def receiveEncoding(self):
        return self._receive_encoding

    @receiveEncoding.setter
    def receiveEncoding(self, v):
        if self._receive_encoding == v:
            return
        self._receive_encoding = v
        self.receive_encoding_changed.emit()

    @pyqtSlot(result=bool)
    def startVirtualPort(self):
        """Start a virtual serial port pair using socat."""
        if sys.platform == "win32":
            self.error_occurred.emit("虚拟串口功能在 Windows 上暂不可用，请使用硬件串口调试模式。")
            return False

        if self._active:
            self.stopVirtualPort()

        try:
            # Remove old symlink
            if os.path.islink(self.VPORT_SYMLINK):
                os.unlink(self.VPORT_SYMLINK)

            self._socat_proc = subprocess.Popen(
                ["socat", "-d", "-d", "pty,raw,echo=0",
                 f"pty,raw,echo=0,link={self.VPORT_SYMLINK}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )

            # Wait for socat to create PTYs
            import re
            pty_paths = []
            start_time = time.time()
            while time.time() - start_time < 3.0:
                # Read stderr for PTY info
                import select
                ready, _, _ = select.select([self._socat_proc.stderr], [], [], 0.1)
                if ready:
                    line = self._socat_proc.stderr.readline()
                    if line:
                        match = re.search(r"PTY is (\S+)", line)
                        if match:
                            pty_paths.append(match.group(1))
                            if len(pty_paths) >= 2:
                                break
                if self._socat_proc.poll() is not None:
                    break

            if len(pty_paths) < 2:
                self.stopVirtualPort()
                self.error_occurred.emit("启动 socat 失败: 无法获取 PTY 路径")
                return False

            self._pty_a = pty_paths[0]
            self._pty_b = pty_paths[1]

            # Open side A
            import termios
            self._fd = os.open(self._pty_a, os.O_RDWR | os.O_NOCTTY)

            # Configure terminal
            attrs = termios.tcgetattr(self._fd)
            import tty
            tty.setraw(self._fd)
            attrs = termios.tcgetattr(self._fd)
            attrs[6][termios.VMIN] = 0
            attrs[6][termios.VTIME] = 1
            attrs[3] &= ~(termios.ECHO | termios.ECHONL | termios.ECHOE | termios.ICANON)
            attrs[1] &= ~(termios.ONLCR | termios.OCRNL)
            termios.tcsetattr(self._fd, termios.TCSANOW, attrs)

            self._active = True
            self._running = True
            self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self._read_thread.start()

            self.resetStats()
            self.is_active_changed.emit()
            self.external_port_changed.emit()
            return True

        except FileNotFoundError:
            self.error_occurred.emit("socat 未安装。请运行: sudo apt install socat")
            return False
        except Exception as e:
            self.error_occurred.emit(f"启动虚拟串口失败: {e}")
            self.stopVirtualPort()
            return False

    @pyqtSlot()
    def stopVirtualPort(self):
        """Stop the virtual serial port."""
        self.stopTimedSend()
        self._running = False

        if self._fd >= 0:
            try:
                os.close(self._fd)
            except OSError:
                pass
            self._fd = -1

        if self._socat_proc:
            try:
                self._socat_proc.terminate()
                self._socat_proc.wait(timeout=2)
            except Exception:
                try:
                    self._socat_proc.kill()
                except Exception:
                    pass
            self._socat_proc = None

        self._pty_a = ""
        self._pty_b = ""

        if os.path.islink(self.VPORT_SYMLINK):
            try:
                os.unlink(self.VPORT_SYMLINK)
            except OSError:
                pass

        was_active = self._active
        self._active = False
        if was_active:
            self.is_active_changed.emit()
            self.external_port_changed.emit()

    @pyqtSlot(str, bool, result=int)
    def sendData(self, data: str, hex_mode: bool) -> int:
        if self._fd < 0:
            self.error_occurred.emit("虚拟串口未打开")
            return -1

        try:
            if hex_mode:
                hex_str = data.replace(" ", "").replace("\n", "").replace("\r", "")
                data_bytes = bytes.fromhex(hex_str)
            else:
                text = data
                if self._newline_cr:
                    text += "\r"
                if self._newline_lf:
                    text += "\n"
                data_bytes = text.encode("utf-8")

            written = os.write(self._fd, data_bytes)
            self._tx_bytes += written
            self.stats_changed.emit()
            return written
        except Exception as e:
            self.error_occurred.emit(str(e))
            return -1

    @pyqtSlot(str, bool, int, int)
    def startTimedSend(self, data: str, hex_mode: bool, interval_ms: int, count: int = -1):
        if not self._active:
            self.error_occurred.emit("虚拟串口未打开")
            return
        self._timed_send_data = data
        self._timed_send_hex = hex_mode
        self._timed_send_count = count
        self._timed_send_sent = 0
        self._timed_send_timer.setInterval(max(interval_ms, 1))
        self._timed_send_timer.start()
        self.timed_send_active_changed.emit()

    @pyqtSlot()
    def stopTimedSend(self):
        self._timed_send_timer.stop()
        self._timed_send_sent = 0
        self._timed_send_count = -1
        self.timed_send_active_changed.emit()

    @pyqtSlot()
    def resetStats(self):
        self._rx_bytes = 0
        self._tx_bytes = 0
        self._rx_bytes_snapshot = 0
        self._tx_bytes_snapshot = 0
        self._stats_timer.restart()
        self.stats_changed.emit()

    def _read_loop(self):
        """Background thread for reading from virtual serial port."""
        import select
        while self._running and self._fd >= 0:
            try:
                ready, _, _ = select.select([self._fd], [], [], 0.05)
                if ready:
                    data = os.read(self._fd, 4096)
                    if data:
                        self._rx_bytes += len(data)
                        self.stats_changed.emit()
                        text = decode_data(data, self._receive_encoding)
                        self.data_received.emit(text, data)
                    elif not data:
                        # EOF
                        break
            except OSError:
                break
            except Exception:
                break

    def _on_timed_send_tick(self):
        if not self._active:
            self.stopTimedSend()
            return
        result = self.sendData(self._timed_send_data, self._timed_send_hex)
        if result > 0:
            self._timed_send_sent += 1
            self.timed_send_completed.emit(self._timed_send_data)
            if 0 < self._timed_send_count <= self._timed_send_sent:
                self.stopTimedSend()

    def _on_stats_timer(self):
        self._rx_bytes_snapshot = self._rx_bytes
        self._tx_bytes_snapshot = self._tx_bytes
        self._stats_timer.restart()
        self.stats_changed.emit()
