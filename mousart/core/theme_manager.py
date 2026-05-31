"""Theme management - multiple themes and font scaling."""
from mousart.qt_compat import *


# Theme definitions: each theme maps color names to hex values
THEMES = {
    "dark": {
        "bgPrimary": "#1a1a2e", "bgSecondary": "#16213e", "bgTertiary": "#0f3460",
        "textPrimary": "#e0e0e0", "textSecondary": "#8899aa", "accent": "#00d4aa",
        "border": "#2a2a4a", "receiveBg": "#0d1117", "sendBg": "#161b22", "titleBar": "#1a1a2e",
    },
    "light": {
        "bgPrimary": "#f0f0f5", "bgSecondary": "#ffffff", "bgTertiary": "#e8e8ed",
        "textPrimary": "#1a1a2e", "textSecondary": "#666677", "accent": "#0088cc",
        "border": "#ccccdd", "receiveBg": "#fafafa", "sendBg": "#ffffff", "titleBar": "#e8e8ed",
    },
    "solarized_dark": {
        "bgPrimary": "#002b36", "bgSecondary": "#073642", "bgTertiary": "#586e75",
        "textPrimary": "#839496", "textSecondary": "#657b83", "accent": "#2aa198",
        "border": "#073642", "receiveBg": "#00212b", "sendBg": "#073642", "titleBar": "#002b36",
    },
    "monokai": {
        "bgPrimary": "#272822", "bgSecondary": "#3e3d32", "bgTertiary": "#49483e",
        "textPrimary": "#f8f8f2", "textSecondary": "#75715e", "accent": "#a6e22e",
        "border": "#49483e", "receiveBg": "#1e1f1c", "sendBg": "#272822", "titleBar": "#272822",
    },
    "high_contrast": {
        "bgPrimary": "#000000", "bgSecondary": "#1a1a1a", "bgTertiary": "#333333",
        "textPrimary": "#ffffff", "textSecondary": "#cccccc", "accent": "#00ff88",
        "border": "#555555", "receiveBg": "#0a0a0a", "sendBg": "#111111", "titleBar": "#000000",
    },
}

THEME_NAMES = list(THEMES.keys())
THEME_LABELS = {
    "dark": "深色 Dark", "light": "浅色 Light",
    "solarized_dark": "Solarized", "monokai": "Monokai",
    "high_contrast": "高对比 High Contrast",
}


class ThemeManager(QObject):
    """Manages application theme and font scale."""

    theme_changed = pyqtSignal()
    font_scale_changed = pyqtSignal()
    colors_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = QSettings("MOUSART", "MOUSART")
        self._theme = self._settings.value("theme", "dark")
        if self._theme not in THEMES:
            self._theme = "dark"
        self._font_scale = float(self._settings.value("fontScale", 1.0))

    @pyqtProperty(str, notify=theme_changed)
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if value not in THEMES:
            return
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
        scale = max(0.8, min(2.0, scale))
        if abs(self._font_scale - scale) < 0.01:
            return
        self._font_scale = scale
        self._settings.setValue("fontScale", scale)
        self.font_scale_changed.emit()

    @property
    def theme_names(self):
        return THEME_NAMES

    @property
    def theme_labels(self):
        return THEME_LABELS

    def get_color(self, name: str) -> QColor:
        """Get a theme color by name."""
        theme_colors = THEMES.get(self._theme, THEMES["dark"])
        hex_val = theme_colors.get(name, "#ffffff")
        return QColor(hex_val)

    def get_color_hex(self, name: str) -> str:
        """Get a theme color as hex string."""
        theme_colors = THEMES.get(self._theme, THEMES["dark"])
        return theme_colors.get(name, "#ffffff")

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
        """Cycle to the next theme."""
        idx = THEME_NAMES.index(self._theme) if self._theme in THEME_NAMES else 0
        next_idx = (idx + 1) % len(THEME_NAMES)
        self.theme = THEME_NAMES[next_idx]
