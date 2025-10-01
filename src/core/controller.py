# Acts as the "brain" of the application.
# Receives input from the UI, processes it, and returns results.

from core.runner import CommandRunner

class AppController:
    def __init__(self):
        """
        Initialize the controller and connect it to the CommandRunner.
        """
        self.runner = CommandRunner()

    def handle_input(self, user_text: str) -> str:
        """
        Handle user input received from the UI.
        For now:
        - If input is empty → return a warning.
        - Otherwise → send it to the CommandRunner for execution.
        """
        if not user_text.strip():
            return "⚠️ Please enter a command."
        
        return self.runner.run(user_text)
