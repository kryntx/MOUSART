"""Right data area with receive log, send area, quick commands, and stats."""
from mousart.qt_compat import *

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

    def __init__(self, time_str: str, log_type: str, data: str):
        self.time = time_str
        self.log_type = log_type
        self.data = data


class DataPanel(QWidget):
    """Right panel with receive log, send area, Modbus, quick commands, and stats."""

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

        self._mode = 0
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

        self._virtual_log = []
        self._debug_log = []

        self._build_ui()
        self._connect_signals()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_all_styles()

    def set_mode(self, mode: int):
        self._mode = mode
        self._mode_label.setText("模拟串口" if mode == 0 else "串口调试")
        self._refresh_log_view()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(0)

        # Use a splitter for receive/send areas
        splitter = QSplitter(Qt_Orientation_Vertical)
        splitter.setChildrenCollapsible(False)

        # --- Receive area ---
        recv_widget = QWidget()
        recv_layout = QVBoxLayout(recv_widget)
        recv_layout.setContentsMargins(2, 2, 2, 2)
        recv_layout.setSpacing(0)

        # Receive toolbar
        recv_toolbar = QHBoxLayout()
        recv_toolbar.setSpacing(3)

        self._mode_label = QLabel("模拟串口")
        self._mode_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #8899aa; margin-left: 6px;")
        recv_toolbar.addWidget(self._mode_label)

        self._hex_display_toggle = SmallToggle("HEX", theme_manager=self._theme_manager)
        self._hex_display_toggle.toggled_custom.connect(self._toggle_hex_display)
        recv_toolbar.addWidget(self._hex_display_toggle)

        self._timestamp_toggle = SmallToggle("时间", theme_manager=self._theme_manager)
        self._timestamp_toggle.active = True
        self._timestamp_toggle.toggled_custom.connect(self._toggle_timestamp)
        recv_toolbar.addWidget(self._timestamp_toggle)

        self._direction_toggle = SmallToggle("↕", theme_manager=self._theme_manager)
        self._direction_toggle.active = True
        self._direction_toggle.toggled_custom.connect(self._toggle_direction)
        recv_toolbar.addWidget(self._direction_toggle)

        self._pause_toggle = SmallToggle("暂停", theme_manager=self._theme_manager)
        self._pause_toggle.toggled_custom.connect(self._toggle_pause)
        recv_toolbar.addWidget(self._pause_toggle)

        sep = QWidget()
        sep.setFixedSize(1, 14)
        sep.setStyleSheet("background: #2a2a4a;")
        recv_toolbar.addWidget(sep)

        # Search
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("搜索...")
        self._search_input.setFixedWidth(100)
        self._search_input.setFixedHeight(20)
        recv_toolbar.addWidget(self._search_input)

        # Filter button
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

        # --- Send area ---
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
        self._hex_send_toggle.toggled_custom.connect(self._toggle_hex_send)
        send_toolbar.addWidget(self._hex_send_toggle)

        self._echo_toggle = SmallToggle("回显", theme_manager=self._theme_manager)
        self._echo_toggle.toggled_custom.connect(self._toggle_echo)
        send_toolbar.addWidget(self._echo_toggle)

        sep2 = QWidget()
        sep2.setFixedSize(1, 14)
        sep2.setStyleSheet("background: #2a2a4a;")
        send_toolbar.addWidget(sep2)

        # Timed send
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

    def _connect_signals(self):
        if self._serial_manager:
            self._serial_manager.data_received.connect(self._on_serial_data)
            self._serial_manager.error_occurred.connect(
                lambda e: self._add_log_entry("ERR", e, self._debug_log))
            self._serial_manager.timed_send_completed.connect(
                lambda d: self._on_timed_send_completed(d, self._debug_log))
            self._serial_manager.port_opened.connect(
                lambda n: self._add_log_entry("SYS", f"已连接: {n}", self._debug_log))
            self._serial_manager.port_closed.connect(
                lambda: self._add_log_entry("SYS", "已断开", self._debug_log))
            self._serial_manager.is_open_changed.connect(self._update_send_btn)
            self._serial_manager.stats_changed.connect(self._update_stats)

        if self._virtual_manager:
            self._virtual_manager.data_received.connect(self._on_virtual_data)
            self._virtual_manager.error_occurred.connect(
                lambda e: self._add_log_entry("ERR", e, self._virtual_log))
            self._virtual_manager.is_active_changed.connect(
                lambda: self._on_virtual_state(self._virtual_log))
            self._virtual_manager.timed_send_completed.connect(
                lambda d: self._on_timed_send_completed(d, self._virtual_log))
            self._virtual_manager.stats_changed.connect(self._update_stats)

        if self._config_manager:
            self._config_manager.quick_commands_changed.connect(
                self._quick_cmd_bar.refresh)

    def eventFilter(self, obj, event):
        if obj == self._send_text and event.type() == QEvent_Type_KeyPress:
            if event.key() == Qt_Key_Return and event.modifiers() & Qt_KeyboardModifier_ControlModifier:
                self._do_send()
                return True
        return super().eventFilter(obj, event)

    def _add_log_entry(self, log_type: str, data: str, log_list: list):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = LogEntry(ts, log_type, data)
        log_list.append(entry)

        if not self._pause_display:
            # Color based on type
            color_map = {
                "RX": "#4ec9b0", "TX": "#569cd6", "ERR": "#f44747",
                "INFO": "#dcdcaa", "SYS": "#9cdcfe"
            }
            direction_map = {
                "RX": "<<", "TX": ">>", "ERR": "!!", "INFO": "i", "SYS": "#"
            }

            color = color_map.get(log_type, "#8899aa")
            direction = direction_map.get(log_type, "?")

            parts = []
            if self._show_timestamp:
                parts.append(f'<span style="color:#8899aa;">{ts}</span>')
            if self._show_direction:
                parts.append(f'<span style="color:{color};font-weight:bold;">{direction}</span>')
            parts.append(f'<span style="color:{color if log_type == "ERR" else "#e0e0e0"};">{data}</span>')

            self._log_view.appendHtml("  ".join(parts))

            # Auto-scroll
            cursor = self._log_view.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self._log_view.setTextCursor(cursor)

        # Auto-record
        if self._log_file_manager and self._log_file_manager.isRecording:
            raw = data.encode("utf-8", errors="replace")
            self._log_file_manager.recordData(log_type, raw, data)

    def _on_serial_data(self, text: str, raw: bytes):
        display = bytes_to_hex(raw, " ") if self._hex_display else text
        if self._filter_text:
            if self._data_analyzer and not self._data_analyzer.matchFilter(display, self._filter_text, self._filter_regex):
                return
        self._add_log_entry("RX", display, self._debug_log)

    def _on_virtual_data(self, text: str, raw: bytes):
        display = bytes_to_hex(raw, " ") if self._hex_display else text
        if self._filter_text:
            if self._data_analyzer and not self._data_analyzer.matchFilter(display, self._filter_text, self._filter_regex):
                return
        self._add_log_entry("RX", display, self._virtual_log)

    def _on_virtual_state(self, log_list):
        if self._virtual_manager and self._virtual_manager.isActive:
            self._add_log_entry("INFO", f"虚拟串口已启动 {self._virtual_manager.externalPort}", log_list)
        else:
            self._add_log_entry("INFO", "虚拟串口已关闭", log_list)
        self._update_send_btn()

    def _on_timed_send_completed(self, data, log_list):
        if self._echo_enabled:
            self._add_log_entry("TX", data, log_list)

    def _do_send(self):
        text = self._send_text.toPlainText()
        if not text:
            return
        manager = self._virtual_manager if self._mode == 0 else self._serial_manager
        if not manager:
            return

        is_active = manager.isActive if self._mode == 0 else manager.isOpen
        if not is_active:
            return

        result = manager.sendData(text, self._hex_send)
        if result > 0 and self._echo_enabled:
            display = self._data_analyzer.textToHex(text) if self._hex_send else text
            log_list = self._virtual_log if self._mode == 0 else self._debug_log
            self._add_log_entry("TX", display, log_list)

    def _send_quick_command(self, data: str, hex_mode: bool):
        manager = self._virtual_manager if self._mode == 0 else self._serial_manager
        if not manager:
            return
        is_active = manager.isActive if self._mode == 0 else manager.isOpen
        if not is_active:
            return

        manager.sendData(data, hex_mode)
        if self._echo_enabled:
            display = self._data_analyzer.textToHex(data) if hex_mode else data
            log_list = self._virtual_log if self._mode == 0 else self._debug_log
            self._add_log_entry("TX", display, log_list)

    def _toggle_hex_display(self, v):
        self._hex_display = v

    def _toggle_hex_send(self, v):
        self._hex_send = v

    def _toggle_timestamp(self, v):
        self._show_timestamp = v

    def _toggle_direction(self, v):
        self._show_direction = v

    def _toggle_pause(self, v):
        self._pause_display = v

    def _toggle_echo(self, v):
        self._echo_enabled = v

    def _toggle_modbus(self, v):
        self._show_modbus = v
        self._modbus_widget.setVisible(v)

    def _toggle_timed_send(self, v):
        manager = self._virtual_manager if self._mode == 0 else self._serial_manager
        if not manager:
            return

        if v:
            is_active = manager.isActive if self._mode == 0 else manager.isOpen
            text = self._send_text.toPlainText()
            if is_active and text:
                try:
                    interval = int(self._interval_input.text())
                except ValueError:
                    interval = 1000
                manager.startTimedSend(text, self._hex_send, interval, -1)
        else:
            manager.stopTimedSend()

    def _toggle_recording(self, v):
        if self._log_file_manager:
            if v:
                self._log_file_manager.startRecording()
            else:
                self._log_file_manager.stopRecording()

    def _send_file(self):
        if self._log_file_manager and self._serial_manager:
            path = self._log_file_manager.getSendFilePath()
            if path:
                result = self._serial_manager.sendFileData(path, self._hex_send)
                self._add_log_entry("INFO", f"文件发送: {result}", self._debug_log)

    def _save_log(self):
        if not self._log_file_manager:
            return
        path = self._log_file_manager.getSaveLogPath()
        if not path:
            return
        log_list = self._virtual_log if self._mode == 0 else self._debug_log
        entries = [{"logTime": e.time, "logType": e.log_type, "logData": e.data} for e in log_list]
        if path.endswith(".csv"):
            self._log_file_manager.exportToCsv(path, entries)
        else:
            self._log_file_manager.saveLogToFile(path, entries)

    def _clear_log(self):
        if self._mode == 0:
            self._virtual_log.clear()
        else:
            self._debug_log.clear()
        self._log_view.clear()

    def _show_filter_menu(self):
        menu = QMenu(self)
        menu.addAction("清除过滤", lambda: self._set_filter("", False))
        menu.addAction("仅含关键字...", lambda: self._set_filter(self._search_input.text(), False))
        menu.addAction("正则匹配...", lambda: self._set_filter(self._search_input.text(), True))
        menu.exec(self._filter_btn.mapToGlobal(self._filter_btn.rect().bottomLeft()))

    def _set_filter(self, text: str, regex: bool):
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
        name_input.setPlaceholderText("AT")
        data_input = QLineEdit()
        data_input.setPlaceholderText("AT\\r\\n")
        hex_check = QCheckBox("HEX模式")

        layout.addRow("名称:", name_input)
        layout.addRow("数据:", data_input)
        layout.addRow(hex_check)

        buttons = QDialogButtonBox(QDialogButtonBox_StandardButton_Ok | QDialogButtonBox_StandardButton_Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog_DialogCode_Accepted:
            if name_input.text() and self._config_manager:
                self._config_manager.addQuickCommand(
                    name_input.text(), data_input.text(), hex_check.isChecked())

    def _edit_quick_command(self, index: int):
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

        buttons = QDialogButtonBox(QDialogButtonBox_StandardButton_Ok | QDialogButtonBox_StandardButton_Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog_DialogCode_Accepted:
            self._config_manager.updateQuickCommand(
                index, name_input.text(), data_input.text(), hex_check.isChecked())

    def _refresh_log_view(self):
        self._log_view.clear()
        log_list = self._virtual_log if self._mode == 0 else self._debug_log
        for entry in log_list:
            color_map = {
                "RX": "#4ec9b0", "TX": "#569cd6", "ERR": "#f44747",
                "INFO": "#dcdcaa", "SYS": "#9cdcfe"
            }
            direction_map = {"RX": "<<", "TX": ">>", "ERR": "!!", "INFO": "i", "SYS": "#"}
            color = color_map.get(entry.log_type, "#8899aa")
            direction = direction_map.get(entry.log_type, "?")
            parts = []
            if self._show_timestamp:
                parts.append(f'<span style="color:#8899aa;">{entry.time}</span>')
            if self._show_direction:
                parts.append(f'<span style="color:{color};font-weight:bold;">{direction}</span>')
            parts.append(f'<span style="color:{color if entry.log_type == "ERR" else "#e0e0e0"};">{entry.data}</span>')
            self._log_view.appendHtml("  ".join(parts))

    def _update_send_btn(self):
        if self._mode == 0:
            active = self._virtual_manager.isActive if self._virtual_manager else False
        else:
            active = self._serial_manager.isOpen if self._serial_manager else False
        self._send_btn.set_btn_enabled(active)

    def _update_stats(self):
        if self._mode == 0:
            mgr = self._virtual_manager
        else:
            mgr = self._serial_manager
        if not mgr:
            return
        self._stats_bar.update_stats(
            self._format_bytes(mgr.rxBytes),
            self._format_bytes(mgr.txBytes),
            self._format_rate(mgr.rxRate),
            self._format_rate(mgr.txRate)
        )

    @staticmethod
    def _format_bytes(b: int) -> str:
        if b < 1024:
            return f"{b} B"
        if b < 1048576:
            return f"{b / 1024:.1f} KB"
        return f"{b / 1048576:.2f} MB"

    @staticmethod
    def _format_rate(bps: float) -> str:
        if bps < 1024:
            return f"{bps:.0f} B/s"
        if bps < 1048576:
            return f"{bps / 1024:.1f} KB/s"
        return f"{bps / 1048576:.2f} MB/s"

    def _update_all_styles(self):
        if not self._theme_manager:
            return
        recv_bg = self._theme_manager.get_color_hex("receiveBg")
        send_bg = self._theme_manager.get_color_hex("sendBg")
        border = self._theme_manager.get_color_hex("border")
        text = self._theme_manager.get_color_hex("textPrimary")

        self.setStyleSheet(f"background: {self._theme_manager.get_color_hex('bgPrimary')};")
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
        self._search_input.setStyleSheet(f"""
            QLineEdit {{
                background: {self._theme_manager.get_color_hex('bgTertiary')};
                color: {text};
                border: 1px solid {border};
                border-radius: 10px;
                padding: 2px 6px;
                font-size: 9px;
            }}
        """)
        self._interval_input.setStyleSheet(f"""
            QLineEdit {{
                background: {self._theme_manager.get_color_hex('bgTertiary')};
                color: {text};
                border: 1px solid {border};
                border-radius: 10px;
                padding: 2px 6px;
                font-size: 9px;
                font-family: monospace;
            }}
        """)
        self._modbus_widget.setStyleSheet(f"background: {self._theme_manager.get_color_hex('bgTertiary')};")

        for toggle in self.findChildren(SmallToggle):
            toggle.set_theme_manager(self._theme_manager)
        for btn in self.findChildren(SmallButton):
            btn.set_theme_manager(self._theme_manager)
