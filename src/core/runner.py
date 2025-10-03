import subprocess
import platform
import os
from pathlib import Path

class CommandRunner:
    def __init__(self):
        self.is_windows = platform.system().lower() == 'windows'
        self.cwd = os.getcwd()

    def _translate(self, command: str) -> str:
        c = command.strip()
        if self.is_windows:
            # Translate some Unix commands to Windows equivalents
            if c == 'ls':
                return 'dir'
            if c == 'pwd':
                return 'cd'
        else:
            # Unix system can accept these as-is
            pass
        return c

    def _handle_cd(self, command: str) -> str | None:
        parts = command.strip().split(maxsplit=1)
        if not parts:
            return None
        if parts[0].lower() != 'cd':
            return None
        # Change directory logic
        if len(parts) == 1:
            # Just 'cd' prints current dir
            return self.cwd + '\n'
        target = parts[1].strip().strip('"').strip("'")
        if target == '-':
            # Optional: add previous directory tracking
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
            completed_process = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=False, cwd=self.cwd
            )
            out = completed_process.stdout
            err = completed_process.stderr
            return out if out else err
        except Exception as e:
            return f"Error: {e}\n"

    def get_cwd(self) -> str:
        return self.cwd
