import re
import os

IS_WINDOWS = os.name == "nt"

class PhraseMapper:
    def __init__(self):
        self.patterns = [
            # Make/Create directory/folder/dir
            (re.compile(r'.*\b(make|create)\b.*\b(folder|directory|dir)\b\s*(.*)', re.I), self._mkdir_cmd),
            # Remove/Delete file (file only)
            (re.compile(r'.*\b(remove|delete|del)\b.*\b(file)\b\s*(.*)', re.I), self._rm_file_cmd),
            # Remove/Delete folder/directory/dir (whole folders)
            (re.compile(r'.*\b(remove|delete|del)\b.*\b(folder|directory|dir)\b\s*(.*)', re.I), self._rm_folder_cmd),
            # Show current directory
            (re.compile(r'.*\b(show|display|list)\b.*\b(current|present)\b.*\b(directory|folder|dir)\b.*', re.I), self._pwd_cmd),
            # List files/folders
            (re.compile(r'.*\b(list|show|display)\b.*\b(files|folders|directories|dir)\b.*', re.I), self._ls_cmd),
            # Go up one level
            (re.compile(r'.*\b(go up|up one level|parent directory|cd ..)\b.*', re.I), 'cd ..'),
            # Change directory to a specific path
            (re.compile(r'.*\b(change directory to|cd to|switch to)\b\s*(\S+)', re.I), self._cd_to_path),
            # Copy file
            (re.compile(r'.*\b(copy)\b.*\b(file)\b\s*([^ ]+)\s+to\s+(.+)', re.I), self._copy_cmd),
            # Move file
            (re.compile(r'.*\b(move)\b.*\b(file)\b\s*([^ ]+)\s+to\s+(.+)', re.I), self._move_cmd),
            # Add more patterns as needed...
        ]

    def _mkdir_cmd(self, match):
        arg = match.group(3).strip()
        return f"mkdir {arg}" if arg else "mkdir"

    def _rm_file_cmd(self, match):
        filename = match.group(3).strip()
        if not filename:
            return "del" if IS_WINDOWS else "rm"
        return f"del {filename}" if IS_WINDOWS else f"rm {filename}"

    def _rm_folder_cmd(self, match):
        foldername = match.group(3).strip()
        if not foldername:
            return "rmdir /s /q" if IS_WINDOWS else "rm -rf"
        return f"rmdir /s /q {foldername}" if IS_WINDOWS else f"rm -rf {foldername}"

    def _ls_cmd(self, match):
        # For listing, use 'dir' on Windows, 'ls' elsewhere
        return "dir" if IS_WINDOWS else "ls"

    def _pwd_cmd(self, match):
        # For showing current directory, use 'cd' on Windows, 'pwd' elsewhere
        return "cd" if IS_WINDOWS else "pwd"

    def _copy_cmd(self, match):
        src = match.group(3).strip()
        dst = match.group(4).strip()
        return f"copy {src} {dst}" if IS_WINDOWS else f"cp {src} {dst}"

    def _move_cmd(self, match):
        src = match.group(3).strip()
        dst = match.group(4).strip()
    def _cd_to_path(self, match):
        path = match.group(2).strip()
        return f"cd {path}"
