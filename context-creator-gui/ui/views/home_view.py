from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QGridLayout, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
import qtawesome as qta
from core.i18n import i18n

class HomeView(QWidget):
    navigate_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.retranslate_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(32, 28, 32, 48)

        container = QWidget()
        container.setMaximumWidth(740)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(24)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        self.lbl_home_title = QLabel()
        self.lbl_home_title.setObjectName("pageTitle")
        self.lbl_home_title.setAlignment(Qt.AlignCenter)
        
        self.lbl_home_sub = QLabel()
        self.lbl_home_sub.setObjectName("pageSubTitle")
        self.lbl_home_sub.setAlignment(Qt.AlignCenter)
        self.lbl_home_sub.setWordWrap(True)
        
        header_layout.addWidget(self.lbl_home_title)
        header_layout.addWidget(self.lbl_home_sub)
        container_layout.addLayout(header_layout)

        intro_card = QGroupBox()
        intro_layout = QVBoxLayout(intro_card)
        intro_layout.setSpacing(18)
        intro_layout.setContentsMargins(24, 24, 24, 24)
        
        self.lbl_home_hint = QLabel()
        self.lbl_home_hint.setWordWrap(True)
        self.lbl_home_hint.setStyleSheet("color: #475569; font-size: 14px;")
        self.lbl_home_hint.setAlignment(Qt.AlignCenter)
        intro_layout.addWidget(self.lbl_home_hint)

        btn_layout = QGridLayout()
        btn_layout.setSpacing(16)
        
        self.btn_nav_local = QPushButton()
        self.btn_nav_remote = QPushButton()
        self.btn_nav_pr = QPushButton()
        self.btn_nav_templates = QPushButton()

        for btn in[self.btn_nav_local, self.btn_nav_remote, self.btn_nav_pr, self.btn_nav_templates]:
            btn.setProperty("class", "home-btn")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setIconSize(QSize(22, 22))
            btn.setFixedHeight(68)

        self.btn_nav_local.setIcon(qta.icon('fa5s.folder-open', color='#8B5CF6'))
        self.btn_nav_remote.setIcon(qta.icon('fa5s.globe', color='#8B5CF6'))
        self.btn_nav_pr.setIcon(qta.icon('fa5s.code-branch', color='#8B5CF6'))
        self.btn_nav_templates.setIcon(qta.icon('fa5s.file-alt', color='#8B5CF6'))

        self.btn_nav_local.clicked.connect(lambda: self.navigate_requested.emit('local'))
        self.btn_nav_remote.clicked.connect(lambda: self.navigate_requested.emit('remote'))
        self.btn_nav_pr.clicked.connect(lambda: self.navigate_requested.emit('pr'))
        self.btn_nav_templates.clicked.connect(lambda: self.navigate_requested.emit('templates'))

        btn_layout.addWidget(self.btn_nav_local, 0, 0)
        btn_layout.addWidget(self.btn_nav_remote, 0, 1)
        btn_layout.addWidget(self.btn_nav_pr, 1, 0)
        btn_layout.addWidget(self.btn_nav_templates, 1, 1)

        intro_layout.addLayout(btn_layout)
        container_layout.addWidget(intro_card)

        footer = QLabel("Drag folders into the source fields. Your output stays neatly organized in one place.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #94A3B8; font-size: 13px; margin-top: 12px;")
        container_layout.addWidget(footer)
        layout.addWidget(container)

    def retranslate_ui(self):
        self.lbl_home_title.setText(i18n.tr("title_main"))
        self.lbl_home_sub.setText(i18n.tr("home_sub"))
        self.lbl_home_hint.setText(i18n.tr("home_sub") if hasattr(i18n, "tr") else "Choose a source type...")
        self.btn_nav_local.setText(i18n.tr("btn_local"))
        self.btn_nav_remote.setText(i18n.tr("btn_remote"))
        self.btn_nav_pr.setText(i18n.tr("btn_pr"))
        self.btn_nav_templates.setText(i18n.tr("btn_templates"))