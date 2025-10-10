from src.ai.ollama_client import ollama_chat
import sys
import signal
from src.history_manager import load_history, add_to_history, get_history_output

if sys.platform == "win32":
    try:
        import pyreadline as readline
    except ImportError:
        print("Warning: pyreadline not installed, command history will be unavailable.")
        readline = None
else:
    import readline

from src.core.controller import Controller

COLOR_RESET = "\033[0m"
COLOR_ERROR = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_INFO = "\033[96m"
COLOR_NORMAL = "\033[92m"
COLOR_CANCEL = "\033[93m"

SIMILARITY_THRESHOLD = 0.6
WARN_THRESHOLD = 0.4

def color_text(text, color_code):
    return f"{color_code}{text}{COLOR_RESET}"

def print_output(output):
    if "Error:" in output or "Blocked by safety" in output:
        print(color_text(output, COLOR_ERROR))
    elif "Warning:" in output:
        print(color_text(output, COLOR_WARNING))
    elif "cancelled by user" in output:
        print(color_text(output, COLOR_CANCEL))
    else:
        print(color_text(output, COLOR_NORMAL))

def signal_handler(sig, frame):
    print("\nCommand cancelled by user.")

def main():
    controller = Controller()
    print(color_text("Magic Shell CLI (Type 'help' for commands, 'exit' or 'quit' to exit)", COLOR_INFO))

    load_history()  # Load history from file at startup

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            user_input = input("> ").strip()
        except EOFError:
            print("\nExiting Magic Shell CLI.")
            break
        except KeyboardInterrupt:
            print("\nCommand cancelled by user.")
            continue

        if not user_input:
            continue

        # Show command history if requested
        if user_input.lower() == "history":
            output = get_history_output()
            print_output(output)
            continue

        # Add command to history if not 'history'
        add_to_history(user_input)

        # Handle AI prefix with Ollama
        if user_input.lower().startswith("/ai"):
            prompt = user_input[3:].strip()
            ai_response = ollama_chat(prompt)
            print(color_text(f"AI: {ai_response}", COLOR_INFO))
            continue

        # Handle help command
        if user_input.lower() == "help":
            print(color_text(
                "Magic Shell Help:\n"
                "- Standard shell and natural language commands supported\n"
                "- Use '/ai <question>' for AI assistance\n"
                "- Use 'exit' or 'quit' to leave\n",
                COLOR_INFO))
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Semantic match for confirmation warning
        template, command, score = controller.matcher.match(user_input)

        if WARN_THRESHOLD <= score < SIMILARITY_THRESHOLD:
            # Bypass warning prompt for 'pwd' command
            if user_input.strip().lower() == 'pwd':
                output = controller.handle_input(user_input)
                print_output(output)
                continue

            print(color_text(f"Warning: Low confidence match '{template}', score: {score:.2f}", COLOR_WARNING))
            confirm = input(color_text(f"Run mapped command '{command}' anyway? (y/N): ", COLOR_WARNING)).strip().lower()
            if confirm != 'y':
                print(color_text("Command cancelled by user.", COLOR_CANCEL))
                continue

        # Preview and ask confirmation for risky commands
        cmd_mapped = controller.mapper.map_phrase(user_input)
        if controller.safety.needs_warning(cmd_mapped):
            print(color_text("WARNING: Risky command detected!", COLOR_WARNING))
            print(color_text(f"Preview: {cmd_mapped}", COLOR_WARNING))
            confirm = input(color_text("Are you sure you want to run it? (y/N): ", COLOR_WARNING)).strip().lower()
            if confirm != "y":
                print(color_text("Command cancelled.", COLOR_CANCEL))
                continue

        # Run input via controller.handle_input (which calls semantic matcher internally)
        output = controller.handle_input(user_input)
        print_output(output)

if __name__ == "__main__":
    main()
