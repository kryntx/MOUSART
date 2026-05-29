"""Custom frameless main window with shadow, resize handles, and drag support."""
import sys
from mousart.qt_compat import *

from mousart.ui.title_bar import TitleBar
from mousart.ui.settings_panel import SettingsPanel
from mousart.ui.data_panel import DataPanel
from mousart.utils.stylesheet import generate_stylesheet

# Resize direction constants
RESIZE_NONE = 0
RESIZE_LEFT = 1
RESIZE_RIGHT = 2
RESIZE_TOP = 3
RESIZE_BOTTOM = 4
RESIZE_TOP_LEFT = 5
RESIZE_TOP_RIGHT = 6
RESIZE_BOTTOM_LEFT = 7
RESIZE_BOTTOM_RIGHT = 8


class MainWindow(QMainWindow):
    """Custom frameless window with shadow, resize, and all panels."""

    def __init__(self, theme_manager, serial_manager, virtual_manager,
                 config_manager, data_analyzer, log_file_manager):
        super().__init__()
        self._theme_manager = theme_manager
        self._serial_manager = serial_manager
        self._virtual_manager = virtual_manager
        self._config_manager = config_manager
        self._data_analyzer = data_analyzer
        self._log_file_manager = log_file_manager

        self._is_maximized = False
        self._resize_direction = RESIZE_NONE
        self._resize_margin = 8
        self._drag_start = None
        self._drag_geom = None

        self.setWindowFlags(Qt_WindowType_FramelessWindowHint | Qt_WindowType_Window)
        self.setAttribute(Qt_WidgetAttribute_WA_TranslucentBackground)
        self.setMinimumSize(700, 500)
        self.resize(1000, 700)

        self._build_ui()
        self._connect_signals()
        self._apply_theme()

    def _build_ui(self):
        # Central widget with shadow
        self._central = QWidget()
        self.setCentralWidget(self._central)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self._central)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self._central.setGraphicsEffect(shadow)

        # Main container
        self._container = QWidget(self._central)
        self._container.setObjectName("mainContainer")

        main_layout = QVBoxLayout(self._central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.addWidget(self._container)

        container_layout = QVBoxLayout(self._container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Title bar
        self._title_bar = TitleBar(theme_manager=self._theme_manager)
        container_layout.addWidget(self._title_bar)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Settings panel (left)
        self._settings_panel = SettingsPanel(
            theme_manager=self._theme_manager,
            serial_manager=self._serial_manager,
            virtual_manager=self._virtual_manager,
            config_manager=self._config_manager
        )
        content_layout.addWidget(self._settings_panel)

        # Separator
        sep = QWidget()
        sep.setFixedWidth(1)
        content_layout.addWidget(sep)
        self._separator = sep

        # Data panel (right)
        self._data_panel = DataPanel(
            theme_manager=self._theme_manager,
            serial_manager=self._serial_manager,
            virtual_manager=self._virtual_manager,
            config_manager=self._config_manager,
            data_analyzer=self._data_analyzer,
            log_file_manager=self._log_file_manager
        )
        content_layout.addWidget(self._data_panel, 1)

        container_layout.addWidget(content, 1)

        # Update window geometry on maximize/restore
        self._update_geometry()

    def _connect_signals(self):
        # Title bar signals
        self._title_bar.minimize_clicked.connect(self.showMinimized)
        self._title_bar.maximize_clicked.connect(self._toggle_maximize)
        self._title_bar.close_clicked.connect(self.close)
        self._title_bar.theme_toggle_clicked.connect(self._toggle_theme)

        # Settings panel mode change
        self._settings_panel.mode_changed.connect(self._data_panel.set_mode)

        # Theme changes
        self._theme_manager.colors_changed.connect(self._apply_theme)
        self._theme_manager.font_scale_changed.connect(self._apply_theme)

    def _toggle_maximize(self):
        if self._is_maximized:
            self.showNormal()
            self._is_maximized = False
        else:
            self.showMaximized()
            self._is_maximized = True
        self._title_bar.set_maximized(self._is_maximized)

    def _toggle_theme(self):
        self._theme_manager.toggle_theme()

    def _apply_theme(self):
        theme = self._theme_manager.theme
        scale = self._theme_manager.fontScale

        # Apply stylesheet
        qss = generate_stylesheet(theme, scale)
        QApplication.instance().setStyleSheet(qss)

        # Update container background
        bg = self._theme_manager.get_color_hex("bgPrimary")
        border = self._theme_manager.get_color_hex("border")
        self._container.setStyleSheet(f"""
            #mainContainer {{
                background: {bg};
                border: 1px solid {border};
                border-radius: 12px;
            }}
        """)

        # Update separator
        self._separator.setStyleSheet(f"background: {border};")

        # Update font size
        font = QFont()
        font.setPointSize(int(12 * scale))
        QApplication.instance().setFont(font)

        # Update child panels
        self._title_bar.set_theme_manager(self._theme_manager)
        self._settings_panel.set_theme_manager(self._theme_manager)
        self._data_panel.set_theme_manager(self._theme_manager)

    def _update_geometry(self):
        """Update layout margins based on maximized state."""
        layout = self._central.layout()
        if self._is_maximized:
            layout.setContentsMargins(0, 0, 0, 0)
            self._container.setStyleSheet(self._container.styleSheet().replace("border-radius: 12px", "border-radius: 0px"))
        else:
            layout.setContentsMargins(12, 12, 12, 12)

    def changeEvent(self, event):
        if event.type() == QEvent_Type_WindowStateChange:
            self._is_maximized = self.isMaximized()
            self._title_bar.set_maximized(self._is_maximized)
            self._update_geometry()
        super().changeEvent(event)

    def _get_resize_direction(self, pos: QPoint) -> int:
        """Determine resize direction based on mouse position."""
        if self._is_maximized:
            return RESIZE_NONE

        m = self._resize_margin
        rect = self.rect()
        x, y = pos.x(), pos.y()
        w, h = rect.width(), rect.height()

        left = x < m
        right = x > w - m
        top = y < m
        bottom = y > h - m

        if top and left:
            return RESIZE_TOP_LEFT
        if top and right:
            return RESIZE_TOP_RIGHT
        if bottom and left:
            return RESIZE_BOTTOM_LEFT
        if bottom and right:
            return RESIZE_BOTTOM_RIGHT
        if left:
            return RESIZE_LEFT
        if right:
            return RESIZE_RIGHT
        if top:
            return RESIZE_TOP
        if bottom:
            return RESIZE_BOTTOM
        return RESIZE_NONE

    def _cursor_for_direction(self, direction: int):
        cursors = {
            RESIZE_LEFT: Qt_CursorShape_SizeHorCursor,
            RESIZE_RIGHT: Qt_CursorShape_SizeHorCursor,
            RESIZE_TOP: Qt_CursorShape_SizeVerCursor,
            RESIZE_BOTTOM: Qt_CursorShape_SizeVerCursor,
            RESIZE_TOP_LEFT: Qt_CursorShape_SizeFDiagCursor,
            RESIZE_TOP_RIGHT: Qt_CursorShape_SizeBDiagCursor,
            RESIZE_BOTTOM_LEFT: Qt_CursorShape_SizeBDiagCursor,
            RESIZE_BOTTOM_RIGHT: Qt_CursorShape_SizeFDiagCursor,
        }
        return cursors.get(direction, Qt_CursorShape_ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt_MouseButton_LeftButton and not self._is_maximized:
            self._resize_direction = self._get_resize_direction(event.pos())
            if self._resize_direction != RESIZE_NONE:
                self._drag_start = event.globalPosition().toPoint()
                self._drag_geom = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_maximized:
            super().mouseMoveEvent(event)
            return

        # Update cursor
        direction = self._get_resize_direction(event.pos())
        if self._resize_direction == RESIZE_NONE:
            self.setCursor(self._cursor_for_direction(direction))

        # Handle resize
        if self._resize_direction != RESIZE_NONE and self._drag_start and self._drag_geom:
            delta = event.globalPosition().toPoint() - self._drag_start
            geom = QRect(self._drag_geom)

            if self._resize_direction in (RESIZE_RIGHT, RESIZE_TOP_RIGHT, RESIZE_BOTTOM_RIGHT):
                geom.setWidth(max(self.minimumWidth(), geom.width() + delta.x()))
            if self._resize_direction in (RESIZE_BOTTOM, RESIZE_BOTTOM_LEFT, RESIZE_BOTTOM_RIGHT):
                geom.setHeight(max(self.minimumHeight(), geom.height() + delta.y()))
            if self._resize_direction in (RESIZE_LEFT, RESIZE_TOP_LEFT, RESIZE_BOTTOM_LEFT):
                new_w = max(self.minimumWidth(), geom.width() - delta.x())
                geom.setLeft(geom.right() - new_w)
            if self._resize_direction in (RESIZE_TOP, RESIZE_TOP_LEFT, RESIZE_TOP_RIGHT):
                new_h = max(self.minimumHeight(), geom.height() - delta.y())
                geom.setTop(geom.bottom() - new_h)

            self.setGeometry(geom)
            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resize_direction = RESIZE_NONE
        self._drag_start = None
        self._drag_geom = None
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        """Paint rounded corners on the container."""
        super().paintEvent(event)
