Step 0: Mindset & Tools
- Install Python 3.10+
- Install git + GitHub account
- Use VS Code (recommended)
- Create folder: magic-shell/

Step 1: Skeleton Setup
Goal: Empty project but with correct folders and files.
1. Inside magic-shell/, create folders:
 src/ui, src/core, src/nlp, src/store, tests
2. Inside each folder, make empty .py files:
 - src/app.py
 - src/ui/tk_view.py
 - src/core/controller.py
 - src/core/runner.py
 - src/core/safety.py
 - src/nlp/mapper.py
 - src/store/history.py
 - src/store/alias.py

Step 2: Build a Dumb UI
Goal: A small window opens with text box + button.
- In src/ui/tk_view.py, write Tkinter code:
 - Entry (input)
 - Button ("Run")
 - Text area (output)
- Wire the button to print input text.
Step 3: Add Command Execution
Goal: Type a system command → run it → show output.
- In src/core/runner.py, write CommandRunner using subprocess.run(...)
- Connect: UI → Controller → Runner → UI

Step 4: Add Controller
Goal: Central brain that takes input and decides what to do.
- In src/core/controller.py, make handle_input(user_text)
- First just call Runner directly
- Later add NLP + Safety

Step 5: Phrase Mapper (NLP-lite)
Goal: Natural phrases → commands.
- In src/nlp/mapper.py, create a dictionary:
 {"list files": "ls -la", "current path": "pwd"}
- Add toggle for NL mode ON/OFF

Step 6: Safety Net
Goal: Prevent disasters like rm -rf.
- In src/core/safety.py, make RiskChecker
- If risky → show confirm popup in UI

Step 7: History & Aliases
Goal: Remember what you did and create shortcuts.
- src/store/history.py → log commands to JSON
- src/store/alias.py → alias support

Step 8: Polishing
- Non-blocking execution (threads)
- Output formatting (headers, colors)
- Config file (settings.json)
- Add unit tests (pytest)
- README with usage steps

Step 9: Demo Flow
- Natural phrase input → mapped command
- Risky command → confirm dialog
- Show history & aliases
- Done ✅

Overall Order of Work
1. Make folder structure + empty files
2. Build GUI (Tkinter skeleton)
3. Add Runner (execute real commands)
4. Add Controller (connect UI + Runner)
5. Add PhraseMapper (NL → command)
6. Add SafetyChecker (block risky commands)
7. Add History + Aliases (JSON store)
8. Add polish (threads, formatting, settings)
9. Prepare demo script + screenshots
