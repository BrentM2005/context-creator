from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, 
    QProgressBar, QTextEdit, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
import qtawesome as qta
from core.i18n import i18n
from ui.views.form.source_group import SourceGroup
from ui.views.form.output_group import OutputGroup
from ui.views.form.filters_group import FiltersGroup
from ui.views.form.extensions_group import ExtensionsGroup
from ui.views.form.ai_group import AIGroup

class FormView(QWidget):
    navigate_back_requested = Signal()
    generate_requested = Signal()
    stop_requested = Signal()
    history_selected = Signal(int)
    open_dir_requested = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = "local"
        self._build_ui()
        self.retranslate_ui()
        
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 25)
        layout.setSpacing(18)
        
        app_top = QHBoxLayout()
        self.btn_back_app = QPushButton()
        self.btn_back_app.setObjectName("btnBack")
        self.btn_back_app.setIcon(qta.icon('fa5s.arrow-left', color='#64748B'))
        self.btn_back_app.setCursor(Qt.PointingHandCursor)
        self.btn_back_app.clicked.connect(self.navigate_back_requested.emit)
        
        self.lbl_history = QLabel()
        self.cmb_history = QComboBox()
        self.cmb_history.setMinimumWidth(380)
        self.cmb_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cmb_history.setCursor(Qt.PointingHandCursor)
        self.cmb_history.currentIndexChanged.connect(self.history_selected.emit)
        
        app_top.addWidget(self.btn_back_app)
        app_top.addStretch()
        app_top.addWidget(self.lbl_history)
        app_top.addWidget(self.cmb_history)
        layout.addLayout(app_top)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_layout_outer = QVBoxLayout(scroll_content)
        scroll_layout_outer.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        scroll_layout_outer.setContentsMargins(0, 0, 0, 0)
        
        form_container = QWidget()
        form_container.setMaximumWidth(900)
        form_container.setMinimumWidth(700)
        scroll_layout = QVBoxLayout(form_container)
        scroll_layout.setContentsMargins(4, 8, 4, 16)
        scroll_layout.setSpacing(20)
        
        self.source_group = SourceGroup()
        self.output_group = OutputGroup()
        self.filters_group = FiltersGroup()
        self.extensions_group = ExtensionsGroup()
        self.ai_group = AIGroup()
        
        scroll_layout.addWidget(self.source_group)
        scroll_layout.addWidget(self.output_group)
        scroll_layout.addWidget(self.filters_group)
        scroll_layout.addWidget(self.extensions_group)
        scroll_layout.addWidget(self.ai_group)
        
        scroll_layout_outer.addWidget(form_container)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        exec_layout = QHBoxLayout()
        self.btn_generate = QPushButton()
        self.btn_generate.setIcon(qta.icon('fa5s.play', color='#FFFFFF'))
        self.btn_generate.clicked.connect(self.generate_requested.emit)
        
        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("btnStop")
        self.btn_stop.setIcon(qta.icon('fa5s.stop', color='#FFFFFF'))
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_requested.emit)
        
        self.btn_clear_form = QPushButton()
        self.btn_clear_form.setObjectName("btnSecondary")
        self.btn_clear_form.setIcon(qta.icon('fa5s.eraser', color='#4F46E5'))
        self.btn_clear_form.clicked.connect(self.clear_form)
        
        self.btn_open_dir = QPushButton()
        self.btn_open_dir.setObjectName("btnSecondary")
        self.btn_open_dir.setIcon(qta.icon('fa5s.external-link-square-alt', color='#4F46E5'))
        self.btn_open_dir.setEnabled(False)
        self.btn_open_dir.clicked.connect(lambda: self.open_dir_requested.emit(self.output_group.get_data().get("output_dir", "")))
        
        exec_layout.addWidget(self.btn_generate, stretch=5)
        exec_layout.addWidget(self.btn_stop, stretch=2)
        exec_layout.addWidget(self.btn_clear_form, stretch=2)
        exec_layout.addWidget(self.btn_open_dir, stretch=3)
        layout.addLayout(exec_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        layout.addWidget(self.progress_bar)
        
        self.lbl_status = QLabel("Ready.")
        self.lbl_status.setObjectName("statusPill")
        layout.addWidget(self.lbl_status)
        
        self.txt_log = QTextEdit()
        self.txt_log.setObjectName("logOutput")
        self.txt_log.setReadOnly(True)
        self.txt_log.setMinimumHeight(160)
        self.txt_log.setMaximumHeight(220)
        layout.addWidget(self.txt_log)

    def set_mode(self, mode):
        self.current_mode = mode
        self.source_group.set_mode(mode)

    def clear_form(self):
        self.source_group.clear_form()
        self.output_group.clear_form()
        self.filters_group.clear_form()
        self.extensions_group.clear_form()
        self.ai_group.clear_form()
        
        self.cmb_history.blockSignals(True)
        self.cmb_history.setCurrentIndex(-1)
        self.cmb_history.blockSignals(False)

    def get_form_data(self):
        data = {}
        data.update(self.source_group.get_data())
        data.update(self.output_group.get_data())
        data.update(self.filters_group.get_data())
        data.update(self.extensions_group.get_data())
        data.update(self.ai_group.get_data())
        return data

    def set_form_data(self, cfg):
        self.source_group.set_data(cfg)
        self.output_group.set_data(cfg)
        self.filters_group.set_data(cfg)
        self.extensions_group.set_data(cfg)
        self.ai_group.set_data(cfg)

    def set_history_items(self, items):
        self.cmb_history.blockSignals(True)
        self.cmb_history.clear()
        for icon_str, text in items:
            if icon_str: self.cmb_history.addItem(qta.icon(icon_str, color='#8B5CF6'), text)
            else: self.cmb_history.addItem(text)
        self.cmb_history.blockSignals(False)

    def set_generating_state(self, is_generating, stopping=False):
        if is_generating:
            self.btn_generate.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.btn_open_dir.setEnabled(False)
            self.btn_clear_form.setEnabled(False)
            self.progress_bar.setValue(0)
            self.txt_log.clear()
        else:
            self.btn_generate.setEnabled(True)
            self.btn_stop.setEnabled(False)
            self.btn_clear_form.setEnabled(True)
            if not stopping: self.btn_open_dir.setEnabled(True)

    def set_status(self, message, good=True):
        self.lbl_status.setText(message)
        if good: self.lbl_status.setStyleSheet("QLabel#statusPill { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; padding: 6px 14px; border-radius: 14px; font-weight: 600; font-size: 13px; }")
        else: self.lbl_status.setStyleSheet("QLabel#statusPill { background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; padding: 6px 14px; border-radius: 14px; font-weight: 600; font-size: 13px; }")

    def append_log(self, msg):
        self.txt_log.append(msg)
        self.txt_log.verticalScrollBar().setValue(self.txt_log.verticalScrollBar().maximum())

    def update_progress(self, val):
        self.progress_bar.setValue(val)

    def retranslate_ui(self):
        self.btn_back_app.setText(i18n.tr("btn_back"))
        self.lbl_history.setText(i18n.tr("lbl_history"))
        
        self.source_group.retranslate_ui(self.current_mode)
        self.output_group.retranslate_ui()
        self.filters_group.retranslate_ui()
        self.extensions_group.retranslate_ui()
        self.ai_group.retranslate_ui()
        
        self.btn_generate.setText(i18n.tr("btn_generate"))
        self.btn_stop.setText(i18n.tr("btn_stop"))
        self.btn_clear_form.setText(i18n.tr("btn_clear"))
        self.btn_open_dir.setText(i18n.tr("btn_open"))