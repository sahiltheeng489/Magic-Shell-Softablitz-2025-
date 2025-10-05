from src.nlp.mapper import PhraseMapper
from src.nlp.semantic_matcher import SemanticMatcher
from src.core.runner import Runner

class Controller:
    def __init__(self, on_output=None, on_cwd_changed=None):
        self.mapper = PhraseMapper()
        self.runner = Runner()
        self.on_output = on_output
        self.on_cwd_changed = on_cwd_changed

        # Initialize the semantic matcher with the path to aliases.json
        self.matcher = SemanticMatcher("aliases.json")

    def handle_input(self, user_text):
        # Use semantic matcher to get best alias and command
        template, command, score = self.matcher.match(user_text)

        # Threshold for confidence
        if score > 0.6:
            resolved_command = command
        else:
            # Fallback to regex phrase mapping if confidence is low
            resolved_command = self.mapper.map_phrase(user_text)

        # Run the resolved command using runner
        output = self.runner.run_command(resolved_command)

        # Notify listeners
        if self.on_output:
            self.on_output(user_text, output)

        # Optionally notify on cwd change, omitted for simplicity
        # if self.on_cwd_changed:
        #     new_cwd = self.runner.get_cwd()
        #     self.on_cwd_changed(new_cwd)

        return output

    # Other Controller methods unchanged...
