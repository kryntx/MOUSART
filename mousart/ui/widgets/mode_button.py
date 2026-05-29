"""Mode selector button (Virtual/Debug)."""
from mousart.qt_compat import *


class ModeButton(QPushButton):
    """Two-line mode selector button with accent when selected."""

    clicked_custom = pyqtSignal()

    def __init__(self, label: str = "", sublabel: str = "", parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._label = label
        self._sublabel = sublabel
        self._is_active = False
        self.setFixedHeight(44)
        self.setCursor(self.cursor())
        self.clicked.connect(self.clicked_custom.emit)
        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    @pyqtProperty(bool)
    def isActive(self):
        return self._is_active

    @isActive.setter
    def isActive(self, v):
        self._is_active = v
        self._update_style()

    def _update_style(self):
        if self._theme_manager:
            accent = self._theme_manager.get_color_hex("accent")
            bg = self._theme_manager.get_color_hex("bgTertiary")
            text = self._theme_manager.get_color_hex("textPrimary")
            text_sec = self._theme_manager.get_color_hex("textSecondary")
            border = self._theme_manager.get_color_hex("border")
        else:
            accent, bg, text = "#00d4aa", "#0f3460", "#e0e0e0"
            text_sec, border = "#8899aa", "#2a2a4a"

        self.setText(f"{self._label}\n{self._sublabel}")

        if self._is_active:
            self.setStyleSheet(f"""
                ModeButton {{
                    background: {accent};
                    color: #ffffff;
                    border: 2px solid {accent};
                    border-radius: 8px;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 4px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                ModeButton {{
                    background: {bg};
                    color: {text_sec};
                    border: 2px solid {border};
                    border-radius: 8px;
                    font-size: 11px;
                    padding: 4px;
                }}
                ModeButton:hover {{
                    border-color: {accent};
                    color: {text};
                }}
            """)
