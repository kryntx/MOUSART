"""Hardware serial port management using pyserial."""
import os
import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QTimer, QElapsedTimer, Qt

import serial
import serial.tools.list_ports

from mousart.utils.constants import SYSTEM_TTY_PREFIXES
from mousart.utils.encoding import decode_data, encode_string


class SerialPortManager(QObject):
    """Manages hardware serial port connections via pyserial."""

    is_open_changed = pyqtSignal()
    current_port_changed = pyqtSignal()
    port_list_changed = pyqtSignal()
    data_received = pyqtSignal(str, bytes)
    error_occurred = pyqtSignal(str)
    port_opened = pyqtSignal(str)
    port_closed = pyqtSignal()
    filter_system_tty_changed = pyqtSignal()
    timed_send_active_changed = pyqtSignal()
    timed_send_completed = pyqtSignal(str)
    dtr_changed = pyqtSignal()
    rts_changed = pyqtSignal()
    pin_states_changed = pyqtSignal()
    stats_changed = pyqtSignal()
    auto_reply_config_changed = pyqtSignal()
    echo_enabled_changed = pyqtSignal()
    newline_changed = pyqtSignal()
    receive_encoding_changed = pyqtSignal()
    auto_save_enabled_changed = pyqtSignal()
    auto_save_path_changed = pyqtSignal()
    send_sequence_active_changed = pyqtSignal()
    send_sequence_completed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._port = None
        self._ports = []
        self._filter_system_tty = True
        self._running = False
        self._read_thread = None

        # Timed send
        self._timed_send_timer = QTimer(self)
        self._timed_send_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timed_send_timer.timeout.connect(self._on_timed_send_tick)
        self._timed_send_data = ""
        self._timed_send_hex = False
        self._timed_send_count = -1
        self._timed_send_sent = 0

        # Stats
        self._rx_bytes = 0
        self._tx_bytes = 0
        self._rx_errors = 0
        self._rx_bytes_snapshot = 0
        self._tx_bytes_snapshot = 0
        self._stats_timer = QElapsedTimer()
        self._stats_timer.start()
        self._stats_update_timer = QTimer(self)
        self._stats_update_timer.setInterval(1000)
        self._stats_update_timer.timeout.connect(self._on_stats_timer)
        self._stats_update_timer.start()

        # Auto-reply
        self._auto_reply_enabled = False
        self._auto_reply_match = ""
        self._auto_reply_response = ""
        self._auto_reply_delay = 0
        self._auto_reply_timer = QTimer(self)
        self._auto_reply_timer.setSingleShot(True)
        self._auto_reply_timer.timeout.connect(self._on_auto_reply_tick)

        # Echo
        self._echo_enabled = False

        # Newline
        self._newline_cr = True
        self._newline_lf = True

        # Encoding
        self._receive_encoding = "UTF-8"

        # Auto-save
        self._auto_save_enabled = False
        self._auto_save_path = ""

        # Send sequence
        self._send_seq_timer = QTimer(self)
        self._send_seq_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._send_seq_timer.timeout.connect(self._on_send_sequence_tick)
        self._send_seq_data = []
        self._send_seq_delays = []
        self._send_seq_hex = False
        self._send_seq_loop = False
        self._send_seq_index = 0

        # Port discovery
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.refreshPorts)
        self._refresh_timer.start(2000)
        self.refreshPorts()

    def _get_port_name(self, display_name: str) -> str:
        """Extract port name from display string."""
        name = display_name
        idx = name.find(" - ")
        if idx >= 0:
            name = name[:idx]
        name = name.replace(" [virtual]", "").strip()
        if name.startswith("pts/"):
            name = "/dev/" + name
        return name

    @pyqtProperty(bool, notify=is_open_changed)
    def isOpen(self):
        return self._port is not None and self._port.is_open

    @pyqtProperty(str, notify=current_port_changed)
    def currentPort(self):
        if self._port and self._port.is_open:
            return self._port.name
        return ""

    @pyqtProperty(list, notify=port_list_changed)
    def portList(self):
        return self._ports

    @pyqtProperty(bool, notify=filter_system_tty_changed)
    def filterSystemTty(self):
        return self._filter_system_tty

    @filterSystemTty.setter
    def filterSystemTty(self, value):
        if self._filter_system_tty == value:
            return
        self._filter_system_tty = value
        self.filter_system_tty_changed.emit()
        self.refreshPorts()

    @pyqtProperty(bool, notify=timed_send_active_changed)
    def timedSendActive(self):
        return self._timed_send_timer.isActive()

    # Pin control
    @pyqtProperty(bool, notify=dtr_changed)
    def dtr(self):
        if not self.isOpen:
            return False
        return self._port.dtr

    @dtr.setter
    def dtr(self, state):
        if self.isOpen:
            self._port.dtr = state
            self.dtr_changed.emit()
            self.pin_states_changed.emit()

    @pyqtProperty(bool, notify=rts_changed)
    def rts(self):
        if not self.isOpen:
            return False
        return self._port.rts

    @rts.setter
    def rts(self, state):
        if self.isOpen:
            self._port.rts = state
            self.rts_changed.emit()
            self.pin_states_changed.emit()

    @pyqtProperty(bool, notify=pin_states_changed)
    def cts(self):
        if not self.isOpen:
            return False
        return self._port.cts

    @pyqtProperty(bool, notify=pin_states_changed)
    def dsr(self):
        if not self.isOpen:
            return False
        return self._port.dsr

    @pyqtProperty(bool, notify=pin_states_changed)
    def dcd(self):
        if not self.isOpen:
            return False
        return self._port.cd

    @pyqtProperty(bool, notify=pin_states_changed)
    def ri(self):
        if not self.isOpen:
            return False
        return self._port.ri

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

    @pyqtProperty(int, notify=stats_changed)
    def rxErrors(self):
        return self._rx_errors

    # Auto-reply
    @pyqtProperty(bool, notify=auto_reply_config_changed)
    def autoReplyEnabled(self):
        return self._auto_reply_enabled

    @autoReplyEnabled.setter
    def autoReplyEnabled(self, v):
        if self._auto_reply_enabled == v:
            return
        self._auto_reply_enabled = v
        self.auto_reply_config_changed.emit()

    @pyqtProperty(str, notify=auto_reply_config_changed)
    def autoReplyMatch(self):
        return self._auto_reply_match

    @autoReplyMatch.setter
    def autoReplyMatch(self, v):
        if self._auto_reply_match == v:
            return
        self._auto_reply_match = v
        self.auto_reply_config_changed.emit()

    @pyqtProperty(str, notify=auto_reply_config_changed)
    def autoReplyResponse(self):
        return self._auto_reply_response

    @autoReplyResponse.setter
    def autoReplyResponse(self, v):
        if self._auto_reply_response == v:
            return
        self._auto_reply_response = v
        self.auto_reply_config_changed.emit()

    @pyqtProperty(int, notify=auto_reply_config_changed)
    def autoReplyDelay(self):
        return self._auto_reply_delay

    @autoReplyDelay.setter
    def autoReplyDelay(self, v):
        if self._auto_reply_delay == v:
            return
        self._auto_reply_delay = v
        self.auto_reply_config_changed.emit()

    # Echo
    @pyqtProperty(bool, notify=echo_enabled_changed)
    def echoEnabled(self):
        return self._echo_enabled

    @echoEnabled.setter
    def echoEnabled(self, v):
        if self._echo_enabled == v:
            return
        self._echo_enabled = v
        self.echo_enabled_changed.emit()

    # Newline
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

    # Encoding
    @pyqtProperty(str, notify=receive_encoding_changed)
    def receiveEncoding(self):
        return self._receive_encoding

    @receiveEncoding.setter
    def receiveEncoding(self, v):
        if self._receive_encoding == v:
            return
        self._receive_encoding = v
        self.receive_encoding_changed.emit()

    # Auto-save
    @pyqtProperty(bool, notify=auto_save_enabled_changed)
    def autoSaveEnabled(self):
        return self._auto_save_enabled

    @autoSaveEnabled.setter
    def autoSaveEnabled(self, v):
        if self._auto_save_enabled == v:
            return
        self._auto_save_enabled = v
        self.auto_save_enabled_changed.emit()

    @pyqtProperty(str, notify=auto_save_path_changed)
    def autoSavePath(self):
        return self._auto_save_path

    @autoSavePath.setter
    def autoSavePath(self, v):
        if self._auto_save_path == v:
            return
        self._auto_save_path = v
        self.auto_save_path_changed.emit()

    # Send sequence
    @pyqtProperty(bool, notify=send_sequence_active_changed)
    def sendSequenceActive(self):
        return self._send_seq_timer.isActive()

    @pyqtSlot()
    def refreshPorts(self):
        new_ports = []
        for port_info in serial.tools.list_ports.comports():
            name = port_info.device
            # Extract short name for display
            short_name = name.split("/")[-1] if "/" in name else name
            if self._filter_system_tty:
                if any(short_name.startswith(p) for p in SYSTEM_TTY_PREFIXES):
                    continue
            display = short_name
            if port_info.description and port_info.description != "n/a":
                display += f" - {port_info.description}"
            new_ports.append(display)

        # Check for virtual port symlink
        vport_link = "/tmp/mousart_vport"
        if os.path.islink(vport_link):
            vp_name = f"{vport_link} [virtual]"
            if vp_name not in new_ports:
                new_ports.append(vp_name)

        if new_ports != self._ports:
            self._ports = new_ports
            self.port_list_changed.emit()

    @pyqtSlot(str, int, int, int, int, int, result=bool)
    def openPort(self, name: str, baud_rate: int, data_bits: int,
                 stop_bits: int, parity: int, flow_control: int) -> bool:
        if self._port and self._port.is_open:
            self.closePort()

        port_name = self._get_port_name(name)

        try:
            # Map parity
            parity_map = {0: serial.PARITY_NONE, 1: serial.PARITY_ODD,
                          2: serial.PARITY_EVEN, 3: serial.PARITY_MARK,
                          4: serial.PARITY_SPACE}
            # Map stop bits
            stopbits_map = {1: serial.STOPBITS_ONE, 1.5: serial.STOPBITS_ONE_POINT_FIVE,
                            2: serial.STOPBITS_TWO}
            # Map flow control
            xonxoff = flow_control == 2
            rtscts = flow_control == 1

            self._port = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                bytesize=data_bits,
                stopbits=stopbits_map.get(stop_bits, serial.STOPBITS_ONE),
                parity=parity_map.get(parity, serial.PARITY_NONE),
                xonxoff=xonxoff,
                rtscts=rtscts,
                timeout=0.05
            )

            self.resetStats()
            self._running = True
            self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self._read_thread.start()

            self.is_open_changed.emit()
            self.current_port_changed.emit()
            self.port_opened.emit(port_name)
            self.pin_states_changed.emit()
            return True

        except Exception as e:
            self.error_occurred.emit(str(e))
            return False

    @pyqtSlot()
    def closePort(self):
        self.stopTimedSend()
        self.stopSendSequence()
        self._running = False
        if self._port and self._port.is_open:
            self._port.close()
            self._port = None
            self.is_open_changed.emit()
            self.current_port_changed.emit()
            self.port_closed.emit()

    @pyqtSlot(str, bool, result=int)
    def sendData(self, data: str, hex_mode: bool) -> int:
        if not self.isOpen:
            self.error_occurred.emit("Port not open")
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

            written = self._port.write(data_bytes)
            if written and written > 0:
                self._tx_bytes += written
                self.stats_changed.emit()
            return written if written else 0
        except Exception as e:
            self.error_occurred.emit(str(e))
            return -1

    @pyqtSlot(bytes, result=int)
    def sendRawBytes(self, data: bytes) -> int:
        if not self.isOpen:
            self.error_occurred.emit("Port not open")
            return -1
        try:
            written = self._port.write(data)
            if written and written > 0:
                self._tx_bytes += written
                self.stats_changed.emit()
            return written if written else 0
        except Exception as e:
            self.error_occurred.emit(str(e))
            return -1

    @pyqtSlot(str, bool, result=str)
    def sendFileData(self, file_path: str, hex_mode: bool) -> str:
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            if not data:
                return "文件为空 (Empty file)"

            if hex_mode:
                hex_str = data.decode("utf-8", errors="replace").replace(" ", "").replace("\n", "").replace("\r", "")
                data_bytes = bytes.fromhex(hex_str)
            else:
                data_bytes = data

            written = self.sendRawBytes(data_bytes)
            if written > 0:
                return str(written)
            return "发送失败 (Send failed)"
        except Exception as e:
            return f"错误: {e}"

    @pyqtSlot(str, bool, int, int)
    def startTimedSend(self, data: str, hex_mode: bool, interval_ms: int, count: int = -1):
        if not self.isOpen:
            self.error_occurred.emit("Port not open")
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
        self._rx_errors = 0
        self._rx_bytes_snapshot = 0
        self._tx_bytes_snapshot = 0
        self._stats_timer.restart()
        self.stats_changed.emit()

    @pyqtSlot()
    def updatePinStates(self):
        self.pin_states_changed.emit()

    @pyqtSlot(list, list, bool, bool)
    def startSendSequence(self, data_list: list, delays: list, hex_mode: bool, loop: bool):
        if not self.isOpen or not data_list:
            return
        self.stopSendSequence()
        self._send_seq_data = data_list
        self._send_seq_delays = delays
        self._send_seq_hex = hex_mode
        self._send_seq_loop = loop
        self._send_seq_index = 0
        self._on_send_sequence_tick()

    @pyqtSlot()
    def stopSendSequence(self):
        self._send_seq_timer.stop()
        self._send_seq_index = 0
        self.send_sequence_active_changed.emit()

    def _read_loop(self):
        """Background thread for reading serial data."""
        while self._running and self._port and self._port.is_open:
            try:
                data = self._port.read(4096)
                if data:
                    self._rx_bytes += len(data)
                    self.stats_changed.emit()

                    text = decode_data(data, self._receive_encoding)
                    self.data_received.emit(text, data)

                    # Auto-reply check
                    if self._auto_reply_enabled and self._auto_reply_match:
                        check_text = data.decode("utf-8", errors="replace")
                        if self._auto_reply_match.lower() in check_text.lower():
                            if self._auto_reply_delay > 0:
                                self._auto_reply_timer.start(self._auto_reply_delay)
                            else:
                                self._send_auto_reply()

                    # Auto-save
                    if self._auto_save_enabled:
                        self._append_to_file(data)
            except serial.SerialException:
                if self._running:
                    self._rx_errors += 1
                    self.error_occurred.emit("Serial read error")
                break
            except Exception:
                if self._running:
                    self._rx_errors += 1
                break

        # Port disconnected
        if self._running and self._port and not self._port.is_open:
            self._running = False
            self.is_open_changed.emit()
            self.current_port_changed.emit()
            self.port_closed.emit()

    def _send_auto_reply(self):
        """Send auto-reply response."""
        if not self.isOpen:
            return
        try:
            response = self._auto_reply_response
            if response.startswith("\\x"):
                hex_str = response.replace("\\x", "").replace(" ", "")
                data_bytes = bytes.fromhex(hex_str)
            else:
                data_bytes = response.encode("utf-8")
            self._port.write(data_bytes)
            self.timed_send_completed.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _on_auto_reply_tick(self):
        self._send_auto_reply()

    def _on_timed_send_tick(self):
        if not self.isOpen:
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

    def _on_send_sequence_tick(self):
        if not self.isOpen or not self._send_seq_data:
            self.stopSendSequence()
            return

        if self._send_seq_index >= len(self._send_seq_data):
            if self._send_seq_loop:
                self._send_seq_index = 0
            else:
                self.stopSendSequence()
                self.send_sequence_completed.emit()
                return

        self.sendData(self._send_seq_data[self._send_seq_index], self._send_seq_hex)
        self.timed_send_completed.emit(self._send_seq_data[self._send_seq_index])

        self._send_seq_index += 1
        if self._send_seq_index < len(self._send_seq_data):
            delay = self._send_seq_delays[self._send_seq_index - 1] if self._send_seq_index - 1 < len(self._send_seq_delays) else 100
            self._send_seq_timer.start(max(delay, 1))
        elif self._send_seq_loop:
            self._send_seq_timer.start(100)
        else:
            self.stopSendSequence()
            self.send_sequence_completed.emit()

    def _append_to_file(self, data: bytes):
        """Append received data to auto-save file."""
        import os
        from datetime import datetime

        path = self._auto_save_path
        if not path:
            log_dir = os.path.join(os.path.expanduser("~"), "mousart_logs")
            os.makedirs(log_dir, exist_ok=True)
            path = os.path.join(log_dir, f"mousart_{datetime.now().strftime('%Y%m%d')}.log")

        try:
            with open(path, "a", encoding="utf-8") as f:
                ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                f.write(f"[{ts}] RX: {data.decode('utf-8', errors='replace')}\n")
        except Exception:
            pass


