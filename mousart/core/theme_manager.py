"""Theme management - dark/light mode and font scaling."""
from mousart.qt_compat import *


class ThemeManager(QObject):
    """Manages application theme (dark/light) and font scale."""

    theme_changed = pyqtSignal()
    font_scale_changed = pyqtSignal()
    colors_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = QSettings("MOUSART", "MOUSART")
        self._theme = self._settings.value("theme", "dark")
        self._font_scale = float(self._settings.value("fontScale", 1.0))

    @pyqtProperty(str, notify=theme_changed)
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if self._theme == value:
            return
        self._theme = value
        self._settings.setValue("theme", value)
        self.theme_changed.emit()
        self.colors_changed.emit()

    @pyqtProperty(float, notify=font_scale_changed)
    def fontScale(self):
        return self._font_scale

    @fontScale.setter
    def fontScale(self, scale):
        scale = max(0.8, min(1.5, scale))
        if abs(self._font_scale - scale) < 0.01:
            return
        self._font_scale = scale
        self._settings.setValue("fontScale", scale)
        self.font_scale_changed.emit()

    def get_color(self, name: str) -> QColor:
        """Get a theme color by name."""
        dark = self._theme == "dark"
        color_map = {
            "bgPrimary": QColor("#1a1a2e") if dark else QColor("#f0f0f5"),
            "bgSecondary": QColor("#16213e") if dark else QColor("#ffffff"),
            "bgTertiary": QColor("#0f3460") if dark else QColor("#e8e8ed"),
            "textPrimary": QColor("#e0e0e0") if dark else QColor("#1a1a2e"),
            "textSecondary": QColor("#8899aa") if dark else QColor("#666677"),
            "accent": QColor("#00d4aa") if dark else QColor("#0088cc"),
            "border": QColor("#2a2a4a") if dark else QColor("#ccccdd"),
            "receiveBg": QColor("#0d1117") if dark else QColor("#fafafa"),
            "sendBg": QColor("#161b22") if dark else QColor("#ffffff"),
            "titleBar": QColor("#1a1a2e") if dark else QColor("#e8e8ed"),
        }
        return color_map.get(name, QColor("#ffffff"))

    def get_color_hex(self, name: str) -> str:
        """Get a theme color as hex string."""
        return self.get_color(name).name()

    @pyqtProperty(QColor, notify=colors_changed)
    def bgPrimary(self):
        return self.get_color("bgPrimary")

    @pyqtProperty(QColor, notify=colors_changed)
    def bgSecondary(self):
        return self.get_color("bgSecondary")

    @pyqtProperty(QColor, notify=colors_changed)
    def bgTertiary(self):
        return self.get_color("bgTertiary")

    @pyqtProperty(QColor, notify=colors_changed)
    def textPrimary(self):
        return self.get_color("textPrimary")

    @pyqtProperty(QColor, notify=colors_changed)
    def textSecondary(self):
        return self.get_color("textSecondary")

    @pyqtProperty(QColor, notify=colors_changed)
    def accent(self):
        return self.get_color("accent")

    @pyqtProperty(QColor, notify=colors_changed)
    def border(self):
        return self.get_color("border")

    @pyqtProperty(QColor, notify=colors_changed)
    def receiveBg(self):
        return self.get_color("receiveBg")

    @pyqtProperty(QColor, notify=colors_changed)
    def sendBg(self):
        return self.get_color("sendBg")

    @pyqtProperty(QColor, notify=colors_changed)
    def titleBar(self):
        return self.get_color("titleBar")

    def toggle_theme(self):
        """Toggle between dark and light theme."""
        self.theme = "light" if self._theme == "dark" else "dark"
