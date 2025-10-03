import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
import tkinter.font as tkFont
from core.controller import Controller

def on_controller_output(user_cmd, output):
    insert_output(f"> {user_cmd}\n{output}\n")

def on_cwd_changed(new_cwd):
    cwd_label.config(text=f"cwd: {new_cwd}")

controller = Controller(on_output=on_controller_output, on_cwd_changed=on_cwd_changed)

# History navigation
cmd_history = []
history_index = -1

def run_command():
    global history_index
    user_command = entry.get()
    if user_command.strip():
        cmd_history.append(user_command)
    history_index = len(cmd_history)
    insert_output(f"> {user_command}\n")
    entry.delete(0, tk.END)
    run_button.config(state='disabled')
    controller.handle_input_async(user_command)
    window.after(200, lambda: run_button.config(state='normal'))

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

def insert_output(text):
    output_area.config(state='normal')
    output_area.insert(tk.END, text)
    output_area.config(state='disabled')
    output_area.see(tk.END)

window = tk.Tk()
window.title("Magic Shell UI")

terminal_font = tkFont.Font(family="Consolas", size=10)

entry = tk.Entry(window, width=80, font=terminal_font)
entry.pack(pady=5)
entry.bind("<Up>", on_up)
entry.bind("<Down>", on_down)

run_button = tk.Button(window, text="Run", command=run_command)
run_button.pack(pady=5)

output_area = tk.Text(window, height=30, width=100,
                      bg="black", fg="lime",
                      insertbackground="white",
                      font=terminal_font,
                      state='disabled')
output_area.pack(pady=5)

scrollbar = tk.Scrollbar(window, command=output_area.yview)
output_area.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

cwd_label = tk.Label(window, text=f"cwd: {controller.get_cwd()}", anchor="w")
cwd_label.pack(fill="x")

window.mainloop()
