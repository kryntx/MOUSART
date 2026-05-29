"""Small pill-shaped toggle button widget."""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtProperty


class SmallToggle(QPushButton):
    """Small toggle button like a chip/tag. Accent when active."""

    toggled_custom = pyqtSignal(bool)

    def __init__(self, label: str = "", parent=None, theme_manager=None):
        super().__init__(label, parent)
        self._active = False
        self._theme_manager = theme_manager
        self.setCheckable(True)
        self.setFixedHeight(20)
        self.setCursor(self.cursor())
        self.clicked.connect(self._on_clicked)
        self._update_style()

    def _on_clicked(self):
        self._active = self.isChecked()
        self._update_style()
        self.toggled_custom.emit(self._active)

    @pyqtProperty(bool)
    def active(self):
        return self._active

    @active.setter
    def active(self, v):
        self._active = v
        self.setChecked(v)
        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def _update_style(self):
        if self._theme_manager:
            accent = self._theme_manager.get_color_hex("accent")
            bg = self._theme_manager.get_color_hex("bgTertiary")
            text = self._theme_manager.get_color_hex("textPrimary")
            text_sec = self._theme_manager.get_color_hex("textSecondary")
        else:
            accent, bg, text, text_sec = "#00d4aa", "#0f3460", "#e0e0e0", "#8899aa"

        if self._active:
            self.setStyleSheet(f"""
                SmallToggle {{
                    background: {accent};
                    color: #ffffff;
                    border: none;
                    border-radius: 10px;
                    padding: 2px 8px;
                    font-size: 10px;
                    font-weight: bold;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                SmallToggle {{
                    background: {bg};
                    color: {text_sec};
                    border: none;
                    border-radius: 10px;
                    padding: 2px 8px;
                    font-size: 10px;
                }}
                SmallToggle:hover {{
                    color: {text};
                }}
            """)
