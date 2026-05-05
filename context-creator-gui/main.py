import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.app import CodebaseToMarkdownApp

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    app.setHighDpiScaleFactorRoundingPolicy(
        app.highDpiScaleFactorRoundingPolicy().PassThrough
    )
    
    icon_path = resource_path("icon.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    window = CodebaseToMarkdownApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()