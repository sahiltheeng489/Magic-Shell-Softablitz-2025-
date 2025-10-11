from src.nlp.mapper import PhraseMapper
from src.nlp.semantic_matcher import SemanticMatcher
from src.core.runner import CommandRunner  # Import the correct runner class
from src.core.safety import Safety
from src.history_manager import add_to_history  # Import for history management
from src.core.commands import rename_item
from src.core.commands import clear_terminal

SIMILARITY_THRESHOLD = 0.6
WARN_THRESHOLD = 0.4

class Controller:
    def __init__(self, on_output=None, on_cwd_changed=None):
        self.mapper = PhraseMapper()
        self.runner = CommandRunner()
        self.safety = Safety()
        self.on_output = on_output
        self.on_cwd_changed = on_cwd_changed

        # Initialize the semantic matcher with the path to aliases.json
        self.matcher = SemanticMatcher("aliases.json")

    def handle_input(self, user_text):
        user_text_stripped = user_text.strip().lower()
        # Special-case skip warning for 'pwd'
        if user_text_stripped == "pwd":
            resolved_command = "pwd"
            output = self.runner.run(resolved_command)
            if self.on_output:
                self.on_output(user_text, output)
            return output

        # Add to command history
        add_to_history(user_text)
        args = user_text.strip().split()
    
        if len(args) > 0 and args[0] == "rename":
            if len(args) != 3:
                return "Usage: rename <old_name> <new_name>"
            return rename_item(args[1], args[2])
        if len(args) == 1 and args[0].lower() == "clear":
            return clear_terminal()

        template, command, score = self.matcher.match(user_text)

        if score >= SIMILARITY_THRESHOLD:
            resolved_command = command
        elif WARN_THRESHOLD <= score < SIMILARITY_THRESHOLD:
            resolved_command = self.mapper.map_phrase(user_text)
        else:
            resolved_command = self.mapper.map_phrase(user_text)

        output = self.runner.run(resolved_command)

        if self.on_output:
            self.on_output(user_text, output)

        return output

    def get_cwd(self) -> str:
        # Expose current working directory from runner to callers (e.g., GUI)
        return self.runner.get_cwd()
