# Placeholder for phrase-to-command mapping
class PhraseMapper:
    def __init__(self):
        self.dictionary = {
            "list files": "ls -la",
            "current path": "pwd",
        }

    def map(self, phrase: str) -> str:
        return self.dictionary.get(phrase.lower(), phrase)
