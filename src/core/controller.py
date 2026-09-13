from src.nlp.mapper import PhraseMapper
from src.nlp.semantic_matcher import SemanticMatcher
from src.core.runner import CommandRunner
from src.core.safety import Safety
from src.core.commands import rename_item, clear_terminal, show_file_content, touch_file, remove_file, remove_folder
from src.store.alias import AliasStore  # Bug 6 fix: wire AliasStore so it's actually used


SIMILARITY_THRESHOLD = 0.6
WARN_THRESHOLD = 0.4


class Controller:
    def __init__(self, on_output=None, on_cwd_changed=None):
        self.mapper = PhraseMapper()
        self.runner = CommandRunner()
        self.safety = Safety()
        self.on_output = on_output
        self.on_cwd_changed = on_cwd_changed
        self.alias_store = AliasStore()  # Bug 6 fix: instantiate and use AliasStore

        # Semantic matcher backed by aliases.json
        self.matcher = SemanticMatcher("aliases.json")

    # ------------------------------------------------------------------
    # Bug 3 fix: add cancel() so the GUI's cancel_command() doesn't crash
    # ------------------------------------------------------------------
    def cancel(self):
        """Proxy cancel signal to the underlying CommandRunner."""
        self.runner.cancel()

    def handle_input(self, user_text):
        user_text_stripped = user_text.strip()

        # Bug 5 fix: history is added by the UI layer — do NOT add it here again

        args = user_text_stripped.split()
        if len(args) == 0:
            return "No command entered."

        lower = user_text_stripped.lower()

        # Special-case: pwd never needs safety warning
        if lower == "pwd":
            output = self.runner.run("pwd")
            if self.on_output:
                self.on_output(user_text, output)
            return output

        # --- Built-in commands handled directly ---
        if args[0].lower() == "rename":
            if len(args) != 3:
                return "Usage: rename <old_name> <new_name>"
            result = rename_item(args[1], args[2])
            if self.on_output:
                self.on_output(user_text, result)
            return result

        if len(args) == 1 and lower == "clear":
            result = clear_terminal()
            if self.on_output:
                self.on_output(user_text, result)
            return result

        if len(args) == 2 and lower.startswith("cat "):
            result = show_file_content(args[1])
            if self.on_output:
                self.on_output(user_text, result)
            return result

        if len(args) == 2 and lower.startswith("touch "):
            result = touch_file(args[1])
            if self.on_output:
                self.on_output(user_text, result)
            return result

        if len(args) == 2:
            cmd = args[0].lower()
            target = args[1]

            if cmd in ["rm", "delete", "del", "removefile", "remove file"]:
                result = remove_file(target)
                if self.on_output:
                    self.on_output(user_text, result)
                return result

            if cmd in ["rmdir", "removedir", "remove directory", "removefolder", "remove folder"]:
                result = remove_folder(target)
                if self.on_output:
                    self.on_output(user_text, result)
                return result

        # --- Bug 6 fix: resolve user-defined aliases before NLP mapping ---
        resolved_by_alias = self.alias_store.resolve(user_text_stripped)
        if resolved_by_alias != user_text_stripped:
            # User has an exact alias for this input — use it directly
            resolved_command = resolved_by_alias
        else:
            # Fall through to semantic/regex NLP mapping
            template, command, score = self.matcher.match(user_text_stripped)
            if score >= SIMILARITY_THRESHOLD:
                resolved_command = command
            else:
                resolved_command = self.mapper.map_phrase(user_text_stripped)

        # --- Bug 7 fix: enforce hard-block on truly dangerous commands ---
        if self.safety.is_blocked(resolved_command):
            error_msg = f"Blocked by safety: '{resolved_command}' is a dangerous command and cannot be run."
            if self.on_output:
                self.on_output(user_text, error_msg)
            return error_msg

        # Save cwd before running so we can detect changes
        cwd_before = self.runner.get_cwd()

        output = self.runner.run(resolved_command)

        # Bug 4 fix: fire on_cwd_changed whenever the working directory changes
        cwd_after = self.runner.get_cwd()
        if cwd_after != cwd_before and self.on_cwd_changed:
            self.on_cwd_changed(cwd_after)

        if self.on_output:
            self.on_output(user_text, output)

        return output

    def get_cwd(self) -> str:
        return self.runner.get_cwd()
