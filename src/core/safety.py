# Safety checker to prevent running dangerous commands.
# Example: prevent commands like "rm -rf /" or "shutdown".

class RiskChecker:
    def is_risky(self, command: str) -> bool:
        """
        Check if a command is risky.
        TODO: Implement proper rules (blacklist certain commands).
        """
        return False  # Placeholder for now
