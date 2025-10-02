import platform

class PhraseMapper:
    def __init__(self):
        self.is_windows = platform.system().lower() == 'windows'
        self.phrase_map_windows = {
            "list files": "dir",
            "current directory": "cd",
            "make directory": "mkdir",
            "remove directory": "rmdir",
        }
        self.phrase_map_unix = {
            "list files": "ls",
            "current directory": "pwd",
            "make directory": "mkdir",
            "remove directory": "rmdir",
        }

    def map_phrase(self, phrase):
        phrase = phrase.lower().strip()
        if self.is_windows:
            return self.phrase_map_windows.get(phrase, phrase)
        else:
            return self.phrase_map_unix.get(phrase, phrase)
