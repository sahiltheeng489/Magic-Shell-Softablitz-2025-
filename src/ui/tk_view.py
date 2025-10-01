# Handles the user interface using Tkinter.
# Responsible for displaying input/output and interacting with the controller.

import tkinter as tk
from tkinter import scrolledtext

class TkView:
    def __init__(self, controller):
        """
        Initialize the Tkinter window and UI components.
        """
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Python Magic Shell")

        # Input text field where user types commands or phrases
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=10)

        # Button that triggers command execution
        self.run_button = tk.Button(self.root, text="Run", command=self.on_run)
        self.run_button.pack(pady=5)

        # Scrollable text area to display output from executed commands
        self.output = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.output.pack(pady=10)

    def on_run(self):
        """
        Event handler for the "Run" button.
        - Reads user input.
        - Sends it to the controller.
        - Displays the response in the output box.
        """
        user_input = self.entry.get()
        response = self.controller.handle_input(user_input)
        self.show_output(response)

    def show_output(self, text):
        """
        Append new text to the output area and auto-scroll.
        """
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def run(self):
        """
        Start the Tkinter main loop (keeps the window running).
        """
        self.root.mainloop()
