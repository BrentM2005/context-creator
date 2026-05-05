import os
import sys
import threading
import subprocess
from pathlib import Path
import qtawesome as qta
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QGuiApplication

from core.config_manager import ConfigManager
from core.i18n import i18n
from ui.styles import get_stylesheet
from ui.worker import GeneratorWorker
from ui.views.home_view import HomeView
from ui.views.form_view import FormView
from ui.views.templates_view import TemplatesView

class CodebaseToMarkdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Context Creator")
        self.resize(1080, 980)
        self.setMinimumSize(940, 820)
        
        self.current_mode = "home"
        self._cancel_event = threading.Event()
        self.config_manager = ConfigManager()
        self.thread = None
        self.worker = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._build_top_bar()

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.home_view = HomeView()
        self.form_view = FormView()
        self.templates_view = TemplatesView()

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.form_view)
        self.stack.addWidget(self.templates_view)

        self.setStyleSheet(get_stylesheet())
        self._connect_signals()
        self._update_history_combo()
        self.retranslate_ui()
        
        self.stack.setCurrentWidget(self.home_view)

    def _build_top_bar(self):
        self.top_bar_widget = QWidget()
        self.top_bar_widget.setObjectName("topBar")
        self.top_bar = QHBoxLayout(self.top_bar_widget)
        self.top_bar.setAlignment(Qt.AlignVCenter)
        self.top_bar.setContentsMargins(28, 16, 28, 16)
        self.top_bar.setSpacing(12)
        
        self.lbl_app_logo_icon = QLabel()
        self.lbl_app_logo_icon.setPixmap(qta.icon('fa5s.layer-group', color='#8B5CF6').pixmap(26, 26))
        self.lbl_app_logo = QLabel("Context Creator")
        self.lbl_app_logo.setObjectName("appLogo")
        self.top_bar.addWidget(self.lbl_app_logo_icon)
        self.top_bar.addWidget(self.lbl_app_logo)
        self.top_bar.addStretch()
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Español", "Français", "Português", "Deutsch"])
        self.lang_combo.setFixedWidth(130)
        self.lang_combo.setCursor(Qt.PointingHandCursor)
        self.top_bar.addWidget(self.lang_combo)
        
        self.main_layout.addWidget(self.top_bar_widget)

    def _connect_signals(self):
        self.lang_combo.currentIndexChanged.connect(self._change_language)
        self.home_view.navigate_requested.connect(self._show_app)
        self.templates_view.navigate_back_requested.connect(lambda: self.stack.setCurrentWidget(self.home_view))
        self.form_view.navigate_back_requested.connect(lambda: self.stack.setCurrentWidget(self.home_view))
        
        self.form_view.history_selected.connect(self._on_history_selected)
        self.form_view.generate_requested.connect(self._start_generation)
        self.form_view.stop_requested.connect(self._stop_generation)
        self.form_view.open_dir_requested.connect(self._open_output_dir)

    def _change_language(self, index):
        langs =["en", "es", "fr", "pt", "de"]
        i18n.set_lang(langs[index])
        self.retranslate_ui()

    def retranslate_ui(self):
        self.home_view.retranslate_ui()
        self.form_view.retranslate_ui()
        self.templates_view.retranslate_ui()

    def _show_app(self, mode):
        if mode == 'templates':
            self.stack.setCurrentWidget(self.templates_view)
        else:
            self.current_mode = mode
            self.form_view.set_mode(mode)
            self.stack.setCurrentWidget(self.form_view)
            self.form_view.set_status(f"Mode: {mode.capitalize()}")

    def _update_history_combo(self):
        history = self.config_manager.get_history()
        items =[]
        if not history:
            items.append((None, "No saved history yet..."))
        else:
            for cfg in history:
                mode = cfg.get("mode", "local")
                out = cfg.get("output_file", "my_project.md")
                if mode == 'local':
                    in_dir = cfg.get("input_dir", "")
                    name = Path(in_dir).name if in_dir else "Unknown Local"
                    items.append(('fa5s.folder', f"[Local] {name} -> {out}"))
                elif mode == 'pr':
                    url = cfg.get("pr_url", "")
                    name = url.rstrip('/').split('/')[-1] if url else "Unknown PR"
                    items.append(('fa5s.code-branch', f"[PR] #{name} -> {out}"))
                else:
                    url = cfg.get("repo_url", "")
                    name = url.rstrip('/').split('/')[-1].replace('.git', '') if url else "Unknown Remote"
                    items.append(('fa5s.globe', f"[Remote] {name} -> {out}"))
        self.form_view.set_history_items(items)

    def _on_history_selected(self, index):
        history = self.config_manager.get_history()
        if 0 <= index < len(history):
            cfg = history[index]
            target_mode = cfg.get("mode", "local")
            if self.current_mode != target_mode:
                self._show_app(target_mode)
            self.form_view.set_form_data(cfg)
            self.form_view.set_status(f"Loaded history: {target_mode.capitalize()}")

    def _open_output_dir(self, out_dir):
        if os.path.isdir(out_dir):
            if sys.platform == "win32": os.startfile(out_dir)
            elif sys.platform == "darwin": subprocess.call(["open", out_dir])
            else: subprocess.call(["xdg-open", out_dir])

    def _stop_generation(self):
        self._cancel_event.set()
        self.form_view.append_log("\n[!] Stopping... Please wait for the current operation to abort.")
        self.form_view.set_generating_state(False, stopping=True)
        self.form_view.set_status("Stopping generation…", good=False)

    def _start_generation(self):
        data = self.form_view.get_form_data()
        out_dir = data["output_dir"].strip()
        if not out_dir or not os.path.isdir(out_dir):
            return QMessageBox.critical(self, "Error", i18n.tr("err_out_dir"))
            
        src1 = data["src1"].strip()
        mode = self.current_mode
        if mode == 'local' and (not src1 or not os.path.isdir(src1)):
            return QMessageBox.critical(self, "Error", i18n.tr("err_in_dir"))
        elif mode == 'remote' and not src1:
            return QMessageBox.critical(self, "Error", i18n.tr("err_repo"))
        elif mode == 'pr' and not src1:
            return QMessageBox.critical(self, "Error", i18n.tr("err_pr"))

        current_config = data.copy()
        current_config.update({
            "mode": mode,
            "input_dir": src1 if mode == 'local' else "",
            "repo_url": src1 if mode == 'remote' else "",
            "pr_url": src1 if mode == 'pr' else "",
            "pat": data["src2"]
        })

        history_config = current_config.copy()
        history_config["pat"] = ""
        self.config_manager.save_config(history_config)
        self._update_history_combo()

        self.form_view.set_generating_state(True)
        self.form_view.set_status("Generating…", good=True)
        self._cancel_event.clear()

        self.thread = QThread()
        self.worker = GeneratorWorker(current_config, self._cancel_event)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.log_signal.connect(self.form_view.append_log)
        self.worker.progress_signal.connect(self.form_view.update_progress)
        self.worker.complete_signal.connect(self._on_generation_complete)
        self.worker.complete_signal.connect(self.thread.quit)
        self.worker.complete_signal.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()

    def _on_generation_complete(self, success, payload):
        self.form_view.set_generating_state(False)
        if success:
            self.form_view.set_status("Done.", good=True)
            if payload and payload.get("copy_clipboard") and payload.get("clipboard_text"):
                try:
                    cb = QGuiApplication.clipboard()
                    cb.setText(payload["clipboard_text"])
                    QMessageBox.information(self, "Success", "Context generated successfully and copied to clipboard!")
                except Exception as e:
                    QMessageBox.warning(self, "Clipboard Error", f"Generation succeeded, but copying failed: {e}")
            else:
                QMessageBox.information(self, "Success", "Context generated successfully!")
        else:
            self.form_view.set_status("Stopped or failed.", good=False)
            if payload and isinstance(payload, dict) and payload.get("cancelled"):
                self.form_view.append_log("\n[!] Generation cancelled.")
            else:
                err = payload.get("error", "") if isinstance(payload, dict) else ""
                if err: QMessageBox.warning(self, "Generation Failed", err)
                else: QMessageBox.warning(self, "Generation Failed", "The generation process did not complete successfully.")

    def closeEvent(self, event):
        try:
            self._cancel_event.set()
            if self.thread and self.thread.isRunning():
                self.thread.quit()
                self.thread.wait(1500)
        except Exception:
            pass
        super().closeEvent(event)