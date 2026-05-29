"""QSS stylesheet generator for dark/light themes."""


def generate_stylesheet(theme: str, font_scale: float = 1.0) -> str:
    """Generate a complete QSS stylesheet for the given theme."""
    if theme == "dark":
        colors = {
            "bg_primary": "#1a1a2e",
            "bg_secondary": "#16213e",
            "bg_tertiary": "#0f3460",
            "text_primary": "#e0e0e0",
            "text_secondary": "#8899aa",
            "accent": "#00d4aa",
            "border": "#2a2a4a",
            "receive_bg": "#0d1117",
            "send_bg": "#161b22",
            "title_bar": "#1a1a2e",
            "input_bg": "#0d1117",
            "hover": "#1a2744",
            "selection": "#0f3460",
        }
    else:
        colors = {
            "bg_primary": "#f0f0f5",
            "bg_secondary": "#ffffff",
            "bg_tertiary": "#e8e8ed",
            "text_primary": "#1a1a2e",
            "text_secondary": "#666677",
            "accent": "#0088cc",
            "border": "#ccccdd",
            "receive_bg": "#fafafa",
            "send_bg": "#ffffff",
            "title_bar": "#e8e8ed",
            "input_bg": "#ffffff",
            "hover": "#dde4ee",
            "selection": "#cce0f0",
        }

    base_size = int(12 * font_scale)
    small_size = max(9, int(10 * font_scale))

    return f"""
    /* Global */
    QWidget {{
        font-size: {base_size}px;
        color: {colors['text_primary']};
    }}

    /* ComboBox */
    QComboBox {{
        background: {colors['input_bg']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        border-radius: 4px;
        padding: 4px 8px;
        min-height: 20px;
        font-size: {small_size}px;
    }}
    QComboBox:hover {{
        border-color: {colors['accent']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox QAbstractItemView {{
        background: {colors['bg_secondary']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        selection-background-color: {colors['selection']};
    }}

    /* TextEdit / PlainTextEdit */
    QPlainTextEdit, QTextEdit, QLineEdit {{
        background: {colors['input_bg']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        border-radius: 4px;
        padding: 4px;
        font-family: monospace;
        font-size: {base_size}px;
    }}
    QPlainTextEdit:focus, QTextEdit:focus, QLineEdit:focus {{
        border-color: {colors['accent']};
    }}

    /* ScrollBar */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {colors['border']};
        border-radius: 4px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {colors['text_secondary']};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {colors['border']};
        border-radius: 4px;
        min-width: 30px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {colors['text_secondary']};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}

    /* Menu */
    QMenu {{
        background: {colors['bg_secondary']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        border-radius: 6px;
        padding: 4px;
    }}
    QMenu::item {{
        padding: 6px 20px;
        border-radius: 4px;
    }}
    QMenu::item:selected {{
        background: {colors['hover']};
    }}

    /* Dialog */
    QDialog {{
        background: {colors['bg_secondary']};
    }}

    /* Label */
    QLabel {{
        color: {colors['text_primary']};
    }}

    /* CheckBox */
    QCheckBox {{
        color: {colors['text_primary']};
        spacing: 6px;
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {colors['border']};
        border-radius: 3px;
        background: {colors['input_bg']};
    }}
    QCheckBox::indicator:checked {{
        background: {colors['accent']};
        border-color: {colors['accent']};
    }}

    /* Slider */
    QSlider::groove:horizontal {{
        border: none;
        height: 4px;
        background: {colors['bg_tertiary']};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {colors['accent']};
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }}
    QSlider::sub-page:horizontal {{
        background: {colors['accent']};
        border-radius: 2px;
    }}

    /* ScrollArea */
    QScrollArea {{
        border: none;
        background: transparent;
    }}

    /* SpinBox */
    QSpinBox {{
        background: {colors['input_bg']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        border-radius: 4px;
        padding: 2px 4px;
    }}
    QSpinBox:focus {{
        border-color: {colors['accent']};
    }}

    /* ToolTip */
    QToolTip {{
        background: {colors['bg_secondary']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        padding: 4px;
        font-size: {small_size}px;
    }}

    /* Splitter */
    QSplitter::handle {{
        background: {colors['border']};
    }}
    QSplitter::handle:horizontal {{
        width: 1px;
    }}
    QSplitter::handle:vertical {{
        height: 1px;
    }}
    """
