import re

class PhraseMapper:
    def __init__(self):
        self.patterns = [
            (re.compile(r'.*\b(make|create)\b.*\b(folder|directory|dir)\b.*', re.I), 'mkdir'),
            (re.compile(r'.*\b(remove|delete|del)\b.*\b(file|folder|directory|dir)\b.*', re.I), 'rm'),
            (re.compile(r'.*\b(show|display|list)\b.*\b(current|present)\b.*\b(directory|folder|dir)\b.*', re.I), 'pwd'),
            (re.compile(r'.*\b(go up|up one level|parent directory|cd ..)\b.*', re.I), 'cd ..'),
            (re.compile(r'.*\b(change directory to|cd to|switch to)\b\s*(\S+)', re.I), self._cd_to_path),
            # Add more natural language patterns here
        ]

    def _cd_to_path(self, match):
        # fetch path group, construct 'cd <path>' command
        path = match.group(2)
        return f"cd {path}"

    def map_phrase(self, input_text: str) -> str:
        for pattern, command in self.patterns:
            if isinstance(command, str):
                if pattern.match(input_text):
                    return command
            else:
                # callable pattern handler
                match = pattern.match(input_text)
                if match:
                    return command(match)
        # fallback: return input as-is
        return input_text
