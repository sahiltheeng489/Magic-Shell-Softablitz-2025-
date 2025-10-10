import json
import os

HISTORY_FILE = "history.json"
history_list = []

def load_history():
    global history_list
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history_list = json.load(f)
            except json.JSONDecodeError:
                history_list = []
    else:
        history_list = []

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_list, f, indent=2)

def add_to_history(command):
    if command and (len(history_list) == 0 or history_list[-1] != command):
        history_list.append(command)
        save_history()

def get_history_output():
    return "\n".join(f"{i+1}: {cmd}" for i, cmd in enumerate(history_list))
