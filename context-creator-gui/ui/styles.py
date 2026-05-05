def get_stylesheet():
    return """
        QMainWindow, QWidget {
            background-color: #F8FAFC;
            color: #1E293B;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 14px;
        }
        QWidget#topBar { background-color: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #E2E8F0; }
        QLabel#appLogo { color: #0F172A; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
        QLineEdit, QTextEdit, QComboBox { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px 12px; color: #0F172A; selection-background-color: #8B5CF6; selection-color: #FFFFFF; }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #8B5CF6; outline: none; }
        QComboBox::drop-down { border: none; width: 30px; }
        QComboBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #64748B; margin-right: 10px; }
        QComboBox QAbstractItemView { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; selection-background-color: #F1F5F9; selection-color: #0F172A; }
        QPushButton { background-color: #8B5CF6; color: #FFFFFF; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 14px; border: none; }
        QPushButton:hover { background-color: #7C3AED; }
        QPushButton:pressed { background-color: #6D28D9; }
        QPushButton:disabled { background-color: #E2E8F0; color: #94A3B8; }
        QPushButton#btnSecondary { background-color: #FFFFFF; color: #4F46E5; border: 1px solid #C7D2FE; }
        QPushButton#btnSecondary:hover { background-color: #EEF2FF; border-color: #818CF8; }
        QPushButton#btnStop { background-color: #EF4444; }
        QPushButton#btnStop:hover { background-color: #DC2626; }
        QPushButton.home-btn { background-color: #FFFFFF; border: 1px solid #E2E8F0; color: #0F172A; padding: 16px 20px; font-size: 15px; font-weight: 600; text-align: left; border-radius: 12px; }
        QPushButton.home-btn:hover { border: 1px solid #8B5CF6; background-color: #F5F3FF; color: #6D28D9; }
        QPushButton#btnBack { background-color: transparent; border: none; color: #64748B; padding: 8px; border-radius: 6px; }
        QPushButton#btnBack:hover { background-color: #E2E8F0; color: #0F172A; }
        QGroupBox { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; margin-top: 28px; padding: 20px 24px 24px 24px; }
        QGroupBox::title { subcontrol-origin: margin; left: 16px; top: 8px; padding: 0 8px; background-color: #FFFFFF; color: #475569; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; text-transform: uppercase; }
        QLabel { color: #334155; font-weight: 500; }
        QCheckBox { spacing: 8px; color: #334155; font-weight: 500; padding-left: 2px; }
        QCheckBox::indicator { width: 18px; height: 18px; border: 1.5px solid #CBD5E1; border-radius: 4px; background-color: #FFFFFF; margin-left: 2px; }
        QCheckBox::indicator:hover { border-color: #8B5CF6; }
        QCheckBox::indicator:checked { background-color: #8B5CF6; border-color: #8B5CF6; image: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTEuNjY2NiAzLjVMNS4yNDk5MiA5LjkxNjY3TDIuMzMzMjUgNyIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4="); }
        QProgressBar { border: none; border-radius: 4px; text-align: center; color: transparent; background-color: #E2E8F0; }
        QProgressBar::chunk { background-color: #8B5CF6; border-radius: 4px; }
        QTextEdit#logOutput { background-color: #0F172A; color: #E2E8F0; font-family: "JetBrains Mono", Consolas, "Courier New", monospace; font-size: 13px; border: 1px solid #1E293B; border-radius: 8px; padding: 10px; }
        QTextEdit#previewText { background-color: #FFFFFF; color: #334155; font-family: "JetBrains Mono", Consolas, "Courier New", monospace; font-size: 13px; line-height: 1.6; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; }
        QScrollArea { border: none; background-color: transparent; }
        QScrollArea > QWidget > QWidget { background-color: transparent; }
        QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
        QScrollBar::handle:vertical { background: #CBD5E1; border-radius: 5px; min-height: 40px; }
        QScrollBar::handle:vertical:hover { background: #94A3B8; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        QScrollBar:horizontal { background: transparent; height: 10px; margin: 0; }
        QScrollBar::handle:horizontal { background: #CBD5E1; border-radius: 5px; min-width: 40px; }
        QScrollBar::handle:horizontal:hover { background: #94A3B8; }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
        QLabel#pageTitle { color: #0F172A; font-size: 32px; font-weight: 800; letter-spacing: -0.8px; }
        QLabel#pageSubTitle { color: #64748B; font-size: 15px; }
        QLabel#statusPill { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; padding: 6px 14px; border-radius: 14px; font-weight: 600; font-size: 13px; }
    """