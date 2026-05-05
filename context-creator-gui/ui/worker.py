from PySide6.QtCore import QObject, Signal
from core.generator import ContextGenerator

class GeneratorWorker(QObject):
    progress_signal = Signal(float)
    log_signal = Signal(str)
    complete_signal = Signal(bool, dict)

    def __init__(self, config, cancel_event):
        super().__init__()
        self.config = config
        self.cancel_event = cancel_event

    def run(self):
        generator = ContextGenerator(
            config=self.config,
            cancel_event=self.cancel_event,
            log_cb=self.log_signal.emit,
            progress_cb=self.progress_signal.emit,
            complete_cb=self.complete_signal.emit
        )
        generator.run()