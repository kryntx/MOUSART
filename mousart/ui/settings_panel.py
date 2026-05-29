"""Left sidebar settings panel with mode selector, serial config, and profiles."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QScrollArea, QFrame, QPushButton)
from PyQt6.QtCore import pyqtSignal, Qt

from mousart.ui.widgets.mode_button import ModeButton
from mousart.ui.widgets.action_button import ActionButton
from mousart.ui.widgets.styled_combo_box import StyledComboBox
from mousart.ui.widgets.editable_combo_box import EditableComboBox
from mousart.ui.widgets.small_toggle import SmallToggle
from mousart.ui.widgets.small_button import SmallButton
from mousart.ui.widgets.pin_control_bar import PinControlBar
from mousart.ui.widgets.auto_reply_panel import AutoReplyPanel

from mousart.utils.constants import (BAUD_RATES, DATA_BITS_LIST, STOP_BITS_LIST,
                                       PARITY_LIST, FLOW_CONTROL_LIST, ENCODING_LIST)


class SettingsPanel(QWidget):
    """Left sidebar with mode selector, serial port configuration, and profiles."""

    mode_changed = pyqtSignal(int)

    def __init__(self, parent=None, theme_manager=None, serial_manager=None,
                 virtual_manager=None, config_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._serial_manager = serial_manager
        self._virtual_manager = virtual_manager
        self._config_manager = config_manager
        self._mode = 0  # 0=virtual, 1=debug
        self._selected_port = 0
        self._selected_encoding = 0

        self.setMinimumWidth(220)
        self.setFixedWidth(280)

        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        self._layout = QVBoxLayout(content)
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.setSpacing(8)

        self._build_mode_selector()
        self._build_separator()
        self._build_virtual_controls()
        self._build_debug_controls()
        self._build_auto_reply()
        self._build_profile_section()
        self._layout.addStretch()
        self._build_status_bar()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Connect signals
        self._connect_signals()
        self._update_mode_visibility()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_all_styles()

    def _build_mode_selector(self):
        header = QLabel("模式 Mode")
        header.setStyleSheet("font-size: 11px; font-weight: bold; color: #8899aa;")
        self._layout.addWidget(header)

        row = QHBoxLayout()
        row.setSpacing(4)

        self._virtual_btn = ModeButton("模拟串口", "Virtual", theme_manager=self._theme_manager)
        self._debug_btn = ModeButton("串口调试", "Debug", theme_manager=self._theme_manager)
        self._virtual_btn.isActive = True

        self._virtual_btn.clicked_custom.connect(lambda: self._set_mode(0))
        self._debug_btn.clicked_custom.connect(lambda: self._set_mode(1))

        row.addWidget(self._virtual_btn)
        row.addWidget(self._debug_btn)
        self._layout.addLayout(row)

    def _build_separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: #2a2a4a; max-height: 1px;")
        self._layout.addWidget(sep)
        self._separator = sep

    def _build_virtual_controls(self):
        self._virtual_widget = QWidget()
        layout = QVBoxLayout(self._virtual_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QLabel("虚拟串口 Virtual Port")
        header.setStyleSheet("font-size: 11px; font-weight: bold; color: #8899aa;")
        layout.addWidget(header)

        desc = QLabel("MOUSART 作为串口A端收发数据，\nB端供外部程序或设备连接")
        desc.setStyleSheet("font-size: 10px; color: #8899aa;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # External port display
        self._ext_port_widget = QWidget()
        ext_layout = QVBoxLayout(self._ext_port_widget)
        ext_layout.setContentsMargins(8, 6, 8, 6)
        ext_layout.addWidget(QLabel("外部端口 (B端)"))
        self._ext_port_label = QLabel("/tmp/mousart_vport")
        self._ext_port_label.setStyleSheet("font-size: 14px; font-family: monospace; font-weight: bold; color: #00d4aa;")
        ext_layout.addWidget(self._ext_port_label)
        hint = QLabel("将此路径提供给外部程序连接")
        hint.setStyleSheet("font-size: 9px; color: #8899aa;")
        ext_layout.addWidget(hint)
        self._ext_port_widget.setVisible(False)
        layout.addWidget(self._ext_port_widget)

        # Encoding
        enc_label = QLabel("接收编码 Encoding")
        enc_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(enc_label)

        self._virtual_enc_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._virtual_enc_combo.addItems(ENCODING_LIST)
        self._virtual_enc_combo.currentIndexChanged.connect(
            lambda i: self._virtual_manager.setReceiveEncoding(ENCODING_LIST[i]) if self._virtual_manager else None)
        layout.addWidget(self._virtual_enc_combo)

        # Newline options
        nl_row = QHBoxLayout()
        nl_label = QLabel("发送换行")
        nl_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        nl_row.addWidget(nl_label)
        nl_row.addStretch()

        self._v_cr_toggle = SmallToggle("CR", theme_manager=self._theme_manager)
        self._v_lf_toggle = SmallToggle("LF", theme_manager=self._theme_manager)
        self._v_cr_toggle.active = True
        self._v_lf_toggle.active = True
        self._v_cr_toggle.toggled_custom.connect(
            lambda v: self._virtual_manager.setNewlineCr(v) if self._virtual_manager else None)
        self._v_lf_toggle.toggled_custom.connect(
            lambda v: self._virtual_manager.setNewlineLf(v) if self._virtual_manager else None)
        nl_row.addWidget(self._v_cr_toggle)
        nl_row.addWidget(self._v_lf_toggle)
        layout.addLayout(nl_row)

        # Start/Stop button
        self._virtual_action_btn = ActionButton("启动 Start", theme_manager=self._theme_manager)
        self._virtual_action_btn.clicked_custom.connect(self._toggle_virtual)
        layout.addWidget(self._virtual_action_btn)

        self._layout.addWidget(self._virtual_widget)

    def _build_debug_controls(self):
        self._debug_widget = QWidget()
        layout = QVBoxLayout(self._debug_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QLabel("串口参数 Serial Config")
        header.setStyleSheet("font-size: 11px; font-weight: bold; color: #8899aa;")
        layout.addWidget(header)

        # Port selector
        port_label = QLabel("端口 Port")
        port_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(port_label)

        port_row = QHBoxLayout()
        self._port_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._port_combo.currentIndexChanged.connect(lambda i: setattr(self, '_selected_port', i))
        port_row.addWidget(self._port_combo, 1)

        refresh_btn = QPushButton("↻")
        refresh_btn.setFixedSize(32, 28)
        refresh_btn.setCursor(self.cursor())
        refresh_btn.clicked.connect(lambda: self._serial_manager.refreshPorts() if self._serial_manager else None)
        port_row.addWidget(refresh_btn)
        layout.addLayout(port_row)

        # Filter toggle
        filter_row = QHBoxLayout()
        filter_label = QLabel("过滤系统tty")
        filter_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        filter_row.addWidget(filter_label)
        filter_row.addStretch()

        self._filter_toggle = SmallToggle("ON", theme_manager=self._theme_manager)
        self._filter_toggle.active = True
        self._filter_toggle.toggled_custom.connect(
            lambda v: setattr(self._serial_manager, 'filterSystemTty', v) if self._serial_manager else None)
        filter_row.addWidget(self._filter_toggle)
        layout.addLayout(filter_row)

        # Baud rate
        baud_label = QLabel("波特率 Baud Rate")
        baud_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(baud_label)
        self._baud_combo = EditableComboBox(theme_manager=self._theme_manager)
        self._baud_combo.addItems(BAUD_RATES)
        self._baud_combo.setCurrentText("115200")
        layout.addWidget(self._baud_combo)

        # Data bits
        db_label = QLabel("数据位 Data Bits")
        db_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(db_label)
        self._data_bits_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._data_bits_combo.addItems(DATA_BITS_LIST)
        self._data_bits_combo.setCurrentIndex(3)
        layout.addWidget(self._data_bits_combo)

        # Stop bits
        sb_label = QLabel("停止位 Stop Bits")
        sb_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(sb_label)
        self._stop_bits_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._stop_bits_combo.addItems(STOP_BITS_LIST)
        layout.addWidget(self._stop_bits_combo)

        # Parity
        par_label = QLabel("校验位 Parity")
        par_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(par_label)
        self._parity_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._parity_combo.addItems(PARITY_LIST)
        layout.addWidget(self._parity_combo)

        # Flow control
        fc_label = QLabel("流控 Flow Control")
        fc_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(fc_label)
        self._flow_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._flow_combo.addItems(FLOW_CONTROL_LIST)
        layout.addWidget(self._flow_combo)

        # Encoding
        enc_label = QLabel("接收编码 Encoding")
        enc_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        layout.addWidget(enc_label)
        self._debug_enc_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._debug_enc_combo.addItems(ENCODING_LIST)
        self._debug_enc_combo.currentIndexChanged.connect(
            lambda i: self._serial_manager.setReceiveEncoding(ENCODING_LIST[i]) if self._serial_manager else None)
        layout.addWidget(self._debug_enc_combo)

        # Newline
        nl_row = QHBoxLayout()
        nl_label = QLabel("发送换行")
        nl_label.setStyleSheet("font-size: 10px; color: #8899aa;")
        nl_row.addWidget(nl_label)
        nl_row.addStretch()
        self._d_cr_toggle = SmallToggle("CR", theme_manager=self._theme_manager)
        self._d_lf_toggle = SmallToggle("LF", theme_manager=self._theme_manager)
        self._d_cr_toggle.active = True
        self._d_lf_toggle.active = True
        self._d_cr_toggle.toggled_custom.connect(
            lambda v: setattr(self._serial_manager, 'newlineCr', v) if self._serial_manager else None)
        self._d_lf_toggle.toggled_custom.connect(
            lambda v: setattr(self._serial_manager, 'newlineLf', v) if self._serial_manager else None)
        nl_row.addWidget(self._d_cr_toggle)
        nl_row.addWidget(self._d_lf_toggle)
        layout.addLayout(nl_row)

        # Pin control
        self._pin_bar = PinControlBar(theme_manager=self._theme_manager)
        self._pin_bar.setVisible(False)
        layout.addWidget(self._pin_bar)

        # Open/Close button
        self._debug_action_btn = ActionButton("打开 Open", theme_manager=self._theme_manager)
        self._debug_action_btn.clicked_custom.connect(self._toggle_serial)
        layout.addWidget(self._debug_action_btn)

        self._debug_widget.setVisible(False)
        self._layout.addWidget(self._debug_widget)

    def _build_auto_reply(self):
        self._auto_reply_panel = AutoReplyPanel(theme_manager=self._theme_manager)
        self._auto_reply_panel.setVisible(False)
        self._layout.addWidget(self._auto_reply_panel)

    def _build_profile_section(self):
        profile_widget = QWidget()
        profile_layout = QVBoxLayout(profile_widget)
        profile_layout.setContentsMargins(6, 6, 6, 6)
        profile_layout.setSpacing(4)

        header_row = QHBoxLayout()
        header = QLabel("配置 Profile")
        header.setStyleSheet("font-size: 9px; font-weight: bold; color: #8899aa;")
        header_row.addWidget(header)
        header_row.addStretch()

        save_btn = SmallButton("保存", theme_manager=self._theme_manager)
        save_btn.clicked_custom.connect(
            lambda: self._config_manager.saveProfile(self._config_manager.current_profile) if self._config_manager else None)
        header_row.addWidget(save_btn)
        profile_layout.addLayout(header_row)

        self._profile_combo = StyledComboBox(theme_manager=self._theme_manager)
        self._profile_combo.currentTextChanged.connect(self._on_profile_changed)
        profile_layout.addWidget(self._profile_combo)

        self._layout.addWidget(profile_widget)
        self._profile_widget = profile_widget

    def _build_status_bar(self):
        self._status_bar = QWidget()
        status_layout = QHBoxLayout(self._status_bar)
        status_layout.setContentsMargins(0, 0, 0, 0)

        self._status_label = QLabel("未启动 Inactive")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("font-size: 11px; color: #8899aa;")
        status_layout.addWidget(self._status_label)

        self._layout.addWidget(self._status_bar)

    def _connect_signals(self):
        if self._serial_manager:
            self._serial_manager.port_list_changed.connect(self._update_port_list)
            self._serial_manager.is_open_changed.connect(self._on_serial_state_changed)
            self._serial_manager.port_opened.connect(
                lambda name: self._add_debug_log("SYS", f"已连接: {name}"))
            self._serial_manager.port_closed.connect(
                lambda: self._add_debug_log("SYS", "已断开"))
            self._serial_manager.pin_states_changed.connect(self._update_pin_states)
            self._auto_reply_panel.toggled.connect(
                lambda v: setattr(self._serial_manager, 'autoReplyEnabled', v))
            self._auto_reply_panel.match_changed.connect(
                lambda v: setattr(self._serial_manager, 'autoReplyMatch', v))
            self._auto_reply_panel.response_changed.connect(
                lambda v: setattr(self._serial_manager, 'autoReplyResponse', v))
            self._auto_reply_panel.delay_changed.connect(
                lambda v: setattr(self._serial_manager, 'autoReplyDelay', v))

        if self._virtual_manager:
            self._virtual_manager.is_active_changed.connect(self._on_virtual_state_changed)

        if self._config_manager:
            self._config_manager.profiles_changed.connect(self._update_profile_list)
            self._config_manager.quick_commands_changed.connect(self._refresh_quick_commands)
            self._update_profile_list()

        self._update_port_list()

    def _set_mode(self, mode: int):
        self._mode = mode
        self._virtual_btn.isActive = (mode == 0)
        self._debug_btn.isActive = (mode == 1)
        self._update_mode_visibility()
        self.mode_changed.emit(mode)

    def _update_mode_visibility(self):
        self._virtual_widget.setVisible(self._mode == 0)
        self._debug_widget.setVisible(self._mode == 1)
        self._auto_reply_panel.setVisible(self._mode == 1)

    def _toggle_virtual(self):
        if self._virtual_manager:
            if self._virtual_manager.isActive:
                self._virtual_manager.stopVirtualPort()
            else:
                self._virtual_manager.startVirtualPort()

    def _toggle_serial(self):
        if not self._serial_manager:
            return
        if self._serial_manager.isOpen:
            self._serial_manager.closePort()
        else:
            if self._selected_port >= 0 and self._selected_port < len(self._serial_manager.portList):
                data_bits_map = [5, 6, 7, 8]
                stop_bits_map = [1, 3, 2]
                parity_map = [0, 3, 2, 4, 1]
                flow_map = [0, 1, 2]

                try:
                    baud = int(self._baud_combo.currentText())
                except ValueError:
                    baud = 9600

                self._serial_manager.openPort(
                    self._serial_manager.portList[self._selected_port],
                    baud,
                    data_bits_map[self._data_bits_combo.currentIndex()],
                    stop_bits_map[self._stop_bits_combo.currentIndex()],
                    parity_map[self._parity_combo.currentIndex()],
                    flow_map[self._flow_combo.currentIndex()]
                )

    def _update_port_list(self):
        if not self._serial_manager:
            return
        self._port_combo.clear()
        self._port_combo.addItems(self._serial_manager.portList)

    def _on_serial_state_changed(self):
        is_open = self._serial_manager.isOpen if self._serial_manager else False
        self._debug_action_btn.isActive = is_open
        self._debug_action_btn.setText("关闭 Close" if is_open else "打开 Open")
        self._pin_bar.setVisible(is_open)
        self._update_status()

    def _on_virtual_state_changed(self):
        is_active = self._virtual_manager.isActive if self._virtual_manager else False
        self._virtual_action_btn.isActive = is_active
        self._virtual_action_btn.setText("停止 Stop" if is_active else "启动 Start")
        self._ext_port_widget.setVisible(is_active)
        self._update_status()

    def _update_status(self):
        if self._mode == 0:
            active = self._virtual_manager.isActive if self._virtual_manager else False
            self._status_label.setText("已就绪 Ready" if active else "未启动 Inactive")
            color = "#00d4aa" if active else "#8899aa"
        else:
            connected = self._serial_manager.isOpen if self._serial_manager else False
            self._status_label.setText("已连接 Connected" if connected else "未连接 Disconnected")
            color = "#00d4aa" if connected else "#8899aa"
        self._status_label.setStyleSheet(f"font-size: 11px; color: {color};")

    def _update_pin_states(self):
        if self._serial_manager and self._serial_manager.isOpen:
            self._pin_bar.set_states(
                self._serial_manager.dtr, self._serial_manager.rts,
                self._serial_manager.cts, self._serial_manager.dsr,
                self._serial_manager.dcd, self._serial_manager.ri
            )

    def _on_profile_changed(self, name):
        if self._config_manager and name and name != self._config_manager.current_profile:
            self._config_manager.loadProfile(name)

    def _update_profile_list(self):
        if not self._config_manager:
            return
        self._profile_combo.clear()
        self._profile_combo.addItems(self._config_manager.get_profiles())

    def _refresh_quick_commands(self):
        # This will be connected to data panel's refresh
        pass

    def _add_debug_log(self, log_type, data):
        # This will be connected to data panel
        pass

    def _update_all_styles(self):
        if not self._theme_manager:
            return
        text_sec = self._theme_manager.get_color_hex("textSecondary")
        border = self._theme_manager.get_color_hex("border")
        bg = self._theme_manager.get_color_hex("bgSecondary")
        accent = self._theme_manager.get_color_hex("accent")

        self.setStyleSheet(f"background: {bg};")
        self._separator.setStyleSheet(f"background: {border}; max-height: 1px;")

        for label in self.findChildren(QLabel):
            if "font-weight: bold" not in label.styleSheet():
                label.setStyleSheet(f"color: {text_sec}; font-size: 10px;")

        for btn in (self._virtual_btn, self._debug_btn):
            btn.set_theme_manager(self._theme_manager)
        for combo in self.findChildren(StyledComboBox):
            combo.set_theme_manager(self._theme_manager)
        for combo in self.findChildren(EditableComboBox):
            combo.set_theme_manager(self._theme_manager)
        for toggle in self.findChildren(SmallToggle):
            toggle.set_theme_manager(self._theme_manager)
        for btn in self.findChildren(SmallButton):
            btn.set_theme_manager(self._theme_manager)
        for btn in self.findChildren(ActionButton):
            btn.set_theme_manager(self._theme_manager)
        self._pin_bar.set_theme_manager(self._theme_manager)
        self._auto_reply_panel.set_theme_manager(self._theme_manager)
        self._ext_port_widget.setStyleSheet(f"background: {self._theme_manager.get_color_hex('bgTertiary')}; border-radius: 6px;")
        self._status_bar.setStyleSheet(f"background: {self._theme_manager.get_color_hex('bgTertiary')}; border-radius: 4px;")
