from core.runner import CommandRunner
from nlp.mapper import PhraseMapper

class Controller:
    def __init__(self):
        self.runner = CommandRunner()
        self.mapper = PhraseMapper()

    def handle_input(self, user_text):
        command = self.mapper.map_phrase(user_text)
        return self.runner.run(command)
