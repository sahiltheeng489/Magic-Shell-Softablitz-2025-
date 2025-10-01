# Handles execution of system commands securely.
# Uses subprocess to run commands and capture their output.

import subprocess

class CommandRunner:
    def run(self, command: str) -> str:
        """
        Execute a shell command and return its output or errors.
        - command: The shell command string (e.g., 'ls', 'echo hello')
        """
        try:
            # Run the command in a subprocess
            result = subprocess.run(
                command, shell=True, text=True,
                capture_output=True, check=False
            )

            # If command produces standard output
            if result.stdout:
                return result.stdout.strip()

            # If command produces an error
            if result.stderr:
                return "❌ Error: " + result.stderr.strip()

            # If no output at all
            return "(No output)"
        except Exception as e:
            # Handle unexpected Python-level errors
            return f"⚠️ Exception: {e}"
