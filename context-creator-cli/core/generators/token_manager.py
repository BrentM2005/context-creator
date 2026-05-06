try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

class TokenManager:
    def __init__(self, config, log_cb=None):
        self.config = config
        self.tokenizer = None
        global HAS_TIKTOKEN
        if HAS_TIKTOKEN:
            try:
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
            except Exception as e:
                if log_cb:
                    log_cb(f"Warning: Failed to load tiktoken encoding: {e}")
                HAS_TIKTOKEN = False

    def count_tokens(self, text: str) -> int:
        if HAS_TIKTOKEN and self.tokenizer:
            try:
                return len(self.tokenizer.encode(text, disallowed_special=()))
            except Exception:
                pass
        return len(text) // 4

    def get_token_budget(self) -> int:
        b_str = self.config.get('token_budget', 'None')
        if '128k' in b_str: return 128000
        elif '200k' in b_str: return 200000
        elif '1M' in b_str: return 1000000
        elif b_str == 'Custom':
            try: return int(self.config.get('custom_budget', 0))
            except ValueError: return 0
        return 0