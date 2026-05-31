"""Log file management with auto-recording and file rotation."""
import os
from datetime import datetime
from mousart.qt_compat import *

from mousart.utils.constants import MAX_RECORD_FILE_SIZE


class LogFileManager(QObject):
    """Manages log file saving, exporting, and auto-recording."""

    is_recording_changed = pyqtSignal()
    current_log_file_changed = pyqtSignal()
    recorded_bytes_changed = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_recording = False
        self._current_log_file = ""
        self._record_directory = ""
        self._recorded_bytes = 0
        self._file_index = 0

    @pyqtProperty(bool, notify=is_recording_changed)
    def isRecording(self):
        return self._is_recording

    @pyqtProperty(str, notify=current_log_file_changed)
    def currentLogFile(self):
        return self._current_log_file

    @pyqtProperty(int, notify=recorded_bytes_changed)
    def recordedBytes(self):
        return self._recorded_bytes

    @pyqtSlot(str, list, bool, result=bool)
    def saveLogToFile(self, file_path: str, log_entries: list, append: bool = False) -> bool:
        try:
            mode = "a" if append else "w"
            with open(file_path, mode, encoding="utf-8") as f:
                if not append:
                    f.write(f"MOUSART Log Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")

                for entry in log_entries:
                    if isinstance(entry, dict):
                        time_str = entry.get("logTime", "")
                        log_type = entry.get("logType", "")
                        data = entry.get("logData", "")

                        prefix = {"RX": "<< RX: ", "TX": ">> TX: ", "ERR": "!! ERR: ",
                                  "INFO": "i  INFO: ", "SYS": "#  SYS: "}.get(log_type, "   ")
                        f.write(f"[{time_str}] {prefix}{data}\n")
            return True
        except Exception as e:
            self.error_occurred.emit(f"无法保存文件: {e}")
            return False

    @pyqtSlot(str, bytes, bool, result=bool)
    def saveRawToFile(self, file_path: str, data: bytes, append: bool = False) -> bool:
        try:
            mode = "ab" if append else "wb"
            with open(file_path, mode) as f:
                f.write(data)
            return True
        except Exception as e:
            self.error_occurred.emit(f"无法保存文件: {e}")
            return False

    @pyqtSlot(str, list, result=bool)
    def exportToCsv(self, file_path: str, log_entries: list) -> bool:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Time,Type,Direction,Data\n")
                for entry in log_entries:
                    if isinstance(entry, dict):
                        time_str = entry.get("logTime", "")
                        log_type = entry.get("logType", "")
                        data = entry.get("logData", "").replace('"', '""')
                        direction = {"RX": "RX", "TX": "TX"}.get(log_type, "SYSTEM")
                        f.write(f'"{time_str}","{log_type}","{direction}","{data}"\n')
            return True
        except Exception as e:
            self.error_occurred.emit(f"无法保存文件: {e}")
            return False

    @pyqtSlot(str, list, result=bool)
    def exportToTxt(self, file_path: str, log_entries: list) -> bool:
        return self.saveLogToFile(file_path, log_entries, False)

    @pyqtSlot(str, list, result=bool)
    def exportToHex(self, file_path: str, log_entries: list) -> bool:
        """Export log entries as HEX text file with metadata header."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"MOUSART HEX Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                for entry in log_entries:
                    if isinstance(entry, dict):
                        time_str = entry.get("logTime", "")
                        log_type = entry.get("logType", "")
                        data = entry.get("logData", "")
                        direction = {"RX": "<<", "TX": ">>"}.get(log_type, "  ")
                        # Convert text to hex representation
                        hex_str = " ".join(f"{ord(c):02X}" for c in data[:128])
                        if len(data) > 128:
                            hex_str += " ..."
                        f.write(f"[{time_str}] {direction} {hex_str}\n")
            return True
        except Exception as e:
            self.error_occurred.emit(f"无法保存文件: {e}")
            return False

    @pyqtSlot(str, list, str, str, result=bool)
    def exportWithMeta(self, file_path: str, log_entries: list,
                       port_info: str = "", baud_rate: str = "") -> bool:
        """Export with metadata header (port info, baud rate, timestamp)."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"MOUSART Log Export\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if port_info:
                    f.write(f"串口: {port_info}\n")
                if baud_rate:
                    f.write(f"波特率: {baud_rate}\n")
                f.write(f"条目数: {len(log_entries)}\n")
                f.write("=" * 60 + "\n\n")
                for entry in log_entries:
                    if isinstance(entry, dict):
                        time_str = entry.get("logTime", "")
                        log_type = entry.get("logType", "")
                        data = entry.get("logData", "")
                        prefix = {"RX": "<< RX: ", "TX": ">> TX: ", "ERR": "!! ERR: ",
                                  "INFO": "i  INFO: ", "SYS": "#  SYS: "}.get(log_type, "   ")
                        f.write(f"[{time_str}] {prefix}{data}\n")
            return True
        except Exception as e:
            self.error_occurred.emit(f"无法保存文件: {e}")
            return False

    @pyqtSlot(str)
    def startRecording(self, directory: str = ""):
        if self._is_recording:
            self.stopRecording()

        self._record_directory = directory
        if not self._record_directory:
            self._record_directory = os.path.join(os.path.expanduser("~"), "mousart_logs")
        os.makedirs(self._record_directory, exist_ok=True)

        self._file_index = 0
        self._recorded_bytes = 0
        self._is_recording = True
        self._current_log_file = os.path.join(
            self._record_directory,
            f"mousart_rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        self.is_recording_changed.emit()
        self.current_log_file_changed.emit()
        self.recorded_bytes_changed.emit()

    @pyqtSlot()
    def stopRecording(self):
        self._is_recording = False
        self._current_log_file = ""
        self.is_recording_changed.emit()
        self.current_log_file_changed.emit()

    @pyqtSlot(str, bytes, str)
    def recordData(self, direction: str, raw_data: bytes, display_text: str = ""):
        if not self._is_recording:
            return

        # Rotate file if too large
        if self._recorded_bytes >= MAX_RECORD_FILE_SIZE:
            self._file_index += 1
            self._recorded_bytes = 0
            self._current_log_file = os.path.join(
                self._record_directory,
                f"mousart_rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._file_index}.log"
            )
            self.current_log_file_changed.emit()

        try:
            with open(self._current_log_file, "a", encoding="utf-8") as f:
                ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                text = display_text if display_text else raw_data.decode("utf-8", errors="replace")
                f.write(f"[{ts}] {direction}: {text}\n")
            self._recorded_bytes += len(raw_data)
            self.recorded_bytes_changed.emit()
        except Exception:
            pass

    @pyqtSlot(str, str, result=str)
    def getSaveFilePath(self, default_name: str, file_filter: str) -> str:
        path, _ = QFileDialog.getSaveFileName(
            None, "保存文件",
            os.path.join(os.path.expanduser("~"), default_name),
            file_filter)
        return path

    @pyqtSlot(str, str, result=str)
    def getOpenFilePath(self, title: str, file_filter: str) -> str:
        path, _ = QFileDialog.getOpenFileName(
            None, title, os.path.expanduser("~"), file_filter)
        return path

    @pyqtSlot(list, result=bool)
    def saveLogToFileWithDialog(self, log_entries: list) -> bool:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.getSaveFilePath(
            f"mousart_log_{ts}.txt",
            "Text files (*.txt);;CSV files (*.csv);;All files (*)")
        if not path:
            return False
        if path.endswith(".csv"):
            return self.exportToCsv(path, log_entries)
        return self.saveLogToFile(path, log_entries, False)

    @pyqtSlot(result=str)
    def getSaveLogPath(self) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.getSaveFilePath(
            f"mousart_log_{ts}.txt",
            "Text files (*.txt);;CSV files (*.csv);;HEX files (*.hex);;All files (*)")

    @pyqtSlot(result=str)
    def getSendFilePath(self) -> str:
        return self.getOpenFilePath("选择发送文件", "All files (*)")
