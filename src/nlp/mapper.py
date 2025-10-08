import os
import re
import json

class PhraseMapper:
    def __init__(self):
        # Load all aliases for intent matching
        with open("aliases.json", "r", encoding="utf-8") as f:
            self.alias_dict = json.load(f)
        self.command_templates = list(self.alias_dict.keys())

        self.patterns = [
            # Make/Create directory/folder/dir
            (re.compile(r'.*\b(make|create)\b.*\b(folder|directory|dir)\b\s*(.*)', re.I), self._mkdir_cmd),
            # Remove/Delete file
            (re.compile(r'.*\b(remove|delete|del)\b.*\b(file)\b\s*(.*)', re.I), self._rm_file_cmd),
            # Remove/Delete folder/directory/dir
            (re.compile(r'.*\b(remove|delete|del)\b.*\b(folder|directory|dir)\b\s*(.*)', re.I), self._rm_folder_cmd),
            # Show current directory
            (re.compile(r'.*\b(show|display|list)\b.*\b(current|present)\b.*\b(directory|folder|dir)\b.*', re.I), self._pwd_cmd),
            # List files/folders
            (re.compile(r'.*\b(list|show|display)\b.*\b(files|folders|directories|dir)\b.*', re.I), self._ls_cmd),
            # Go up one level

            (re.compile(r'.*\b(go up|up one level|parent directory|cd ..)\b.*', re.I), "cd .."),
            # Change directory to a specific path
            (re.compile(r'.*\b(change directory to|cd to|switch to)\b\s*(\S+)', re.I), self._cd_to_path),
            # Copy file
            (re.compile(r'.*\b(copy)\b.*\b(file)\b\s*([^ ]+)\s+to\s+(.+)', re.I), self._copy_cmd),
            # Move file
            (re.compile(r'.*\b(move)\b.*\b(file)\b\s*([^ ]+)\s+to\s+(.+)', re.I), self._move_cmd),
        ]

    def _mkdir_cmd(self, match):
        arg = match.group(3).strip()
        return f"mkdir {arg}" if arg else "mkdir"

    def _rm_file_cmd(self, match):
        filename = match.group(3).strip()
        if not filename:
            return "del" if os.name == "nt" else "rm"
        return f"del {filename}" if os.name == "nt" else f"rm {filename}"

    def _rm_folder_cmd(self, match):
        foldername = match.group(3).strip()
        if not foldername:
            return "rmdir /s /q" if os.name == "nt" else "rm -rf"
        return f"rmdir /s /q {foldername}" if os.name == "nt" else f"rm -rf {foldername}"

    def _ls_cmd(self, match):
        return "dir" if os.name == "nt" else "ls"

    def _pwd_cmd(self, match):
        return "cd" if os.name == "nt" else "pwd"

    def _cd_to_path(self, match):
        path = match.group(2).strip()
        return f"cd {path}"

    def _copy_cmd(self, match):
        src = match.group(3).strip()
        dst = match.group(4).strip()
        if os.name == "nt":
            return f"copy {src} {dst}"
        else:
            return f"cp {src} {dst}"

    def _move_cmd(self, match):
        src = match.group(3).strip()
        dst = match.group(4).strip()
        if os.name == "nt":
            return f"move {src} {dst}"
        else:
            return f"mv {src} {dst}"

    def map_phrase(self, user_input):
        for pattern, handler in self.patterns:
            match = pattern.match(user_input)
            if match:
                if callable(handler):
                    return handler(match)
                else:
                    return handler
        return user_input  # fallback if no pattern matches
