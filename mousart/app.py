"""Application entry point for MOUSART."""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon

from mousart import __version__, __app_name__
from mousart.core.theme_manager import ThemeManager
from mousart.core.serial_manager import SerialPortManager
from mousart.core.virtual_serial_manager import VirtualSerialManager
from mousart.core.config_manager import ConfigManager
from mousart.core.data_analyzer import DataAnalyzer
from mousart.core.log_file_manager import LogFileManager
from mousart.ui.main_window import MainWindow


def main():
    """Main entry point for MOUSART application."""
    # High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setApplicationName(__app_name__)
    app.setApplicationVersion(__version__)
    app.setOrganizationName(__app_name__)
    app.setOrganizationDomain("mousart.dev")

    # Set application icon
    icon_paths = [
        os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "mousart_256.png"),
        os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "mousart_128.png"),
        os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "mousart_64.png"),
        os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "mousart_48.png"),
        os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "mousart_32.png"),
        os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "mousart_16.png"),
    ]
    for path in icon_paths:
        if os.path.isfile(path):
            app.setWindowIcon(QIcon(path))
            break

    # Create managers
    theme_manager = ThemeManager()
    serial_manager = SerialPortManager()
    virtual_manager = VirtualSerialManager()
    config_manager = ConfigManager()
    data_analyzer = DataAnalyzer()
    log_file_manager = LogFileManager()

    # Create and show main window
    window = MainWindow(
        theme_manager=theme_manager,
        serial_manager=serial_manager,
        virtual_manager=virtual_manager,
        config_manager=config_manager,
        data_analyzer=data_analyzer,
        log_file_manager=log_file_manager
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
