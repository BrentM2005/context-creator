from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QGuiApplication
import qtawesome as qta
from core.constants import DOC_TEMPLATES
from core.i18n import i18n

class TemplatesView(QWidget):
    navigate_back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.retranslate_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        app_top = QHBoxLayout()
        self.btn_back_tpl = QPushButton()
        self.btn_back_tpl.setObjectName("btnBack")
        self.btn_back_tpl.setIcon(qta.icon('fa5s.arrow-left', color='#64748B'))
        self.btn_back_tpl.setIconSize(QSize(18, 18))
        self.btn_back_tpl.setCursor(Qt.PointingHandCursor)
        self.btn_back_tpl.clicked.connect(self.navigate_back_requested.emit)
        app_top.addWidget(self.btn_back_tpl)
        app_top.addStretch()
        layout.addLayout(app_top)

        header_layout = QVBoxLayout()
        self.lbl_tpl_title = QLabel()
        self.lbl_tpl_title.setObjectName("pageTitle")
        self.lbl_tpl_sub = QLabel()
        self.lbl_tpl_sub.setObjectName("pageSubTitle")
        self.lbl_tpl_sub.setWordWrap(True)
        header_layout.addWidget(self.lbl_tpl_title)
        header_layout.addWidget(self.lbl_tpl_sub)
        layout.addLayout(header_layout)

        ctl_layout = QHBoxLayout()
        ctl_layout.setSpacing(16)
        self.lbl_tpl_type = QLabel()
        
        self.cmb_templates = QComboBox()
        self.cmb_templates.addItems(list(DOC_TEMPLATES.keys()))
        self.cmb_templates.setMinimumWidth(320)
        self.cmb_templates.setCursor(Qt.PointingHandCursor)
        self.cmb_templates.currentIndexChanged.connect(self._update_template_preview)
        
        self.btn_copy_tpl = QPushButton()
        self.btn_copy_tpl.setIcon(qta.icon('fa5s.copy', color='#FFFFFF'))
        self.btn_copy_tpl.setCursor(Qt.PointingHandCursor)
        self.btn_copy_tpl.clicked.connect(self._copy_template)
        
        ctl_layout.addWidget(self.lbl_tpl_type)
        ctl_layout.addWidget(self.cmb_templates)
        ctl_layout.addWidget(self.btn_copy_tpl)
        ctl_layout.addStretch()
        layout.addLayout(ctl_layout)

        self.lbl_preview = QLabel()
        self.lbl_preview.setStyleSheet("margin-top: 8px; color: #64748B; font-weight: 600;")
        layout.addWidget(self.lbl_preview)

        self.txt_tpl_preview = QTextEdit()
        self.txt_tpl_preview.setObjectName("previewText")
        self.txt_tpl_preview.setReadOnly(True)
        self.txt_tpl_preview.setMinimumHeight(520)
        layout.addWidget(self.txt_tpl_preview)

        self._update_template_preview()

    def _update_template_preview(self):
        sel = self.cmb_templates.currentText()
        text = DOC_TEMPLATES.get(sel, "")
        self.txt_tpl_preview.setText(text)

    def _copy_template(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.txt_tpl_preview.toPlainText())
        QMessageBox.information(self, "Copied", i18n.tr("msg_copied"))

    def retranslate_ui(self):
        self.btn_back_tpl.setText(i18n.tr("btn_back"))
        self.lbl_tpl_title.setText(i18n.tr("templates_title"))
        self.lbl_tpl_sub.setText(i18n.tr("templates_sub"))
        self.lbl_tpl_type.setText(i18n.tr("lbl_template_type"))
        self.btn_copy_tpl.setText(i18n.tr("btn_copy_prompt"))
        self.lbl_preview.setText(i18n.tr("lbl_preview"))