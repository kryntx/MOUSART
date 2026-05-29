"""Auto-reply configuration panel."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QSpinBox, QCheckBox)
from PyQt6.QtCore import pyqtSignal


class AutoReplyPanel(QWidget):
    """Auto-reply configuration panel with toggle, match, response, and delay."""

    toggled = pyqtSignal(bool)
    match_changed = pyqtSignal(str)
    response_changed = pyqtSignal(str)
    delay_changed = pyqtSignal(int)

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # Header with toggle
        header = QHBoxLayout()
        self._toggle = QCheckBox("自动回复 Auto-Reply")
        self._toggle.stateChanged.connect(lambda s: self.toggled.emit(s == 2))
        header.addWidget(self._toggle)
        header.addStretch()
        layout.addLayout(header)

        # Match field
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("匹配:"))
        self._match_input = QLineEdit()
        self._match_input.setPlaceholderText("关键字...")
        self._match_input.textChanged.connect(self.match_changed.emit)
        row1.addWidget(self._match_input)
        layout.addLayout(row1)

        # Response field
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("回复:"))
        self._response_input = QLineEdit()
        self._response_input.setPlaceholderText("响应数据...")
        self._response_input.textChanged.connect(self.response_changed.emit)
        row2.addWidget(self._response_input)
        layout.addLayout(row2)

        # Delay field
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("延迟(ms):"))
        self._delay_spin = QSpinBox()
        self._delay_spin.setRange(0, 60000)
        self._delay_spin.setValue(0)
        self._delay_spin.valueChanged.connect(self.delay_changed.emit)
        row3.addWidget(self._delay_spin)
        row3.addStretch()
        layout.addLayout(row3)

        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def set_values(self, enabled: bool, match: str, response: str, delay: int):
        self._toggle.setChecked(enabled)
        self._match_input.setText(match)
        self._response_input.setText(response)
        self._delay_spin.setValue(delay)

    def _update_style(self):
        if not self._theme_manager:
            return
        text = self._theme_manager.get_color_hex("textSecondary")
        accent = self._theme_manager.get_color_hex("accent")
        self.setStyleSheet(f"""
            QLabel {{ color: {text}; font-size: 10px; }}
            QCheckBox {{ color: {text}; font-size: 10px; }}
        """)
