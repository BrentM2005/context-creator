import os
import json
from .constants import CONFIG_FILE

class ConfigManager:
    def __init__(self):
        self.history =[]
        self._load_config()

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.history = data
                    elif isinstance(data, dict):
                        self.history = [data]
            except Exception:
                pass

    def save_config(self, current_config):
        self.history = [cfg for cfg in self.history if cfg != current_config]
        self.history.insert(0, current_config)
        self.history = self.history[:15]  

        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception:
            pass

    def get_history(self):
        return self.history