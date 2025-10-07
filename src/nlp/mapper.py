import re

class PhraseMapper:
    def __init__(self):
        self.patterns = [
            (re.compile(r'.*\b(make|create)\b.*\b(folder|directory|dir)\b\s*(.*)', re.I), self._mkdir_cmd),
            (re.compile(r'.*\b(remove|delete|del)\b.*\b(file|folder|directory|dir)\b\s*(.*)', re.I), self._rm_cmd),
            (re.compile(r'.*\b(show|display|list)\b.*\b(current|present)\b.*\b(directory|folder|dir)\b.*', re.I), 'pwd'),
            (re.compile(r'.*\b(go up|up one level|parent directory|cd ..)\b.*', re.I), 'cd ..'),
            # (re.compile(r'.*\b(change directory to|cd to|switch to)\b\s*(\S+)', re.I), self._cd_to_path),
            # Add more natural language patterns here
        ]

    def _mkdir_cmd(self, match):
        arg = match.group(3).strip()
        return f"mkdir {arg}" if arg else "mkdir"

    def _rm_cmd(self, match):
        arg = match.group(3).strip()
        return f"rm {arg}" if arg else "rm"

    def _cd_to_path(self, match):
        path = match.group(2).strip()
        return f"cd {path}"

    def map_phrase(self, input_text: str) -> str:
        for pattern, cmd in self.patterns:
            match = pattern.match(input_text)
            if match:
                if callable(cmd):
                    return cmd(match)
                else:
                    return cmd
        return input_text  # fallback to input as-is
