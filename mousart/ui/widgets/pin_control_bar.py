"""Pin control bar with DTR/RTS toggles and CTS/DSR/DCD/RI LED indicators."""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter, QColor


class LEDIndicator(QWidget):
    """Small LED indicator dot."""

    def __init__(self, label: str, parent=None, color: str = "#888888"):
        super().__init__(parent)
        self._label = label
        self._color = QColor(color)
        self.setFixedSize(32, 20)

    def set_state(self, on: bool):
        self._color = QColor("#00d4aa") if on else QColor("#555555")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw LED dot
        painter.setBrush(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(4, 5, 10, 10)
        # Draw label
        painter.setPen(QColor("#8899aa"))
        painter.drawText(16, 0, 16, 20, Qt.AlignmentFlag.AlignVCenter, self._label)
        painter.end()


class PinControlBar(QWidget):
    """Row with DTR/RTS toggle buttons and CTS/DSR/DCD/RI LED indicators."""

    dtr_toggled = pyqtSignal(bool)
    rts_toggled = pyqtSignal(bool)

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)

        # DTR toggle
        self._dtr_btn = QPushButton("DTR")
        self._dtr_btn.setCheckable(True)
        self._dtr_btn.setFixedSize(36, 20)
        self._dtr_btn.setCursor(self.cursor())
        self._dtr_btn.clicked.connect(lambda: self.dtr_toggled.emit(self._dtr_btn.isChecked()))
        self._layout.addWidget(self._dtr_btn)

        # RTS toggle
        self._rts_btn = QPushButton("RTS")
        self._rts_btn.setCheckable(True)
        self._rts_btn.setFixedSize(36, 20)
        self._rts_btn.setCursor(self.cursor())
        self._rts_btn.clicked.connect(lambda: self.rts_toggled.emit(self._rts_btn.isChecked()))
        self._layout.addWidget(self._rts_btn)

        self._layout.addSpacing(8)

        # LED indicators
        self._cts_led = LEDIndicator("CTS")
        self._dsr_led = LEDIndicator("DSR")
        self._dcd_led = LEDIndicator("DCD")
        self._ri_led = LEDIndicator("RI")

        self._layout.addWidget(self._cts_led)
        self._layout.addWidget(self._dsr_led)
        self._layout.addWidget(self._dcd_led)
        self._layout.addWidget(self._ri_led)
        self._layout.addStretch()

        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def set_states(self, dtr: bool, rts: bool, cts: bool, dsr: bool, dcd: bool, ri: bool):
        self._dtr_btn.setChecked(dtr)
        self._rts_btn.setChecked(rts)
        self._cts_led.set_state(cts)
        self._dsr_led.set_state(dsr)
        self._dcd_led.set_state(dcd)
        self._ri_led.set_state(ri)

    def _update_style(self):
        accent = self._theme_manager.get_color_hex("accent") if self._theme_manager else "#00d4aa"
        bg = self._theme_manager.get_color_hex("bgTertiary") if self._theme_manager else "#0f3460"
        text = self._theme_manager.get_color_hex("textSecondary") if self._theme_manager else "#8899aa"

        btn_style = f"""
            QPushButton {{
                background: {bg};
                color: {text};
                border: 1px solid transparent;
                border-radius: 3px;
                font-size: 9px;
                font-weight: bold;
            }}
            QPushButton:checked {{
                background: {accent};
                color: #ffffff;
            }}
        """
        self._dtr_btn.setStyleSheet(btn_style)
        self._rts_btn.setStyleSheet(btn_style)
