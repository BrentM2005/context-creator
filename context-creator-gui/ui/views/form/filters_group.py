from PySide6.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox
from core.i18n import i18n

class FiltersGroup(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        fil_layout = QGridLayout(self)
        self.lbl_max_size = QLabel()
        self.txt_max_size = QLineEdit("500")
        self.lbl_max_lines = QLabel()
        self.txt_max_lines = QLineEdit("2000")
        self.chk_gitignore = QCheckBox()
        self.chk_gitignore.setChecked(True)
        
        fil_layout.addWidget(self.lbl_max_size, 0, 0)
        fil_layout.addWidget(self.txt_max_size, 0, 1)
        fil_layout.addWidget(self.lbl_max_lines, 1, 0)
        fil_layout.addWidget(self.txt_max_lines, 1, 1)
        fil_layout.addWidget(self.chk_gitignore, 2, 0, 1, 2)
        
        self.lbl_formatting = QLabel()
        self.chk_line_num = QCheckBox()
        self.chk_no_comment = QCheckBox()
        self.chk_no_empty = QCheckBox()
        fmt_layout = QHBoxLayout()
        fmt_layout.addWidget(self.chk_line_num)
        fmt_layout.addWidget(self.chk_no_comment)
        fmt_layout.addWidget(self.chk_no_empty)
        fmt_layout.addStretch()
        
        fil_layout.addWidget(self.lbl_formatting, 3, 0)
        fil_layout.addLayout(fmt_layout, 3, 1)

    def get_data(self):
        return {
            "max_size_kb": self.txt_max_size.text(),
            "max_lines": self.txt_max_lines.text(),
            "use_gitignore": self.chk_gitignore.isChecked(),
            "include_line_numbers": self.chk_line_num.isChecked(),
            "remove_comments": self.chk_no_comment.isChecked(),
            "remove_empty_lines": self.chk_no_empty.isChecked(),
        }

    def set_data(self, cfg):
        self.txt_max_size.setText(cfg.get("max_size_kb", "500"))
        self.txt_max_lines.setText(cfg.get("max_lines", "2000"))
        self.chk_gitignore.setChecked(cfg.get("use_gitignore", True))
        self.chk_line_num.setChecked(cfg.get("include_line_numbers", False))
        self.chk_no_comment.setChecked(cfg.get("remove_comments", False))
        self.chk_no_empty.setChecked(cfg.get("remove_empty_lines", False))

    def clear_form(self):
        self.txt_max_size.setText("500")
        self.txt_max_lines.setText("2000")
        self.chk_gitignore.setChecked(True)
        self.chk_line_num.setChecked(False)
        self.chk_no_comment.setChecked(False)
        self.chk_no_empty.setChecked(False)

    def retranslate_ui(self):
        self.setTitle(i18n.tr("sec_filters"))
        self.lbl_max_size.setText(i18n.tr("lbl_max_size"))
        self.lbl_max_lines.setText(i18n.tr("lbl_max_lines"))
        self.chk_gitignore.setText(i18n.tr("chk_gitignore"))
        self.lbl_formatting.setText(i18n.tr("lbl_formatting"))
        self.chk_line_num.setText(i18n.tr("chk_line_num"))
        self.chk_no_comment.setText(i18n.tr("chk_no_comment"))
        self.chk_no_empty.setText(i18n.tr("chk_no_empty"))