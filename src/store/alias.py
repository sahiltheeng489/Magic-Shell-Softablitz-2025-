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

    def _save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.aliases, f, indent=2)
        except Exception as e:
            print(f"[AliasStore] Failed to save: {e}")

    def resolve(self, text: str) -> str:
        """Return the command mapped to text if an alias exists, else return text unchanged."""
        key = text.strip()
        return self.aliases.get(key, text)

    def add(self, name: str, command: str):
        """Add or update an alias and persist it to disk."""
        self.aliases[name.strip()] = command.strip()
        self._save()

    def remove(self, name: str) -> bool:
        """Remove an alias by name. Returns True if removed, False if not found."""
        key = name.strip()
        if key in self.aliases:
            del self.aliases[key]
            self._save()
            return True
        return False

    def list_all(self) -> dict:
        """Return a copy of all current aliases."""
        return dict(self.aliases)
