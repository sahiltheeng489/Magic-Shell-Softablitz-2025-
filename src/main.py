# Entry point of the Magic Shell project
# Connects the Controller with the Tkinter UI and starts the app.

from ui.tk_view import TkView
from core.controller import AppController

def main():
    """
    Main entry function.
    - Creates the application controller (handles logic).
    - Passes it to the Tkinter view.
    - Starts the GUI loop.
    """
    controller = AppController()
    app = TkView(controller)
    app.run()

# Only run main() if this file is executed directly (not imported as a module).
if __name__ == "__main__":
    main()
