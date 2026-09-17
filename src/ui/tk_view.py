import sys
import os
import json
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox
from src.core.controller import Controller
from src.ai.ollama_client import ollama_chat  # Real Ollama AI client

def load_settings():
    settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json'))
    defaults = {
        "color_normal": "lime",
        "color_error": "red",
        "color_warning": "orange",
        "color_info": "cyan",
        "color_cancel": "yellow",
        "default_cwd": "",
        "font_family": "Consolas",
        "font_size": 10
    }
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            defaults.update(loaded)
    except Exception:
        pass
    return defaults

config = load_settings()

if config.get("default_cwd"):
    try:
        os.chdir(config["default_cwd"])
    except Exception:
        pass

def on_controller_output(user_cmd, output):
    if "Blocked by safety" in output or "Error:" in output or "not found" in output:
        tag = "error"
    elif "Warning:" in output:
        tag = "warning"
    elif "** Command cancelled" in output or "cancelled by user" in output:
        tag = "cancel"
    else:
        tag = "normal"
    insert_output(f"> {user_cmd}\n{output}\n", tag=tag)

def on_cwd_changed(new_cwd):
    cwd_label.config(text=f"cwd: {new_cwd}")

controller = Controller(on_output=on_controller_output, on_cwd_changed=on_cwd_changed)

cmd_history = []
history_index = -1

def run_command():
    global history_index
    user_command = entry.get()
    if user_command.strip():
        cmd_history.append(user_command)
    history_index = len(cmd_history)
    entry.delete(0, tk.END)
    run_button.config(state='disabled')

    # /ai prefix support - calls real Ollama server
    if user_command.strip().startswith("/ai"):
        prompt = user_command.strip()[3:].strip()
        if not prompt:
            insert_output("Usage: /ai <your question>\n", tag="info")
            run_button.config(state='normal')
            return
        insert_output(f"AI thinking...\n", tag="info")
        def ai_task():
            response = ollama_chat(prompt)
            window.after(0, lambda: insert_output(f"AI: {response}\n", tag="info"))
            window.after(0, lambda: run_button.config(state='normal'))
        import threading
        threading.Thread(target=ai_task, daemon=True).start()
        return

    # Help command — route through controller so GUI and CLI show the same output
    if user_command.strip().lower() == "help":
        help_text = controller._build_help()
        insert_output(help_text + "\n", tag="info")
        run_button.config(state='normal')
        return

    # Preview and confirm harmful commands
    mapped_cmd = controller.mapper.map_phrase(user_command)
    if controller.safety.needs_warning(mapped_cmd):
        confirm = messagebox.askyesno(
            "Warning: Risky Command",
            f"Risky command detected:\n\n{mapped_cmd}\n\nAre you sure you want to run it?")
        if not confirm:
            insert_output("Command cancelled by user.\n", tag="cancel")
            run_button.config(state='normal')
            return

    controller.handle_input_async(user_command)
    window.after(200, lambda: run_button.config(state='normal'))

def cancel_command():
    controller.cancel()
    insert_output("** Command cancelled by user **\n", tag="cancel")
    run_button.config(state='normal')

def clear_screen():
    output_area.config(state='normal')
    output_area.delete(1.0, tk.END)
    output_area.config(state='disabled')

def on_up(event):
    global history_index
    if cmd_history and history_index > 0:
        history_index -= 1
        entry.delete(0, tk.END)
        entry.insert(0, cmd_history[history_index])

def on_down(event):
    global history_index
    if cmd_history and history_index < len(cmd_history) - 1:
        history_index += 1
        entry.delete(0, tk.END)
        entry.insert(0, cmd_history[history_index])
    else:
        history_index = len(cmd_history)
        entry.delete(0, tk.END)

# --- Tab Autocomplete ---
_tab_matches = []
_tab_index = -1
_tab_prefix = ""

BUILTIN_COMMANDS = [
    "alias", "unalias", "alias list", "history", "help",
    "clear", "cls", "exit", "quit",
    "mkdir", "touch", "cat", "rename", "rm", "del",
    "rmdir", "cd", "dir", "pwd", "/ai",
]

def _get_completions(prefix):
    """Return all completions for the given prefix."""
    prefix_lower = prefix.lower()
    matches = []

    # 1. Alias names from aliases.json
    for name in sorted(controller.alias_store.list_all().keys()):
        if name.lower().startswith(prefix_lower):
            matches.append(name)

    # 2. Built-in commands
    for cmd in BUILTIN_COMMANDS:
        if cmd.lower().startswith(prefix_lower) and cmd not in matches:
            matches.append(cmd)

    # 3. Files and folders in current directory
    try:
        cwd = controller.get_cwd()
        # If prefix has a path component, complete inside that dir
        dir_part = os.path.dirname(prefix) if os.sep in prefix or "/" in prefix else ""
        base_part = os.path.basename(prefix) if prefix else prefix
        search_dir = os.path.join(cwd, dir_part) if dir_part else cwd
        for name in sorted(os.listdir(search_dir)):
            candidate = os.path.join(dir_part, name) if dir_part else name
            if candidate.lower().startswith(prefix_lower) and candidate not in matches:
                # Append trailing slash for directories
                if os.path.isdir(os.path.join(search_dir, name)):
                    candidate += os.sep
                matches.append(candidate)
    except Exception:
        pass

    return matches

def on_tab(event):
    global _tab_matches, _tab_index, _tab_prefix
    current = entry.get()

    # If this is a fresh Tab press (not cycling), build the completion list
    if not _tab_matches or current != (_tab_matches[_tab_index] if _tab_matches else ""):
        _tab_prefix = current
        _tab_matches = _get_completions(current)
        _tab_index = -1

    if not _tab_matches:
        return "break"  # Nothing to complete

    # Cycle forward
    _tab_index = (_tab_index + 1) % len(_tab_matches)
    entry.delete(0, tk.END)
    entry.insert(0, _tab_matches[_tab_index])

    # Show hint in output if multiple matches
    if len(_tab_matches) > 1:
        hint = "  ".join(_tab_matches)
        insert_output(f"[Tab] {hint}\n", tag="info")

    return "break"  # Prevent default Tab behaviour (focus change)

def on_shift_tab(event):
    global _tab_matches, _tab_index, _tab_prefix
    current = entry.get()

    if not _tab_matches or current != (_tab_matches[_tab_index] if _tab_matches else ""):
        _tab_prefix = current
        _tab_matches = _get_completions(current)
        _tab_index = len(_tab_matches)

    if not _tab_matches:
        return "break"

    # Cycle backward
    _tab_index = (_tab_index - 1) % len(_tab_matches)
    entry.delete(0, tk.END)
    entry.insert(0, _tab_matches[_tab_index])
    return "break"

def reset_tab_state(event=None):
    """Reset tab state whenever user types a printable character (not Tab/arrows)."""
    global _tab_matches, _tab_index, _tab_prefix
    if event and event.keysym in ("Tab", "ISO_Left_Tab", "Up", "Down", "Shift_L", "Shift_R"):
        return
    _tab_matches = []
    _tab_index = -1
    _tab_prefix = ""

def insert_output(text, tag="normal"):
    output_area.config(state='normal')
    output_area.insert(tk.END, text, tag)
    output_area.config(state='disabled')
    output_area.see(tk.END)

window = tk.Tk()
window.title("Magic Shell UI")

terminal_font = tkFont.Font(family=config["font_family"], size=config["font_size"])

entry = tk.Entry(window, width=80, font=terminal_font)
entry.pack(pady=5)
entry.bind("<Up>", on_up)
entry.bind("<Down>", on_down)
entry.bind("<Tab>", on_tab)
entry.bind("<Shift-Tab>", on_shift_tab)
entry.bind("<Key>", reset_tab_state)
entry.bind("<Return>", lambda e: run_command())

run_button = tk.Button(window, text="Run", command=run_command)
run_button.pack(pady=5)

cancel_button = tk.Button(window, text="Cancel", command=cancel_command)
cancel_button.pack(pady=2)

clear_button = tk.Button(window, text="Clear Screen", command=clear_screen)
clear_button.pack(pady=2)

output_area = tk.Text(window, height=30, width=100,
                      bg="black", fg=config["color_normal"],
                      insertbackground="white",
                      font=terminal_font,
                      state='disabled')
output_area.pack(pady=5)

output_area.tag_config("normal", foreground=config["color_normal"])
output_area.tag_config("error", foreground=config["color_error"])
output_area.tag_config("warning", foreground=config["color_warning"])
output_area.tag_config("info", foreground=config["color_info"])
output_area.tag_config("cancel", foreground=config["color_cancel"])

scrollbar = tk.Scrollbar(window, command=output_area.yview)
output_area.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

cwd_label = tk.Label(window, text=f"cwd: {controller.get_cwd()}", anchor="w")
cwd_label.pack(fill="x")

window.mainloop()
