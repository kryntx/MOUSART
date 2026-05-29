"""Right data area - two independent panels for Virtual Serial and Hardware Debug."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPlainTextEdit, QLineEdit, QMenu, QSplitter,
                               QDialog, QFormLayout, QCheckBox, QDialogButtonBox,
                               QStackedWidget)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QAction, QTextCursor, QFont, QColor

from mousart.ui.widgets.small_toggle import SmallToggle
from mousart.ui.widgets.small_button import SmallButton
from mousart.ui.widgets.quick_command_bar import QuickCommandBar
from mousart.ui.widgets.data_stats_bar import DataStatsBar

from mousart.utils.constants import MODBUS_FC_OPTIONS, MAX_LOG_ENTRIES
from mousart.utils.hex_display import bytes_to_hex
from datetime import datetime


class LogEntry:
    """Single log entry."""
    __slots__ = ('time', 'log_type', 'data')
    def __init__(self, time_str, log_type, data):
        self.time = time_str
        self.log_type = log_type
        self.data = data


class SinglePanel(QWidget):
    """A single send/receive panel for one mode (virtual or debug)."""

    def __init__(self, parent=None, theme_manager=None, config_manager=None,
                 data_analyzer=None, log_file_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._config_manager = config_manager
        self._data_analyzer = data_analyzer
        self._log_file_manager = log_file_manager

        self._hex_display = False
        self._hex_send = False
        self._show_timestamp = True
        self._show_direction = True
        self._pause_display = False
        self._echo_enabled = False
        self._filter_text = ""
        self._filter_regex = False
        self._timed_send_interval = 1000
        self._show_modbus = False
        self._log_entries = []
        self._manager = None  # Will be set to serial_manager or virtual_manager

        self._build_ui()

    def set_manager(self, manager):
        """Set the serial manager (virtual or hardware) for this panel."""
        self._manager = manager

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setChildrenCollapsible(False)

        # === Receive area ===
        recv_widget = QWidget()
        recv_layout = QVBoxLayout(recv_widget)
        recv_layout.setContentsMargins(2, 2, 2, 2)
        recv_layout.setSpacing(0)

        # Receive toolbar
        recv_toolbar = QHBoxLayout()
        recv_toolbar.setSpacing(3)

        self._hex_display_toggle = SmallToggle("HEX", theme_manager=self._theme_manager)
        self._hex_display_toggle.toggled_custom.connect(lambda v: setattr(self, '_hex_display', v))
        recv_toolbar.addWidget(self._hex_display_toggle)

        self._timestamp_toggle = SmallToggle("时间", theme_manager=self._theme_manager)
        self._timestamp_toggle.active = True
        self._timestamp_toggle.toggled_custom.connect(lambda v: setattr(self, '_show_timestamp', v))
        recv_toolbar.addWidget(self._timestamp_toggle)

        self._direction_toggle = SmallToggle("↕", theme_manager=self._theme_manager)
        self._direction_toggle.active = True
        self._direction_toggle.toggled_custom.connect(lambda v: setattr(self, '_show_direction', v))
        recv_toolbar.addWidget(self._direction_toggle)

        self._pause_toggle = SmallToggle("暂停", theme_manager=self._theme_manager)
        self._pause_toggle.toggled_custom.connect(lambda v: setattr(self, '_pause_display', v))
        recv_toolbar.addWidget(self._pause_toggle)

        sep = QWidget()
        sep.setFixedSize(1, 14)
        sep.setStyleSheet("background: #2a2a4a;")
        recv_toolbar.addWidget(sep)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("搜索...")
        self._search_input.setFixedWidth(100)
        self._search_input.setFixedHeight(20)
        recv_toolbar.addWidget(self._search_input)

        self._filter_btn = SmallButton("过滤", theme_manager=self._theme_manager)
        self._filter_btn.clicked_custom.connect(self._show_filter_menu)
        recv_toolbar.addWidget(self._filter_btn)

        recv_toolbar.addStretch()

        save_btn = SmallButton("保存", theme_manager=self._theme_manager)
        save_btn.clicked_custom.connect(self._save_log)
        recv_toolbar.addWidget(save_btn)

        self._record_toggle = SmallToggle("录制", theme_manager=self._theme_manager)
        self._record_toggle.toggled_custom.connect(self._toggle_recording)
        recv_toolbar.addWidget(self._record_toggle)

        clear_btn = SmallButton("清空", theme_manager=self._theme_manager)
        clear_btn.clicked_custom.connect(self._clear_log)
        recv_toolbar.addWidget(clear_btn)

        recv_layout.addLayout(recv_toolbar)

        # Log view
        self._log_view = QPlainTextEdit()
        self._log_view.setReadOnly(True)
        self._log_view.setMaximumBlockCount(MAX_LOG_ENTRIES)
        font = QFont("monospace")
        font.setPointSize(11)
        self._log_view.setFont(font)
        recv_layout.addWidget(self._log_view, 1)

        splitter.addWidget(recv_widget)

        # === Send area ===
        send_widget = QWidget()
        send_layout = QVBoxLayout(send_widget)
        send_layout.setContentsMargins(2, 2, 2, 2)
        send_layout.setSpacing(0)

        # Send toolbar
        send_toolbar = QHBoxLayout()
        send_toolbar.setSpacing(3)

        send_label = QLabel("发送")
        send_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #8899aa; margin-left: 6px;")
        send_toolbar.addWidget(send_label)

        self._hex_send_toggle = SmallToggle("HEX", theme_manager=self._theme_manager)
        self._hex_send_toggle.toggled_custom.connect(lambda v: setattr(self, '_hex_send', v))
        send_toolbar.addWidget(self._hex_send_toggle)

        self._echo_toggle = SmallToggle("回显", theme_manager=self._theme_manager)
        self._echo_toggle.toggled_custom.connect(lambda v: setattr(self, '_echo_enabled', v))
        send_toolbar.addWidget(self._echo_toggle)

        sep2 = QWidget()
        sep2.setFixedSize(1, 14)
        sep2.setStyleSheet("background: #2a2a4a;")
        send_toolbar.addWidget(sep2)

        self._interval_input = QLineEdit("1000")
        self._interval_input.setFixedWidth(60)
        self._interval_input.setFixedHeight(20)
        self._interval_input.setStyleSheet("font-size: 9px; font-family: monospace;")
        send_toolbar.addWidget(self._interval_input)
        ms_label = QLabel("ms")
        ms_label.setStyleSheet("font-size: 9px; color: #8899aa;")
        send_toolbar.addWidget(ms_label)

        self._timed_toggle = SmallToggle("定时", theme_manager=self._theme_manager)
        self._timed_toggle.toggled_custom.connect(self._toggle_timed_send)
        send_toolbar.addWidget(self._timed_toggle)

        file_btn = SmallButton("文件", theme_manager=self._theme_manager)
        file_btn.clicked_custom.connect(self._send_file)
        send_toolbar.addWidget(file_btn)

        self._modbus_toggle = SmallToggle("Modbus", theme_manager=self._theme_manager)
        self._modbus_toggle.toggled_custom.connect(self._toggle_modbus)
        send_toolbar.addWidget(self._modbus_toggle)

        send_toolbar.addStretch()

        self._send_btn = SmallButton("发送", theme_manager=self._theme_manager, accent=True)
        self._send_btn.set_btn_enabled(False)
        self._send_btn.clicked_custom.connect(self._do_send)
        send_toolbar.addWidget(self._send_btn)

        send_layout.addLayout(send_toolbar)

        # Modbus panel
        self._modbus_widget = self._build_modbus_panel()
        self._modbus_widget.setVisible(False)
        send_layout.addWidget(self._modbus_widget)

        # Send text area
        self._send_text = QPlainTextEdit()
        self._send_text.setPlaceholderText("Ctrl+Enter 发送")
        self._send_text.setMaximumHeight(120)
        font2 = QFont("monospace")
        font2.setPointSize(12)
        self._send_text.setFont(font2)
        send_layout.addWidget(self._send_text, 1)

        splitter.addWidget(send_widget)
        splitter.setSizes([400, 200])

        layout.addWidget(splitter, 1)

        # Quick command bar
        self._quick_cmd_bar = QuickCommandBar(
            theme_manager=self._theme_manager,
            config_manager=self._config_manager
        )
        self._quick_cmd_bar.send_command.connect(self._send_quick_command)
        self._quick_cmd_bar.add_requested.connect(self._add_quick_command)
        self._quick_cmd_bar.edit_requested.connect(self._edit_quick_command)
        layout.addWidget(self._quick_cmd_bar)

        # Stats bar
        self._stats_bar = DataStatsBar(theme_manager=self._theme_manager)
        layout.addWidget(self._stats_bar)

        # Keyboard shortcut
        self._send_text.installEventFilter(self)

    def _build_modbus_panel(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        layout.addWidget(QLabel("Addr:"))
        self._modbus_addr = QLineEdit("1")
        self._modbus_addr.setFixedWidth(36)
        layout.addWidget(self._modbus_addr)

        layout.addWidget(QLabel("FC:"))
        from mousart.ui.widgets.styled_combo_box import StyledComboBox
        self._modbus_fc_combo = StyledComboBox(theme_manager=self._theme_manager)
        for name, _ in MODBUS_FC_OPTIONS:
            self._modbus_fc_combo.addItem(name)
        layout.addWidget(self._modbus_fc_combo)

        layout.addWidget(QLabel("Addr:"))
        self._modbus_start = QLineEdit("0")
        self._modbus_start.setFixedWidth(50)
        layout.addWidget(self._modbus_start)

        layout.addWidget(QLabel("Qty:"))
        self._modbus_qty = QLineEdit("1")
        self._modbus_qty.setFixedWidth(36)
        layout.addWidget(self._modbus_qty)

        build_btn = SmallButton("构建", theme_manager=self._theme_manager, accent=True)
        build_btn.clicked_custom.connect(self._build_modbus_frame)
        layout.addWidget(build_btn)
        layout.addStretch()

        return widget

    def eventFilter(self, obj, event):
        if obj == self._send_text and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._do_send()
                return True
        return super().eventFilter(obj, event)

    def add_log_entry(self, log_type, data):
        """Add a log entry to this panel."""
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = LogEntry(ts, log_type, data)
        self._log_entries.append(entry)

        if not self._pause_display:
            color_map = {"RX": "#4ec9b0", "TX": "#569cd6", "ERR": "#f44747", "INFO": "#dcdcaa", "SYS": "#9cdcfe"}
            direction_map = {"RX": "<<", "TX": ">>", "ERR": "!!", "INFO": "i", "SYS": "#"}
            color = color_map.get(log_type, "#8899aa")
            direction = direction_map.get(log_type, "?")

            parts = []
            if self._show_timestamp:
                parts.append(f'<span style="color:#8899aa;">{ts}</span>')
            if self._show_direction:
                parts.append(f'<span style="color:{color};font-weight:bold;">{direction}</span>')
            parts.append(f'<span style="color:{color if log_type == "ERR" else "#e0e0e0"};">{data}</span>')

            self._log_view.appendHtml("  ".join(parts))
            cursor = self._log_view.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self._log_view.setTextCursor(cursor)

        # Auto-record
        if self._log_file_manager and self._log_file_manager.isRecording:
            raw = data.encode("utf-8", errors="replace")
            self._log_file_manager.recordData(log_type, raw, data)

    def on_data_received(self, text, raw):
        """Handle received data from serial manager."""
        display = bytes_to_hex(raw, " ") if self._hex_display else text
        if self._filter_text:
            if self._data_analyzer and not self._data_analyzer.matchFilter(display, self._filter_text, self._filter_regex):
                return
        self.add_log_entry("RX", display)

    def on_error(self, error):
        self.add_log_entry("ERR", error)

    def on_timed_send_completed(self, data):
        if self._echo_enabled:
            self.add_log_entry("TX", data)

    def on_port_event(self, event_type, info=""):
        if event_type == "opened":
            self.add_log_entry("SYS", f"已连接: {info}")
        elif event_type == "closed":
            self.add_log_entry("SYS", "已断开")
        elif event_type == "vstarted":
            self.add_log_entry("INFO", f"虚拟串口已启动 {info}")
        elif event_type == "vstopped":
            self.add_log_entry("INFO", "虚拟串口已关闭")
        self._update_send_btn()

    def update_send_state(self, is_active):
        """Update send button state."""
        self._send_btn.set_btn_enabled(is_active)

    def _do_send(self):
        if not self._manager:
            return
        text = self._send_text.toPlainText()
        if not text:
            return
        is_active = self._manager.isOpen if hasattr(self._manager, 'isOpen') else self._manager.isActive
        if not is_active:
            return
        result = self._manager.sendData(text, self._hex_send)
        if result > 0 and self._echo_enabled:
            display = self._data_analyzer.textToHex(text) if self._hex_send else text
            self.add_log_entry("TX", display)

    def _send_quick_command(self, data, hex_mode):
        if not self._manager:
            return
        is_active = self._manager.isOpen if hasattr(self._manager, 'isOpen') else self._manager.isActive
        if not is_active:
            return
        self._manager.sendData(data, hex_mode)
        if self._echo_enabled:
            display = self._data_analyzer.textToHex(data) if hex_mode else data
            self.add_log_entry("TX", display)

    def _toggle_timed_send(self, v):
        if not self._manager:
            return
        if v:
            is_active = self._manager.isOpen if hasattr(self._manager, 'isOpen') else self._manager.isActive
            text = self._send_text.toPlainText()
            if is_active and text:
                try:
                    interval = int(self._interval_input.text())
                except ValueError:
                    interval = 1000
                self._manager.startTimedSend(text, self._hex_send, interval, -1)
        else:
            self._manager.stopTimedSend()

    def _toggle_recording(self, v):
        if self._log_file_manager:
            if v:
                self._log_file_manager.startRecording()
            else:
                self._log_file_manager.stopRecording()

    def _toggle_modbus(self, v):
        self._show_modbus = v
        self._modbus_widget.setVisible(v)

    def _send_file(self):
        if self._log_file_manager and self._manager and hasattr(self._manager, 'sendFileData'):
            path = self._log_file_manager.getSendFilePath()
            if path:
                result = self._manager.sendFileData(path, self._hex_send)
                self.add_log_entry("INFO", f"文件发送: {result}")

    def _save_log(self):
        if not self._log_file_manager:
            return
        path = self._log_file_manager.getSaveLogPath()
        if not path:
            return
        entries = [{"logTime": e.time, "logType": e.log_type, "logData": e.data} for e in self._log_entries]
        if path.endswith(".csv"):
            self._log_file_manager.exportToCsv(path, entries)
        else:
            self._log_file_manager.saveLogToFile(path, entries)

    def _clear_log(self):
        self._log_entries.clear()
        self._log_view.clear()

    def _show_filter_menu(self):
        menu = QMenu(self)
        menu.addAction("清除过滤", lambda: self._set_filter("", False))
        menu.addAction("仅含关键字...", lambda: self._set_filter(self._search_input.text(), False))
        menu.addAction("正则匹配...", lambda: self._set_filter(self._search_input.text(), True))
        menu.exec(self._filter_btn.mapToGlobal(self._filter_btn.rect().bottomLeft()))

    def _set_filter(self, text, regex):
        self._filter_text = text
        self._filter_regex = regex
        if text:
            self._filter_btn.setText("过滤✓")
            self._filter_btn.set_accent(True)
        else:
            self._filter_btn.setText("过滤")
            self._filter_btn.set_accent(False)

    def _build_modbus_frame(self):
        if not self._data_analyzer:
            return
        try:
            addr = int(self._modbus_addr.text())
            fc_idx = self._modbus_fc_combo.currentIndex()
            fc = MODBUS_FC_OPTIONS[fc_idx][1] if fc_idx < len(MODBUS_FC_OPTIONS) else 3
            start = int(self._modbus_start.text())
            qty = int(self._modbus_qty.text())
            frame = self._data_analyzer.buildModbusRtuFrame(addr, fc, start, qty)
            self._send_text.setPlainText(self._data_analyzer.bytesToHex(frame, " "))
        except ValueError:
            pass

    def _add_quick_command(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("添加快捷命令")
        dialog.setMinimumWidth(300)
        layout = QFormLayout(dialog)
        name_input = QLineEdit()
        data_input = QLineEdit()
        hex_check = QCheckBox("HEX模式")
        layout.addRow("名称:", name_input)
        layout.addRow("数据:", data_input)
        layout.addRow(hex_check)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if name_input.text() and self._config_manager:
                self._config_manager.addQuickCommand(name_input.text(), data_input.text(), hex_check.isChecked())

    def _edit_quick_command(self, index):
        if not self._config_manager or index < 0 or index >= len(self._config_manager.quick_commands):
            return
        cmd = self._config_manager.quick_commands[index]
        dialog = QDialog(self)
        dialog.setWindowTitle("编辑快捷命令")
        dialog.setMinimumWidth(300)
        layout = QFormLayout(dialog)
        name_input = QLineEdit(cmd.get("name", ""))
        data_input = QLineEdit(cmd.get("data", ""))
        hex_check = QCheckBox("HEX模式")
        hex_check.setChecked(cmd.get("hex", False))
        layout.addRow("名称:", name_input)
        layout.addRow("数据:", data_input)
        layout.addRow(hex_check)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._config_manager.updateQuickCommand(index, name_input.text(), data_input.text(), hex_check.isChecked())

    def _update_send_btn(self):
        if self._manager:
            is_active = self._manager.isOpen if hasattr(self._manager, 'isOpen') else self._manager.isActive
            self._send_btn.set_btn_enabled(is_active)

    def update_stats(self):
        if self._manager:
            rx = self._manager.rxBytes
            tx = self._manager.txBytes
            rx_rate = self._manager.rxRate
            tx_rate = self._manager.txRate
            self._stats_bar.update_stats(
                self._format_bytes(rx), self._format_bytes(tx),
                self._format_rate(rx_rate), self._format_rate(tx_rate)
            )

    def refresh_quick_commands(self):
        self._quick_cmd_bar.refresh()

    @staticmethod
    def _format_bytes(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.2f} MB"

    @staticmethod
    def _format_rate(bps):
        if bps < 1024: return f"{bps:.0f} B/s"
        if bps < 1048576: return f"{bps/1024:.1f} KB/s"
        return f"{bps/1048576:.2f} MB/s"

    def apply_theme(self, theme_manager):
        self._theme_manager = theme_manager
        recv_bg = theme_manager.get_color_hex("receiveBg")
        send_bg = theme_manager.get_color_hex("sendBg")
        border = theme_manager.get_color_hex("border")
        text = theme_manager.get_color_hex("textPrimary")

        self._log_view.setStyleSheet(f"""
            QPlainTextEdit {{
                background: {recv_bg};
                color: {text};
                border: 1px solid {border};
                border-radius: 6px;
            }}
        """)
        self._send_text.setStyleSheet(f"""
            QPlainTextEdit {{
                background: {send_bg};
                color: {text};
                border: 1px solid {border};
                border-radius: 6px;
            }}
        """)
        for toggle in self.findChildren(SmallToggle):
            toggle.set_theme_manager(theme_manager)
        for btn in self.findChildren(SmallButton):
            btn.set_theme_manager(theme_manager)


class DataPanel(QWidget):
    """Right panel with two independent panels: Virtual Serial and Hardware Debug."""

    def __init__(self, parent=None, theme_manager=None, serial_manager=None,
                 virtual_manager=None, config_manager=None, data_analyzer=None,
                 log_file_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._serial_manager = serial_manager
        self._virtual_manager = virtual_manager
        self._config_manager = config_manager
        self._data_analyzer = data_analyzer
        self._log_file_manager = log_file_manager

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Stacked widget to switch between two independent panels
        self._stack = QStackedWidget()

        # Panel 0: Virtual Serial
        self._virtual_panel = SinglePanel(
            theme_manager=self._theme_manager,
            config_manager=self._config_manager,
            data_analyzer=self._data_analyzer,
            log_file_manager=self._log_file_manager
        )
        self._virtual_panel.set_manager(self._virtual_manager)

        # Panel 1: Hardware Debug
        self._debug_panel = SinglePanel(
            theme_manager=self._theme_manager,
            config_manager=self._config_manager,
            data_analyzer=self._data_analyzer,
            log_file_manager=self._log_file_manager
        )
        self._debug_panel.set_manager(self._serial_manager)

        self._stack.addWidget(self._virtual_panel)  # index 0
        self._stack.addWidget(self._debug_panel)     # index 1

        layout.addWidget(self._stack)

    def set_mode(self, mode):
        """Switch between virtual (0) and debug (1) panels."""
        self._stack.setCurrentIndex(mode)

    def _connect_signals(self):
        # Virtual manager signals
        if self._virtual_manager:
            self._virtual_manager.data_received.connect(self._virtual_panel.on_data_received)
            self._virtual_manager.error_occurred.connect(self._virtual_panel.on_error)
            self._virtual_manager.is_active_changed.connect(
                lambda: self._virtual_panel.on_port_event(
                    "vstarted" if self._virtual_manager.isActive else "vstopped",
                    self._virtual_manager.externalPort if self._virtual_manager.isActive else ""
                ))
            self._virtual_manager.timed_send_completed.connect(self._virtual_panel.on_timed_send_completed)
            self._virtual_manager.stats_changed.connect(self._virtual_panel.update_stats)

        # Serial manager signals
        if self._serial_manager:
            self._serial_manager.data_received.connect(self._debug_panel.on_data_received)
            self._serial_manager.error_occurred.connect(self._debug_panel.on_error)
            self._serial_manager.port_opened.connect(
                lambda n: self._debug_panel.on_port_event("opened", n))
            self._serial_manager.port_closed.connect(
                lambda: self._debug_panel.on_port_event("closed"))
            self._serial_manager.is_open_changed.connect(
                lambda: self._debug_panel.update_send_state(
                    self._serial_manager.isOpen if self._serial_manager else False
                ))
            self._serial_manager.timed_send_completed.connect(self._debug_panel.on_timed_send_completed)
            self._serial_manager.stats_changed.connect(self._debug_panel.update_stats)

        # Config manager signals
        if self._config_manager:
            self._config_manager.quick_commands_changed.connect(self._virtual_panel.refresh_quick_commands)
            self._config_manager.quick_commands_changed.connect(self._debug_panel.refresh_quick_commands)

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self.setStyleSheet(f"background: {tm.get_color_hex('bgPrimary')};")
        self._virtual_panel.apply_theme(tm)
        self._debug_panel.apply_theme(tm)
