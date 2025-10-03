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
            if c == 'ls':
                return 'dir'
            if c == 'pwd':
                return 'cd'
        return c

    def _handle_cd(self, command: str) -> str | None:
        """
        If command is a 'cd ...', perform it in-process and return a message.
        Return None if it's not a cd command.
        """
        parts = command.strip().split(maxsplit=1)
        if not parts:
            return None
        if parts[0].lower() != 'cd':
            return None

        # cd with no args -> print cwd
        if len(parts) == 1:
            return str(self.cwd) + "\n"

        target = parts[1].strip().strip('"').strip("'")
        # Expand ~ and relative paths
        if target == '-':
            # No previous dir tracking yet; optional enhancement
            return str(self.cwd) + "\n"

        new_path = Path(target)
        if not new_path.is_absolute():
            new_path = Path(self.cwd) / new_path

        try:
            new_path = new_path.resolve(strict=True)
            if not new_path.is_dir():
                return f"The system cannot find the path specified: {target}\n"
            # Change process cwd for future commands
            os.chdir(new_path)
            self.cwd = str(new_path)
            return ""
        except Exception as e:
            return f"cd: {e}\n"

    def run(self, command: str) -> str:
        command = self._translate(command)

        # Intercept cd to change internal cwd
        cd_result = self._handle_cd(command)
        if cd_result is not None:
            return cd_result

        try:
            completed_process = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=False, cwd=self.cwd
            )
            # Prefer stdout; if empty, show stderr
            out = completed_process.stdout
            err = completed_process.stderr
            return out if out else err
        except Exception as e:
            return f"Error: {e}\n"

    def get_cwd(self) -> str:
        return self.cwd
