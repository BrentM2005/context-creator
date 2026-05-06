import sys
import os
import platform
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
    if platform.system() == "Windows":
        import ctypes
        try:
            myappid = 'brentm2005.contextcreator.gui.1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(
        app.highDpiScaleFactorRoundingPolicy().PassThrough
    )
    
    icon_path = resource_path("logo.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        
    window = CodebaseToMarkdownApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()