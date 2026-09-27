"""
Entry point for Magic Shell GUI.
Run this file from the project root:
    python src/main.py
"""
import sys
import os

# Ensure the project root is on the path so imports like `src.core.controller` resolve
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Change working directory to project root so history.json / aliases.json resolve correctly
os.chdir(project_root)

# Now import and run the GUI module
import src.ui.tk_view  # noqa: F401  (tk_view runs mainloop at module level)
