import os
import re
import json

# Optional filler prefix: "can you", "please", "i want to", "i need to", "could you"
_FILLER = r'(?:(?:can\s+you|please|i\s+(?:want|need|would\s+like)\s+to|could\s+you|just)\s+)?'

class PhraseMapper:
    def __init__(self):
        # Load all aliases for intent matching
        with open("aliases.json", "r", encoding="utf-8") as f:
            self.alias_dict = json.load(f)
        self.command_templates = list(self.alias_dict.keys())

        self.patterns = [
            # -- WHERE AM I / PWD --
            (re.compile(
                r'(?:where\s+am\s+i'
                r'|what(?:\'s|\s+is)\s+(?:the\s+)?(?:current|present|my)\s*(?:directory|folder|dir|path)'
                r'|what\s+is\s+my\s+(?:current\s+)?(?:directory|folder|dir|path)'
                r'|print\s+working\s+dir(?:ectory)?'
                r'|show\s+(?:current|present)\s*(?:dir(?:ectory)?|folder|path))',
                re.I), self._pwd_cmd),

            # -- SHOW FILE CONTENTS (must be before list-files to avoid greedy match) --
            (re.compile(
                _FILLER +
                r'(?:show|display|print|view|cat|read|open)\s+(?:the\s+)?contents?\s+of\s+(\S+)',
                re.I), self._cat_cmd),
            (re.compile(
                _FILLER +
                r'(?:read|open|view|cat)\s+(?:(?:the\s+)?file\s+)?(\S+)',
                re.I), self._cat_cmd),
            (re.compile(
                _FILLER +
                r'display\s+(\S+\.\w+)',
                re.I), self._cat_cmd),

            # -- LIST FILES --
            (re.compile(
                _FILLER +
                r'(?:list|show|display|what(?:\'s|\s+is)\s+in|see\s+what(?:\'s|\s+is)?\s+(?:in|here)|show\s+me)\s*'
                r'(?:(?:all\s+)?(?:the\s+)?(?:files?|folders?|directories|contents?|items?|things?)\s*(?:in|here|inside)?.*)?$',
                re.I), self._ls_cmd),

            # -- GO UP --
            (re.compile(
                r'(?:go\s+up|up\s+one\s+(?:level|dir(?:ectory)?)|parent\s+(?:dir(?:ectory)?|folder)|back\s+(?:up|one)|'
                r'navigate\s+(?:up|back)|one\s+(?:level|step)\s+up|cd\s+\.\.)',
                re.I), "cd .."),

            # -- NAVIGATE TO PATH --
            (re.compile(
                _FILLER +
                r'(?:change\s+(?:dir(?:ectory)?|folder)\s+to|go\s+(?:to|into)|navigate\s+to|'
                r'cd\s+to|switch\s+to|open\s+folder|move\s+(?:in)?to)\s+(\S+)',
                re.I), self._cd_to_path),

            # -- CREATE FOLDER --
            (re.compile(
                _FILLER +
                r'(?:make|create|add|new)\s+(?:a\s+)?(?:new\s+)?(?:folder|directory|dir)(?:\s+(?:called|named|with\s+name))?\s*(.*)',
                re.I), self._mkdir_cmd),

            # -- CREATE FILE (touch) --
            (re.compile(
                _FILLER +
                r'(?:create|make|add|new|touch)\s+(?:a\s+)?(?:new\s+)?file(?:\s+(?:called|named|with\s+name))?\s+(\S+)',
                re.I), self._touch_cmd),

            # -- DELETE FILE (match filenames with extension) --
            (re.compile(
                _FILLER +
                r'(?:delete|remove|erase|get\s+rid\s+of|del|rm)\s+(?:(?:the\s+)?file\s+)?(\S+\.\w+)',
                re.I), self._rm_file_cmd),

            # -- DELETE FOLDER --
            (re.compile(
                _FILLER +
                r'(?:delete|remove|erase|get\s+rid\s+of|rmdir)\s+(?:(?:the\s+)?(?:folder|directory|dir)\s+)?(\S+)',
                re.I), self._rm_folder_cmd),

            # -- COPY FILE --
            (re.compile(
                _FILLER +
                r'(?:copy|duplicate|cp)\s+(?:(?:the\s+)?file\s+)?([^ ]+)\s+(?:to|into|as)\s+(.+)',
                re.I), self._copy_cmd),

            # -- MOVE / RENAME FILE --
            (re.compile(
                _FILLER +
                r'(?:move|mv|rename)\s+(?:(?:the\s+)?file\s+)?([^ ]+)\s+(?:to|as|into)\s+(.+)',
                re.I), self._move_cmd),

            # -- CLEAR SCREEN --
            (re.compile(
                r'(?:clear\s+(?:the\s+)?(?:screen|terminal|console)|clr)',
                re.I), "cls" if os.name == "nt" else "clear"),
        ]

    # -- Handlers --

    def _mkdir_cmd(self, match):
        arg = match.group(1).strip() if match.lastindex and match.group(1) else ""
        return f"mkdir {arg}" if arg else "mkdir"

    def _touch_cmd(self, match):
        filename = match.group(1).strip() if match.lastindex and match.group(1) else ""
        return f"touch {filename}" if filename else "touch"

    def _cat_cmd(self, match):
        filename = match.group(1).strip() if match.lastindex and match.group(1) else ""
        return f"cat {filename}" if filename else "cat"

    def _rm_file_cmd(self, match):
        filename = match.group(1).strip() if match.lastindex and match.group(1) else ""
        if not filename:
            return "del" if os.name == "nt" else "rm"
        return f"del {filename}" if os.name == "nt" else f"rm {filename}"

    def _rm_folder_cmd(self, match):
        foldername = match.group(1).strip() if match.lastindex and match.group(1) else ""
        if not foldername:
            return "rmdir /s /q" if os.name == "nt" else "rm -rf"
        return f"rmdir /s /q {foldername}" if os.name == "nt" else f"rm -rf {foldername}"

    def _ls_cmd(self, match):
        return "dir" if os.name == "nt" else "ls"

    def _pwd_cmd(self, match):
        return "cd" if os.name == "nt" else "pwd"

    def _cd_to_path(self, match):
        path = match.group(1).strip() if match.lastindex and match.group(1) else ""
        return f"cd {path}" if path else "cd"

    def _copy_cmd(self, match):
        src = match.group(1).strip()
        dst = match.group(2).strip()
        return f"copy {src} {dst}" if os.name == "nt" else f"cp {src} {dst}"

    def _move_cmd(self, match):
        src = match.group(1).strip()
        dst = match.group(2).strip()
        return f"move {src} {dst}" if os.name == "nt" else f"mv {src} {dst}"

    def map_phrase(self, user_input):
        for pattern, handler in self.patterns:
            match = pattern.match(user_input)
            if match:
                if callable(handler):
                    return handler(match)
                else:
                    return handler
        return user_input  # fallback: pass through as-is
