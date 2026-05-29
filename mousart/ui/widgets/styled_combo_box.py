"""Styled combo box widget."""
from mousart.qt_compat import *


class StyledComboBox(QComboBox):
    """Custom-styled combo box with themed appearance."""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self.setFixedHeight(28)
        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def _update_style(self):
        if not self._theme_manager:
            return
        bg = self._theme_manager.get_color_hex("sendBg")
        text = self._theme_manager.get_color_hex("textPrimary")
        border = self._theme_manager.get_color_hex("border")
        accent = self._theme_manager.get_color_hex("accent")
        bg_sec = self._theme_manager.get_color_hex("bgSecondary")
        hover = self._theme_manager.get_color_hex("hover")

        self.setStyleSheet(f"""
            StyledComboBox {{
                background: {bg};
                color: {text};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }}
            StyledComboBox:hover {{
                border-color: {accent};
            }}
            StyledComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            StyledComboBox QAbstractItemView {{
                background: {bg_sec};
                color: {text};
                border: 1px solid {border};
                selection-background-color: {hover};
                outline: none;
            }}
        """)
