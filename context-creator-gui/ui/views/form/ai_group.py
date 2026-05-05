from PySide6.QtWidgets import QGroupBox, QGridLayout, QLabel, QComboBox, QLineEdit, QCheckBox
from core.i18n import i18n

class AIGroup(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        ai_layout = QGridLayout(self)
        self.lbl_git_mode = QLabel()
        self.cmb_git_mode = QComboBox()
        self.cmb_git_mode.addItems(["All Files", "Changed vs HEAD", "Changed vs main"])
        
        self.lbl_budget = QLabel()
        self.cmb_budget = QComboBox()
        self.cmb_budget.addItems(["None", "GPT-4o (128k)", "Claude (200k)", "Gemini (1M)", "Custom"])
        self.txt_budget = QLineEdit("100000")
        self.txt_budget.setEnabled(False)
        self.cmb_budget.currentIndexChanged.connect(
            lambda: self.txt_budget.setEnabled(self.cmb_budget.currentText() == "Custom")
        )
        
        ai_layout.addWidget(self.lbl_git_mode, 0, 0)
        ai_layout.addWidget(self.cmb_git_mode, 0, 1)
        ai_layout.addWidget(self.lbl_budget, 0, 2)
        ai_layout.addWidget(self.cmb_budget, 0, 3)
        ai_layout.addWidget(self.txt_budget, 0, 4)
        
        self.chk_secrets = QCheckBox()
        self.chk_secrets.setChecked(True)
        self.chk_summaries = QCheckBox()
        self.chk_summaries.setChecked(True)
        ai_layout.addWidget(self.chk_secrets, 1, 0, 1, 2)
        ai_layout.addWidget(self.chk_summaries, 1, 2, 1, 3)

    def get_data(self):
        return {
            "git_mode": self.cmb_git_mode.currentText(),
            "token_budget": self.cmb_budget.currentText(),
            "custom_budget": self.txt_budget.text(),
            "secret_scan": self.chk_secrets.isChecked(),
            "summaries": self.chk_summaries.isChecked()
        }

    def set_data(self, cfg):
        self.cmb_git_mode.setCurrentText(cfg.get("git_mode", "All Files"))
        self.cmb_budget.setCurrentText(cfg.get("token_budget", "None"))
        self.txt_budget.setText(cfg.get("custom_budget", "100000"))
        self.chk_secrets.setChecked(cfg.get("secret_scan", True))
        self.chk_summaries.setChecked(cfg.get("summaries", True))

    def clear_form(self):
        self.cmb_git_mode.setCurrentIndex(0)
        self.cmb_budget.setCurrentIndex(0)
        self.txt_budget.setText("100000")
        self.txt_budget.setEnabled(False)
        self.chk_secrets.setChecked(True)
        self.chk_summaries.setChecked(True)

    def retranslate_ui(self):
        self.setTitle(i18n.tr("sec_ai"))
        self.lbl_git_mode.setText(i18n.tr("lbl_git_mode"))
        self.lbl_budget.setText(i18n.tr("lbl_budget"))
        self.chk_secrets.setText(i18n.tr("chk_secrets"))
        self.chk_summaries.setText(i18n.tr("chk_summaries"))