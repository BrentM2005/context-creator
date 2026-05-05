from .generators.pr_generator import PRGenerator
from .generators.codebase_generator import CodebaseGenerator

class ContextGenerator:
    def __init__(self, config, cancel_event, log_cb, progress_cb, complete_cb):
        self.config = config
        self.cancel_event = cancel_event
        self.log = log_cb
        self.progress = progress_cb
        self.complete = complete_cb

    def run(self):
        if self.config.get('mode') == 'pr':
            generator = PRGenerator(
                self.config, self.cancel_event, self.log, self.progress, self.complete
            )
        else:
            generator = CodebaseGenerator(
                self.config, self.cancel_event, self.log, self.progress, self.complete
            )
        
        generator.run()