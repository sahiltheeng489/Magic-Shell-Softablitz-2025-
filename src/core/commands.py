# src/core/commands.py
import os

def rename_item(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return f"Renamed '{old_name}' to '{new_name}' successfully."
    except Exception as e:
        return f"Error renaming '{old_name}': {e}"
def clear_terminal():
    # Clear screen command for Windows or Unix-based
    os.system("cls" if os.name == "nt" else "clear")
    return "" 