import json
import os

DEFAULT_ALIAS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'aliases.json'))

class AliasStore:
    def __init__(self, path: str = DEFAULT_ALIAS_FILE):
        self.path = path
        self.aliases = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.aliases = data
            except Exception:
                self.aliases = {}

    def resolve(self, text: str) -> str:
        key = text.strip()
        return self.aliases.get(key, text)
