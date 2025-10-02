import tkinter as tk
import tkinter.font as tkFont
from ..core.runner import CommandRunner

runner = CommandRunner()

def run_command():
    user_command = entry.get()
    output = runner.run(user_command)
    insert_output(f"> {user_command}\n{output}\n")
    entry.delete(0, tk.END)

def insert_output(text):
    output_area.config(state='normal')
    output_area.insert(tk.END, text)
    output_area.config(state='disabled')
    output_area.see(tk.END)  # scroll to end

window = tk.Tk()
window.title("Magic Shell UI")

terminal_font = tkFont.Font(family="Consolas", size=10)

entry = tk.Entry(window, width=80, font=terminal_font)
entry.pack(pady=5)

run_button = tk.Button(window, text="Run", command=run_command)
run_button.pack(pady=5)

output_area = tk.Text(window, height=20, width=80,
                      bg="black", fg="lime",
                      insertbackground="white",
                      font=terminal_font,
                      state='disabled')
output_area.pack(pady=5)

scrollbar = tk.Scrollbar(window, command=output_area.yview)
output_area.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

window.mainloop()
