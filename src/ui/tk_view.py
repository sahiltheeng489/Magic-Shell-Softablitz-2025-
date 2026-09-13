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

    # Help command
    if user_command.strip().lower() == "help":
        insert_output(
            "Magic Shell Help:\n"
            "- Standard shell and natural language commands supported\n"
            "- Use '/ai <question>' for AI assistance\n"
            "- Use 'exit' to leave GUI\n",
            tag="info")
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
