"""Quick command button bar with flow layout."""
from mousart.qt_compat import *


class QuickCommandButton(QPushButton):
    """Individual quick command button."""

    send_requested = pyqtSignal(str, bool)
    edit_requested = pyqtSignal(int)

    def __init__(self, index: int, name: str, data: str, hex_mode: bool,
                 parent=None, theme_manager=None):
        super().__init__(name, parent)
        self._index = index
        self._data = data
        self._hex_mode = hex_mode
        self._theme_manager = theme_manager
        self.setFixedHeight(28)
        self.setCursor(self.cursor())
        self.setToolTip(f"{'HEX' if hex_mode else 'TXT'}: {data[:50]}")
        self.clicked.connect(lambda: self.send_requested.emit(self._data, self._hex_mode))
        self._update_style()

    def _update_style(self):
        accent = self._theme_manager.get_color_hex("accent") if self._theme_manager else "#00d4aa"
        bg = self._theme_manager.get_color_hex("bgTertiary") if self._theme_manager else "#0f3460"
        text = self._theme_manager.get_color_hex("textPrimary") if self._theme_manager else "#e0e0e0"
        border = self._theme_manager.get_color_hex("border") if self._theme_manager else "#2a2a4a"

        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {text};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 2px 8px;
                font-size: 10px;
            }}
            QPushButton:hover {{
                border-color: {accent};
                background: {accent};
                color: #ffffff;
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt_MouseButton_RightButton:
            self.edit_requested.emit(self._index)
        else:
            super().mousePressEvent(event)


class QuickCommandBar(QWidget):
    """Scrollable quick command button strip."""

    send_command = pyqtSignal(str, bool)
    add_requested = pyqtSignal()
    edit_requested = pyqtSignal(int)

    def __init__(self, parent=None, theme_manager=None, config_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._config_manager = config_manager
        self._hex_send = False

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.setSpacing(4)

        # Scroll area for commands
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt_ScrollBarPolicy_ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt_ScrollBarPolicy_ScrollBarAlwaysOff)
        self._scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._cmd_widget = QWidget()
        self._cmd_layout = QHBoxLayout(self._cmd_widget)
        self._cmd_layout.setContentsMargins(0, 0, 0, 0)
        self._cmd_layout.setSpacing(4)
        self._scroll.setWidget(self._cmd_widget)

        self._layout.addWidget(self._scroll, 1)

        # Add button
        self._add_btn = QPushButton("+")
        self._add_btn.setFixedSize(28, 28)
        self._add_btn.setCursor(self.cursor())
        self._add_btn.clicked.connect(self.add_requested.emit)
        self._layout.addWidget(self._add_btn)

        self._update_style()
        self._rebuild_buttons()

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self._update_style()

    def set_config_manager(self, cm):
        self._config_manager = cm
        self._rebuild_buttons()

    def set_hex_send(self, v: bool):
        self._hex_send = v

    def refresh(self):
        self._rebuild_buttons()

    def _rebuild_buttons(self):
        # Clear existing buttons
        while self._cmd_layout.count():
            item = self._cmd_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self._config_manager:
            return

        for i, cmd in enumerate(self._config_manager.quick_commands):
            btn = QuickCommandButton(
                i, cmd.get("name", "?"), cmd.get("data", ""),
                cmd.get("hex", False), theme_manager=self._theme_manager
            )
            btn.send_requested.connect(self.send_command.emit)
            btn.edit_requested.connect(self.edit_requested.emit)
            self._cmd_layout.addWidget(btn)

        self._cmd_layout.addStretch()

    def _update_style(self):
        accent = self._theme_manager.get_color_hex("accent") if self._theme_manager else "#00d4aa"
        bg = self._theme_manager.get_color_hex("bgTertiary") if self._theme_manager else "#0f3460"
        text = self._theme_manager.get_color_hex("textPrimary") if self._theme_manager else "#e0e0e0"
        border = self._theme_manager.get_color_hex("border") if self._theme_manager else "#2a2a4a"

        self._add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {accent};
                border: 1px dashed {accent};
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {accent};
                color: #ffffff;
            }}
        """)
