import tkinter as tk

def run_command():
    # Get text from the input box
    user_input = entry.get()
    # Print it to the output area
    output_area.insert(tk.END, user_input + '\n')
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
output_area = tk.Text(window, height=10, width=50)
output_area.pack(pady=5)

# Start the app
window.mainloop()
