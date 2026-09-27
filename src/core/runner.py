import subprocess
import platform
import os
from pathlib import Path
import signal
from src.history_manager import load_history, add_to_history, get_history_output

class CommandRunner:
    def __init__(self):
        self.is_windows = platform.system().lower() == 'windows'
        self.cwd = os.getcwd()
        self.process = None

    def _translate(self, command: str) -> str:
        c = command.strip()
        if self.is_windows:
            if c == 'ls':
                return 'dir'
            if c == 'pwd':
                return 'cd'
        return c

    def _handle_cd(self, command: str) -> str | None:
        parts = command.strip().split(maxsplit=1)
        if not parts or parts[0].lower() != 'cd':
            return None
        if len(parts) == 1:
            return self.cwd + '\n'
        target = parts[1].strip().strip('"').strip("'")
        if target == '-':
            return self.cwd + '\n'
        new_path = Path(target)
        if not new_path.is_absolute():
            new_path = Path(self.cwd) / new_path
        try:
            new_path = new_path.resolve(strict=True)
            if not new_path.is_dir():
                return f"Error: The directory does not exist: {target}\n"
            os.chdir(new_path)
            self.cwd = str(new_path)
            return ""
        except Exception as e:
            return f"Error changing directory: {e}\n"

    def run(self, command: str) -> str:
        command = self._translate(command)
        cd_result = self._handle_cd(command)
        if cd_result is not None:
            return cd_result
        try:
            self.process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, cwd=self.cwd
            )
            out, err = self.process.communicate()
            self.process = None
            return out if out else err
        except Exception as e:
            self.process = None
            return f"Error: {e}\n"

    def cancel(self):
        if self.process:
            if self.is_windows:
                self.process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                self.process.terminate()
            self.process = None

    def get_cwd(self) -> str:
        return self.cwd

    def run_command(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return
        # Show command history if user types 'history'
        if cmd == "history":
            output = get_history_output()
            print(output)  # Or update GUI output
            return
        # Save command to history
        add_to_history(cmd)

        # Run command normally
        return self.run(cmd)
