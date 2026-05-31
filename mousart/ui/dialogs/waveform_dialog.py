"""Waveform dialog - popup window showing UART serial waveform."""
from mousart.qt_compat import *
from mousart.ui.widgets.waveform_widget import WaveformWidget
from mousart.ui.widgets.small_button import SmallButton


class WaveformDialog(QDialog):
    """Popup dialog displaying a UART waveform visualization."""

    def __init__(self, parent=None, theme_manager=None, data: bytes = b"",
                 direction: str = "RX", timestamp: str = "", text_display: str = ""):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._data = data
        self._direction = direction

        self.setWindowTitle("串口波形 UART Waveform")
        self.setMinimumSize(600, 400)
        self.resize(900, 520)

        self._build_ui(direction, timestamp, text_display)
        self._apply_theme()
        self._waveform.set_data(data, direction)

    def _build_ui(self, direction, timestamp, text_display):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Header
        header = QHBoxLayout()
        header.setSpacing(12)

        dir_label = QLabel("<< RX" if direction == "RX" else ">> TX")
        color = "#4ec9b0" if direction == "RX" else "#569cd6"
        dir_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
        header.addWidget(dir_label)

        if timestamp:
            ts_label = QLabel(timestamp)
            ts_label.setStyleSheet("color: #8899aa; font-size: 11px;")
            header.addWidget(ts_label)

        count_label = QLabel(f"字节: {len(data)}")
        count_label.setStyleSheet("color: #8899aa; font-size: 11px;")
        header.addWidget(count_label)

        header.addStretch()

        cfg_label = QLabel("8N1  |  滚轮缩放  拖拽平移")
        cfg_label.setStyleSheet("color: #666677; font-size: 10px;")
        header.addWidget(cfg_label)

        layout.addLayout(header)

        # Waveform
        self._waveform = WaveformWidget(theme_manager=self._theme_manager)
        layout.addWidget(self._waveform, 1)

        # Data info panel
        info_widget = QWidget()
        info_widget.setMaximumHeight(140)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(4, 4, 4, 4)
        info_layout.setSpacing(2)

        # HEX display
        hex_str = " ".join(f"{b:02X}" for b in data[:64])
        if len(data) > 64:
            hex_str += f" ... (+{len(data) - 64})"
        hex_label = QLabel(f"HEX: {hex_str}")
        hex_label.setWordWrap(True)
        hex_label.setStyleSheet("font-family: monospace; font-size: 10px; color: #e0e0e0;")
        info_layout.addWidget(hex_label)

        # Binary display (bit-level view)
        bin_str = " ".join(f"{b:08b}" for b in data[:16])
        if len(data) > 16:
            bin_str += f" ... (+{len(data) - 16})"
        bin_label = QLabel(f"BIN: {bin_str}")
        bin_label.setWordWrap(True)
        bin_label.setStyleSheet("font-family: monospace; font-size: 10px; color: #4ec9b0;")
        info_layout.addWidget(bin_label)

        # Text display
        if text_display:
            text_label = QLabel(f"TXT: {text_display[:200]}")
            text_label.setWordWrap(True)
            text_label.setStyleSheet("font-family: monospace; font-size: 10px; color: #dcdcaa;")
            info_layout.addWidget(text_label)

        # Bit statistics
        if data:
            total_1 = sum(bin(b).count('1') for b in data)
            total_bits = len(data) * 8
            stats = (f"总位数: {total_bits}  |  1的个数: {total_1}  |  "
                     f"0的个数: {total_bits - total_1}  |  "
                     f"1占比: {total_1 / total_bits * 100:.1f}%")
            stats_label = QLabel(stats)
            stats_label.setStyleSheet("font-size: 10px; color: #8899aa;")
            info_layout.addWidget(stats_label)

        layout.addWidget(info_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self._close_btn = SmallButton("关闭", theme_manager=self._theme_manager)
        self._close_btn.clicked_custom.connect(self.accept)
        btn_layout.addWidget(self._close_btn)
        layout.addLayout(btn_layout)

    def _apply_theme(self):
        if self._theme_manager:
            bg = self._theme_manager.get_color_hex("bgSecondary")
            border = self._theme_manager.get_color_hex("border")
            self.setStyleSheet(f"""
                QDialog {{
                    background: {bg};
                    border: 1px solid {border};
                    border-radius: 8px;
                }}
            """)
            self._waveform.set_theme_manager(self._theme_manager)
