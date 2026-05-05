from PySide6.QtWidgets import QGroupBox, QGridLayout, QLabel, QLineEdit
from core.i18n import i18n

class ExtensionsGroup(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        ext_layout = QGridLayout(self)
        self.lbl_exts = QLabel()
        self.txt_exts = QLineEdit()
        self.lbl_ignores = QLabel()
        self.txt_ignores = QLineEdit()
        ext_layout.addWidget(self.lbl_exts, 0, 0)
        ext_layout.addWidget(self.txt_exts, 0, 1)
        ext_layout.addWidget(self.lbl_ignores, 1, 0)
        ext_layout.addWidget(self.txt_ignores, 1, 1)

    def get_data(self):
        return {
            "extensions": self.txt_exts.text(),
            "custom_ignores": self.txt_ignores.text(),
        }

    def set_data(self, cfg):
        self.txt_exts.setText(cfg.get("extensions", ""))
        self.txt_ignores.setText(cfg.get("custom_ignores", ""))

    def clear_form(self):
        self.txt_exts.clear()
        self.txt_ignores.clear()

    def retranslate_ui(self):
        self.setTitle(i18n.tr("sec_exts"))
        self.lbl_exts.setText(i18n.tr("lbl_exts"))
        self.lbl_ignores.setText(i18n.tr("lbl_ignores"))