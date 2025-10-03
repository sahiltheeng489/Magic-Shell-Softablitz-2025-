import threading
from src.core.runner import CommandRunner
from src.core.safety import Safety
from src.nlp.mapper import PhraseMapper
from src.store.alias import AliasStore
from src.store.history import HistoryStore

class Controller:
    def __init__(self, on_output=None, on_cwd_changed=None):
        self.runner = CommandRunner()
        self.safety = Safety()
        self.mapper = PhraseMapper()
        self.aliases = AliasStore()
        self.history = HistoryStore()
        self.on_output = on_output
        self.on_cwd_changed = on_cwd_changed

    def handle_input(self, user_text: str) -> str:
        text = self.aliases.resolve(user_text)
        cmd = self.mapper.map_phrase(text)

        # Detect cd before safety to ensure path messages still pass through
        if cmd.strip().lower().startswith('cd'):
            result = self.runner.run(cmd)
            self.history.add(user_text, status="ok", output_len=len(result))
            if self.on_cwd_changed:
                self.on_cwd_changed(self.runner.get_cwd())
            return result

        if self.safety.is_blocked(cmd):
            msg = "Blocked by safety rules.\n"
            self.history.add(user_text, status="blocked", output_len=len(msg))
            return msg

        if self.safety.needs_warning(cmd):
            warning = f"Warning: risky command detected -> {cmd}\n"
            output = self.runner.run(cmd)
            final = warning + output
            self.history.add(user_text, status="warn", output_len=len(final))
            return final

        output = self.runner.run(cmd)
        self.history.add(user_text, status="ok", output_len=len(output))
        return output

    def handle_input_async(self, user_text: str):
        def task():
            result = self.handle_input(user_text)
            if self.on_output:
                self.on_output(user_text, result)
        t = threading.Thread(target=task, daemon=True)
        t.start()

    def get_cwd(self) -> str:
        return self.runner.get_cwd()
