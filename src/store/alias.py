# Placeholder for alias support
class AliasStore:
    def __init__(self):
        self.aliases = {}

    def add_alias(self, name: str, command: str):
        self.aliases[name] = command

    def resolve(self, name: str) -> str:
        return self.aliases.get(name, name)
