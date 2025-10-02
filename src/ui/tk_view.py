import tkinter as tk
from ..core.runner import CommandRunner

# Create an instance of CommandRunner
runner = CommandRunner()

def run_command():
    # Get text from the input box
    user_input = entry.get()
    # Run the command using CommandRunner
    output = runner.run(user_input)
    # Display the output in the text area
    output_area.insert(tk.END, f"> {user_input}\n{output}\n")
    # Clear input box
    entry.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("Magic Shell UI")

# Input box
entry = tk.Entry(window, width=40)
entry.pack(pady=5)

# Run button
run_button = tk.Button(window, text="Run", command=run_command)
run_button.pack(pady=5)

# Output text area
output_area = tk.Text(window, height=15, width=60)
output_area.pack(pady=5)

# Start the app
window.mainloop()
