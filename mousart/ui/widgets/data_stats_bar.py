"""Data statistics bar showing RX/TX bytes and rates."""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class DataStatsBar(QWidget):
    """Bottom bar showing RX/TX cumulative bytes and real-time rates."""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(8, 2, 8, 2)
        self._layout.setSpacing(12)

        self._rx_label = QLabel("RX: 0 B  (0 B/s)")
        self._tx_label = QLabel("TX: 0 B  (0 B/s)")

        for label in (self._rx_label, self._tx_label):
            label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self._layout.addWidget(label)

        self._layout.addStretch()
        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def update_stats(self, rx_bytes: str, tx_bytes: str, rx_rate: str, tx_rate: str):
        self._rx_label.setText(f"RX: {rx_bytes}  ({rx_rate})")
        self._tx_label.setText(f"TX: {tx_bytes}  ({tx_rate})")

    def _update_style(self):
        if self._theme_manager:
            text = self._theme_manager.get_color_hex("textSecondary")
            bg = self._theme_manager.get_color_hex("bgPrimary")
        else:
            text, bg = "#8899aa", "#1a1a2e"

        self.setStyleSheet(f"background: {bg};")
        style = f"""
            QLabel {{
                color: {text};
                font-size: 10px;
                font-family: monospace;
            }}
        """
        self._rx_label.setStyleSheet(style.replace("color:", "color: #4ec9b0;") if self._theme_manager else style)
        self._tx_label.setStyleSheet(style.replace("color:", "color: #569cd6;") if self._theme_manager else style)

        # Use proper colors
        rx_color = "#4ec9b0"
        tx_color = "#569cd6"
        self._rx_label.setStyleSheet(f"color: {rx_color}; font-size: 10px; font-family: monospace;")
        self._tx_label.setStyleSheet(f"color: {tx_color}; font-size: 10px; font-family: monospace;")
