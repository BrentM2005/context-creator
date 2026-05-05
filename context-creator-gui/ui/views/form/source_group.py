from PySide6.QtWidgets import QGroupBox, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt
import qtawesome as qta
from core.i18n import i18n
from ui.widgets import DropLineEdit

class SourceGroup(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.layout = QGridLayout(self)
        self.lbl_src_1 = QLabel()
        self.txt_src_1 = DropLineEdit()
        
        self.btn_browse_in = QPushButton()
        self.btn_browse_in.setObjectName("btnSecondary")
        self.btn_browse_in.setIcon(qta.icon('fa5s.search', color='#4F46E5') if 'qtawesome' in globals() else qta.icon('fa5s.search', color='#4F46E5'))
        self.btn_browse_in.clicked.connect(self._browse_input)

        self.lbl_src_2 = QLabel()
        self.txt_src_2 = QLineEdit()
        self.txt_src_2.setEchoMode(QLineEdit.Password)

    def _browse_input(self):
        d = QFileDialog.getExistingDirectory(self, "Select Code Directory")
        if d: self.txt_src_1.setText(d)

    def set_mode(self, mode):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget(): item.widget().hide()

        if mode == 'local':
            self.lbl_src_1.setText(i18n.tr("lbl_target_dir"))
            self.layout.addWidget(self.lbl_src_1, 0, 0)
            self.layout.addWidget(self.txt_src_1, 0, 1)
            self.layout.addWidget(self.btn_browse_in, 0, 2)
            self.btn_browse_in.show()
            self.txt_src_1.setPlaceholderText("Drop a code folder here or browse…")
            self.txt_src_2.setText("")
        elif mode == 'remote':
            self.lbl_src_1.setText(i18n.tr("lbl_repo_url"))
            self.lbl_src_2.setText(i18n.tr("lbl_auth_token"))
            self.layout.addWidget(self.lbl_src_1, 0, 0)
            self.layout.addWidget(self.txt_src_1, 0, 1, 1, 2)
            self.layout.addWidget(self.lbl_src_2, 1, 0)
            self.layout.addWidget(self.txt_src_2, 1, 1, 1, 2)
            self.lbl_src_2.show()
            self.txt_src_2.show()
            self.txt_src_1.setPlaceholderText("https://github.com/user/repo")
        elif mode == 'pr':
            self.lbl_src_1.setText("PR / MR URL:")
            self.lbl_src_2.setText(i18n.tr("lbl_auth_token"))
            self.layout.addWidget(self.lbl_src_1, 0, 0)
            self.layout.addWidget(self.txt_src_1, 0, 1, 1, 2)
            self.layout.addWidget(self.lbl_src_2, 1, 0)
            self.layout.addWidget(self.txt_src_2, 1, 1, 1, 2)
            self.lbl_src_2.show()
            self.txt_src_2.show()
            self.txt_src_1.setPlaceholderText("https://github.com/user/repo/pull/123")

        self.lbl_src_1.show()
        self.txt_src_1.show()

    def get_data(self):
        return {
            "src1": self.txt_src_1.text(),
            "src2": self.txt_src_2.text(),
        }

    def set_data(self, cfg):
        mode = cfg.get("mode", "local")
        if mode == 'local': self.txt_src_1.setText(cfg.get("input_dir", ""))
        elif mode == 'remote': self.txt_src_1.setText(cfg.get("repo_url", ""))
        elif mode == 'pr': self.txt_src_1.setText(cfg.get("pr_url", ""))
        self.txt_src_2.setText("")

    def clear_form(self):
        self.txt_src_1.clear()
        self.txt_src_2.clear()

    def retranslate_ui(self, current_mode):
        self.setTitle(i18n.tr("sec_source"))
        self.set_mode(current_mode)