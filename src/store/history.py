import json
import os
from datetime import datetime

DEFAULT_HISTORY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'history.json'))

class HistoryStore:
    def __init__(self, path: str = DEFAULT_HISTORY_FILE):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add(self, command: str, status: str = "ok", output_len: int = 0):
        entry = {
            "ts": datetime.now().isoformat(timespec='seconds'),
            "cmd": command,
            "status": status,
            "output_len": output_len,
        }
        data = self._read_all()
        data.append(entry)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _read_all(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
