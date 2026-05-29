"""Large action button (Open/Close, Start/Stop)."""
from mousart.qt_compat import *


class ActionButton(QPushButton):
    """Large action button with green/red accent based on active state."""

    clicked_custom = pyqtSignal()

    def __init__(self, label: str = "", parent=None, theme_manager=None):
        super().__init__(label, parent)
        self._theme_manager = theme_manager
        self._is_active = False
        self.setMinimumHeight(34)
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
            border = self._theme_manager.get_color_hex("border")
        else:
            accent, bg, text, border = "#00d4aa", "#0f3460", "#e0e0e0", "#2a2a4a"

        if self._is_active:
            # Red-ish when active (close action)
            self.setStyleSheet(f"""
                ActionButton {{
                    background: #e74c3c;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 16px;
                }}
                ActionButton:hover {{ background: #c0392b; }}
            """)
        else:
            self.setStyleSheet(f"""
                ActionButton {{
                    background: {accent};
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 16px;
                }}
                ActionButton:hover {{ opacity: 0.85; }}
            """)
