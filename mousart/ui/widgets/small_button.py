"""Small button with optional accent styling."""
from mousart.qt_compat import *


class SmallButton(QPushButton):
    """Small flat button with optional accent mode."""

    clicked_custom = pyqtSignal()

    def __init__(self, label: str = "", parent=None, theme_manager=None,
                 accent: bool = False):
        super().__init__(label, parent)
        self._theme_manager = theme_manager
        self._accent = accent
        self._btn_enabled = True
        self.setFixedHeight(20)
        self.setCursor(self.cursor())
        self.clicked.connect(self.clicked_custom.emit)
        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def set_accent(self, v: bool):
        self._accent = v
        self._update_style()

    def set_btn_enabled(self, v: bool):
        self._btn_enabled = v
        self.setEnabled(v)
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

        if self._accent:
            self.setStyleSheet(f"""
                SmallButton {{
                    background: {accent};
                    color: #ffffff;
                    border: none;
                    border-radius: 10px;
                    padding: 2px 10px;
                    font-size: 10px;
                    font-weight: bold;
                }}
                SmallButton:hover {{ opacity: 0.85; }}
                SmallButton:disabled {{ opacity: 0.4; }}
            """)
        else:
            self.setStyleSheet(f"""
                SmallButton {{
                    background: {bg};
                    color: {text_sec};
                    border: 1px solid {border};
                    border-radius: 10px;
                    padding: 2px 10px;
                    font-size: 10px;
                }}
                SmallButton:hover {{
                    color: {text};
                    border-color: {accent};
                }}
            """)
