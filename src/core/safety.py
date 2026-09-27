import re

class Safety:
    def __init__(self):
        # Simple deny patterns (expand as needed)
        self.deny_patterns = [
            r'rm\s+-rf\s+[/\\]?$',              # rm -rf /
            r'format\s+\w:',                    # Windows format
            r'del\s+/s\s+/q\s+.*\*',            # aggressive Windows delete
            r'rd\s+/s\s+/q\s+[/\\]?.*',         # recursive Windows remove dir
            r'shutdown(\s|$)',                  # shutdown command
        ]

        # Commands that require confirmation (soft risky)
        self.warn_patterns = [
            r'rm\s+-rf\s+.+',
            r'del\s+/s\s+.+',
            r'rd\s+/s\s+.+',
            r'move\s+.+',
            r'copy\s+.+',
        ]

    def is_blocked(self, cmd: str) -> bool:
        c = cmd.strip().lower()
        return any(re.search(p, c) for p in self.deny_patterns)

    def needs_warning(self, cmd: str) -> bool:
        c = cmd.strip().lower()
        if c == "pwd":
            return False
        return any(re.search(p, c) for p in self.warn_patterns)
