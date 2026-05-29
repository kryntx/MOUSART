"""Editable combo box for custom baud rate entry."""
from PyQt6.QtWidgets import QComboBox, QCompleter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator


class EditableComboBox(QComboBox):
    """Editable combo box with integer validator for baud rate entry."""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self.setEditable(True)
        self.setFixedHeight(28)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        # Set integer validator for baud rate
        validator = QIntValidator(1, 9999999, self)
        self.lineEdit().setValidator(validator)

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
            EditableComboBox {{
                background: {bg};
                color: {text};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }}
            EditableComboBox:hover {{
                border-color: {accent};
            }}
            EditableComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            EditableComboBox QAbstractItemView {{
                background: {bg_sec};
                color: {text};
                border: 1px solid {border};
                selection-background-color: {hover};
                outline: none;
            }}
        """)
