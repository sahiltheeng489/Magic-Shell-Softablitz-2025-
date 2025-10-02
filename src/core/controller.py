from core.runner import CommandRunner

class Controller:
    def __init__(self):
        self.runner = CommandRunner()

    def handle_input(self, user_text):
        # For now, just run the command and return the output
        return self.runner.run(user_text)
