"""Custom title bar widget with icon, font scale, theme toggle, and window controls."""
from mousart.qt_compat import *


class TitleBarButton(QPushButton):
    """Window control button (minimize, maximize, close)."""

    def __init__(self, btn_type: str, parent=None, theme_manager=None):
        super().__init__(parent)
        self._type = btn_type
        self._theme_manager = theme_manager
        self.setFixedSize(32, 28)
        self.setCursor(self.cursor())
        self._hovered = False
        self._update_style()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def enterEvent(self, event):
        self._hovered = True
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._type == "close" and self._hovered:
            painter.fillRect(self.rect(), QColor("#e81123"))
            painter.setPen(QColor("#ffffff"))
        elif self._hovered:
            bg = self._theme_manager.get_color_hex("bgTertiary") if self._theme_manager else "#0f3460"
            painter.fillRect(self.rect(), QColor(bg))
            painter.setPen(QColor(self._theme_manager.get_color_hex("textPrimary")) if self._theme_manager else QColor("#e0e0e0"))
        else:
            painter.setPen(QColor(self._theme_manager.get_color_hex("textSecondary")) if self._theme_manager else QColor("#8899aa"))

        painter.setBrush(Qt_BrushStyle_NoBrush)
        pen = painter.pen()
        pen.setWidthF(1.2)
        painter.setPen(pen)

        cx, cy = self.width() / 2, self.height() / 2
        s = 5

        if self._type == "minimize":
            painter.drawLine(int(cx - s), int(cy), int(cx + s), int(cy))
        elif self._type == "maximize":
            painter.drawRect(int(cx - s), int(cy - s), int(s * 2), int(s * 2))
        elif self._type == "restore":
            # Two overlapping rectangles
            painter.drawRect(int(cx - s - 1), int(cy - s + 2), int(s * 1.5), int(s * 1.5))
            painter.drawRect(int(cx - s + 2), int(cy - s - 1), int(s * 1.5), int(s * 1.5))
        elif self._type == "close":
            painter.drawLine(int(cx - s), int(cy - s), int(cx + s), int(cy + s))
            painter.drawLine(int(cx - s), int(cy + s), int(cx + s), int(cy - s))

        painter.end()

    def _update_style(self):
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")


class TitleBar(QWidget):
    """Custom title bar with app icon, font scale slider, theme toggle, and window controls."""

    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    theme_toggle_clicked = pyqtSignal()

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._is_maximized = False
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 4, 0)
        layout.setSpacing(8)

        # App icon
        self._icon_widget = QWidget()
        self._icon_widget.setFixedSize(20, 20)
        self._icon_widget.paintEvent = self._paint_icon
        layout.addWidget(self._icon_widget)

        # App name
        self._title_label = QLabel("MOUSART")
        self._title_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(self._title_label)

        layout.addStretch()

        # Font scale control
        self._small_a = QLabel("A")
        self._small_a.setStyleSheet("font-size: 10px;")
        layout.addWidget(self._small_a)

        self._scale_bar = QWidget()
        self._scale_bar.setFixedSize(80, 4)
        self._scale_bar.paintEvent = self._paint_scale_bar
        self._scale_bar.mousePressEvent = self._on_scale_click
        layout.addWidget(self._scale_bar)

        self._big_a = QLabel("A")
        self._big_a.setStyleSheet("font-size: 18px;")
        layout.addWidget(self._big_a)

        # Theme toggle
        self._theme_btn = QPushButton()
        self._theme_btn.setFixedSize(30, 24)
        self._theme_btn.setCursor(self.cursor())
        self._theme_btn.clicked.connect(self.theme_toggle_clicked.emit)
        self._theme_btn.paintEvent = self._paint_theme_icon
        self._theme_btn.setStyleSheet("QPushButton { border: none; background: transparent; border-radius: 4px; }")
        layout.addWidget(self._theme_btn)

        layout.addSpacing(8)

        # Window control buttons
        self._min_btn = TitleBarButton("minimize", theme_manager=theme_manager)
        self._max_btn = TitleBarButton("maximize", theme_manager=theme_manager)
        self._close_btn = TitleBarButton("close", theme_manager=theme_manager)

        self._min_btn.clicked.connect(self.minimize_clicked.emit)
        self._max_btn.clicked.connect(self.maximize_clicked.emit)
        self._close_btn.clicked.connect(self.close_clicked.emit)

        layout.addWidget(self._min_btn)
        layout.addWidget(self._max_btn)
        layout.addWidget(self._close_btn)

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        for btn in (self._min_btn, self._max_btn, self._close_btn):
            btn.set_theme_manager(tm)
        self._update_style()
        self.update()

    def set_maximized(self, v: bool):
        self._is_maximized = v
        self._max_btn._type = "restore" if v else "maximize"
        self._max_btn.update()

    def _update_style(self):
        if not self._theme_manager:
            return
        bg = self._theme_manager.get_color_hex("titleBar")
        text = self._theme_manager.get_color_hex("textPrimary")
        text_sec = self._theme_manager.get_color_hex("textSecondary")
        border = self._theme_manager.get_color_hex("border")

        self.setStyleSheet(f"background: {bg};")
        self._title_label.setStyleSheet(f"color: {text}; font-size: 13px; font-weight: bold; font-family: 'Segoe UI', sans-serif;")
        self._small_a.setStyleSheet(f"color: {text_sec}; font-size: 10px;")
        self._big_a.setStyleSheet(f"color: {text_sec}; font-size: 18px;")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self._theme_manager:
            border = QColor(self._theme_manager.get_color_hex("border"))
        else:
            border = QColor("#2a2a4a")
        painter.setPen(border)
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        painter.end()

    def _paint_icon(self, event):
        painter = QPainter(self._icon_widget)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        accent = QColor(self._theme_manager.get_color_hex("accent")) if self._theme_manager else QColor("#00d4aa")

        pen = QPen(accent, 2)
        pen.setCapStyle(Qt_PenCapStyle_RoundCap)
        painter.setPen(pen)

        w, h = self._icon_widget.width(), self._icon_widget.height()
        cx, cy = w / 2, h / 2

        # Draw bezier curve (serial signal wave)
        path = QPainterPath()
        path.moveTo(2, cy)
        path.cubicTo(cx * 0.5, cy - 6, cx, cy + 6, w - 2, cy)
        painter.drawPath(path)

        # Draw center dot
        painter.setPen(Qt_PenStyle_NoPen)
        painter.setBrush(accent)
        painter.drawEllipse(int(cx) - 2, int(cy) - 2, 4, 4)
        painter.end()

    def _paint_scale_bar(self, event):
        painter = QPainter(self._scale_bar)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self._scale_bar.width(), self._scale_bar.height()

        # Background
        bg = QColor(self._theme_manager.get_color_hex("bgTertiary")) if self._theme_manager else QColor("#0f3460")
        painter.setBrush(bg)
        painter.setPen(Qt_PenStyle_NoPen)
        painter.drawRoundedRect(0, 0, w, h, 2, 2)

        # Fill
        accent = QColor(self._theme_manager.get_color_hex("accent")) if self._theme_manager else QColor("#00d4aa")
        painter.setBrush(accent)
        if self._theme_manager:
            ratio = (self._theme_manager.fontScale - 0.8) / 0.7
        else:
            ratio = 0.5
        painter.drawRoundedRect(0, 0, int(w * ratio), h, 2, 2)
        painter.end()

    def _on_scale_click(self, event: QMouseEvent):
        if self._theme_manager:
            ratio = QMouseEvent_Position(event).x() / self._scale_bar.width()
            self._theme_manager.fontScale = 0.8 + ratio * 0.7
            self._scale_bar.update()

    def _paint_theme_icon(self, event):
        painter = QPainter(self._theme_btn)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self._theme_btn.width(), self._theme_btn.height()
        cx, cy = w / 2, h / 2
        r = min(w, h) * 0.35

        text_color = QColor(self._theme_manager.get_color_hex("textPrimary")) if self._theme_manager else QColor("#e0e0e0")

        if self._theme_manager and self._theme_manager.theme == "dark":
            # Moon icon
            painter.setBrush(text_color)
            painter.setPen(Qt_PenStyle_NoPen)
            path = QPainterPath()
            path.addEllipse(int(cx - r), int(cy - r), int(r * 2), int(r * 2))
            path.addEllipse(int(cx + r * 0.4 - r * 0.7), int(cy - r * 0.3 - r * 0.7),
                           int(r * 1.4), int(r * 1.4))
            painter.drawPath(path)
        else:
            # Sun icon
            pen = QPen(text_color, 1.5)
            painter.setPen(pen)
            painter.setBrush(Qt_BrushStyle_NoBrush)
            painter.drawEllipse(int(cx - r * 0.5), int(cy - r * 0.5),
                               int(r), int(r))
            import math
            for i in range(8):
                angle = i * math.pi / 4
                x1 = cx + math.cos(angle) * r * 0.7
                y1 = cy + math.sin(angle) * r * 0.7
                x2 = cx + math.cos(angle) * r
                y2 = cy + math.sin(angle) * r
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        painter.end()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt_MouseButton_LeftButton:
            self.maximize_clicked.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt_MouseButton_LeftButton:
            self.window().startSystemMove()
