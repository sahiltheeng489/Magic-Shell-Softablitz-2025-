import sys
from src.core.controller import Controller

def main():
    controller = Controller()
    print("Magic Shell CLI (Type 'exit' or 'quit' to exit)")
    while True:
        cwd = controller.get_cwd()
        try:
            user_input = input(f"{cwd}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Magic Shell CLI.")
            break

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Handle command asynchronously if desired, or synchronous for simplicity
        output = controller.handle_input(user_input)
        print(output)

if __name__ == "__main__":
    main()
