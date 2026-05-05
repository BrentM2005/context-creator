from PySide6.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, QFileDialog
from PySide6.QtCore import Qt
import qtawesome as qta
from core.i18n import i18n
from ui.widgets import DropLineEdit

class OutputGroup(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        out_layout = QGridLayout(self)
        self.lbl_out_dir = QLabel()
        self.txt_out_dir = DropLineEdit()
        self.btn_browse_out = QPushButton()
        self.btn_browse_out.setObjectName("btnSecondary")
        self.btn_browse_out.setIcon(qta.icon('fa5s.folder-open', color='#4F46E5'))
        self.btn_browse_out.clicked.connect(self._browse_output)
        out_layout.addWidget(self.lbl_out_dir, 0, 0)
        out_layout.addWidget(self.txt_out_dir, 0, 1)
        out_layout.addWidget(self.btn_browse_out, 0, 2)

        self.lbl_out_file = QLabel()
        self.txt_out_file = QLineEdit("my_project.md")
        out_layout.addWidget(self.lbl_out_file, 1, 0)
        out_layout.addWidget(self.txt_out_file, 1, 1, 1, 2)

        self.lbl_artifacts = QLabel()
        self.chk_tech = QCheckBox("Tech Stack")
        self.chk_tech.setChecked(True)
        self.chk_mermaid = QCheckBox("Mermaid Graph")
        self.chk_prompt = QCheckBox("Prompt Pack")
        art_layout = QHBoxLayout()
        art_layout.addWidget(self.chk_tech)
        art_layout.addWidget(self.chk_mermaid)
        art_layout.addWidget(self.chk_prompt)
        art_layout.addStretch()
        out_layout.addWidget(self.lbl_artifacts, 2, 0)
        out_layout.addLayout(art_layout, 2, 1, 1, 2)

        self.lbl_format = QLabel()
        self.cmb_format = QComboBox()
        self.cmb_format.addItems(["ChatGPT / Standard (Markdown)", "Claude Optimized (XML)", "Gemini Optimized (Delimited)", "JSON Structured Export", "Raw Text"])
        self.chk_clipboard = QCheckBox()
        out_layout.addWidget(self.lbl_format, 3, 0)
        out_layout.addWidget(self.cmb_format, 3, 1)
        out_layout.addWidget(self.chk_clipboard, 3, 2)

    def _browse_output(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if d: self.txt_out_dir.setText(d)

    def get_data(self):
        return {
            "output_dir": self.txt_out_dir.text(),
            "output_file": self.txt_out_file.text(),
            "llm_opt": self.cmb_format.currentText(),
            "generate_tech_stack": self.chk_tech.isChecked(),
            "mermaid_graph": self.chk_mermaid.isChecked(),
            "prompt_packs": self.chk_prompt.isChecked(),
            "clipboard_mode": self.chk_clipboard.isChecked(),
        }

    def set_data(self, cfg):
        self.txt_out_dir.setText(cfg.get("output_dir", ""))
        self.txt_out_file.setText(cfg.get("output_file", "my_project.md"))
        self.cmb_format.setCurrentText(cfg.get("llm_opt", "ChatGPT / Standard (Markdown)"))
        self.chk_tech.setChecked(cfg.get("generate_tech_stack", True))
        self.chk_mermaid.setChecked(cfg.get("mermaid_graph", False))
        self.chk_prompt.setChecked(cfg.get("prompt_packs", False))
        self.chk_clipboard.setChecked(cfg.get("clipboard_mode", False))

    def clear_form(self):
        self.txt_out_dir.clear()
        self.txt_out_file.setText("my_project.md")
        self.cmb_format.setCurrentIndex(0)
        self.chk_tech.setChecked(True)
        self.chk_mermaid.setChecked(False)
        self.chk_prompt.setChecked(False)
        self.chk_clipboard.setChecked(False)

    def retranslate_ui(self):
        self.setTitle(i18n.tr("sec_output"))
        self.lbl_out_dir.setText(i18n.tr("lbl_out_dir"))
        self.lbl_out_file.setText(i18n.tr("lbl_out_file"))
        self.btn_browse_out.setText(i18n.tr("btn_browse"))
        self.lbl_artifacts.setText(i18n.tr("lbl_artifacts"))
        self.lbl_format.setText(i18n.tr("lbl_format"))
        self.chk_clipboard.setText(i18n.tr("lbl_clipboard"))