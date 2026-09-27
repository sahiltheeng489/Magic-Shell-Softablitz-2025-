# Magic Shell 🐚✨

> **Softablitz 2025 Hackathon Project**

A natural language-powered terminal shell for students and beginners — type what you want in plain English and Magic Shell figures out the command.

---

## 🚀 The Problem

Traditional terminals demand exact commands, flags, and syntax. For students and beginners this means:
- Steep learning curve just to do basic tasks
- Constant context-switching to browser searches
- Frustration when errors say nothing useful

## 💡 The Solution

Magic Shell lets you type in plain English:

| You type | Magic Shell runs |
|---|---|
| `show me the files` | `dir` |
| `create a new folder called src` | `mkdir src` |
| `where am i` | `cd` (shows current path) |
| `go up` | `cd ..` |
| `show the contents of readme.txt` | `cat readme.txt` |
| `/ai how do I copy a file?` | AI assistant answers |
| `alias gs=git status` | Creates `gs` shortcut |

---

## ✨ Features

- **Natural Language Commands** — type plain English, get the right shell command
- **AI Assistant** — `/ai <question>` powered by Ollama (tinyllama model, runs locally)
- **Runtime Alias System** — create, list, and remove custom shortcuts at runtime
- **Tab Autocomplete** — completes alias names, built-in commands, and file/folder names
- **Command History** — scroll with ↑/↓ arrows, view with `history`
- **Safety Layer** — dangerous commands (e.g. `rm -rf /`) are hard-blocked; risky ones require confirmation
- **Live CWD Label** — GUI always shows the current working directory
- **Rich `help` Command** — shows all supported NLP phrases, file commands, alias commands
- **Dual Interface** — both a Tkinter GUI (`src/main.py`) and a CLI (`cli_shell.py`)
- **Persistent Aliases** — aliases saved to `aliases.json`, survive app restarts
- **Customisable** — font, colors, and default working directory via `settings.json`

---

## 🏗️ Folder Structure

```
Magic-Shell-Softablitz-2025-/
│
├── src/                        # Main application source
│   ├── main.py                 # Entry point — launches the Tkinter GUI
│   ├── history_manager.py      # Utility: add/get command history
│   │
│   ├── ai/                     # AI integration
│   │   ├── ollama_client.py    # Calls local Ollama server (tinyllama)
│   │   └── langchain_llama.py  # LangChain integration (future)
│   │
│   ├── core/                   # Application brain
│   │   ├── controller.py       # Central controller — routes input to commands
│   │   ├── runner.py           # Executes shell commands via subprocess
│   │   ├── safety.py           # Hard-blocks and warnings for dangerous commands
│   │   └── commands.py         # Built-in commands (rename, touch, cat, rm, rmdir)
│   │
│   ├── nlp/                    # Natural language processing
│   │   ├── mapper.py           # Regex-based phrase → command mapper
│   │   └── semantic_matcher.py # Semantic similarity via sentence-transformers
│   │
│   ├── store/                  # Persistent storage
│   │   ├── alias.py            # AliasStore — load/save/resolve/add/remove aliases
│   │   └── history.py          # HistoryStore — session history
│   │
│   └── ui/
│       └── tk_view.py          # Tkinter GUI — input, output, buttons, tab-complete
│
├── cli_shell.py                # Standalone CLI shell (no GUI required)
├── aliases.json                # Persistent alias dictionary
├── history.json                # Saved command history
├── settings.json               # App configuration (colors, font, default CWD)
├── README.md
└── ROADMAP.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **GUI** | Tkinter (built-in) |
| **NLP — Regex** | Python `re` module |
| **NLP — Semantic** | `sentence-transformers` (all-MiniLM-L6-v2) |
| **AI Assistant** | Ollama (local LLM server) + tinyllama model |
| **Persistence** | JSON files (`aliases.json`, `history.json`) |
| **Shell Execution** | `subprocess` module |
| **Version Control** | Git / GitHub |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com/download) (for `/ai` command)

### Install Python dependencies

```bash
pip install sentence-transformers
```

### Clone the repo

```bash
git clone https://github.com/sahiltheeng489/Magic-Shell-Softablitz-2025-.git
cd Magic-Shell-Softablitz-2025-
```

### (One-time) Download the AI model

```bash
ollama pull tinyllama
```

### Run the GUI

```bash
python src/main.py
```

### Run the CLI

```bash
python cli_shell.py
```

---

## 🧪 Usage Examples

### Natural Language
```
list all files
create a new folder called myproject
go up
navigate to C:\Users
show the contents of settings.json
delete file old_notes.txt
can you remove the folder temp
copy file a.txt to b.txt
clear the screen
where am i
```

### Alias System
```
alias gs=git status     # create shortcut
gs                      # runs: git status
alias list              # show all aliases
alias gs                # look up what gs maps to
unalias gs              # remove alias
unalias clear screen    # multi-word alias names supported
```

### AI Assistant
```
/ai how do I list all files recursively?
/ai what does the cd command do?
/ai explain the difference between rmdir and del
```

### Help
```
help
```

---

## ⚙️ Configuration (`settings.json`)

```json
{
  "color_normal": "lime",
  "color_error": "red",
  "color_warning": "orange",
  "color_info": "cyan",
  "color_cancel": "yellow",
  "default_cwd": "",
  "font_family": "Consolas",
  "font_size": 10
}
```

Set `default_cwd` to a path (e.g. `"C:\\Projects"`) to open the shell in that folder automatically.

---

## 🔒 Safety System

| Level | Examples | Behaviour |
|---|---|---|
| 🔴 Hard Blocked | `rm -rf /`, `format c:`, `shutdown` | Rejected — cannot run at all |
| 🟡 Warning | `del /s`, `move`, risky deletions | Confirmation dialog before running |
| 🟢 Safe | `dir`, `mkdir`, `cd`, `echo` | Runs immediately |

---

## 🗺️ Keyboard Shortcuts (GUI)

| Key | Action |
|---|---|
| `Enter` | Run command |
| `↑` / `↓` | Scroll through command history |
| `Tab` | Autocomplete (cycles through aliases, commands, files) |
| `Shift+Tab` | Autocomplete — cycle backward |

---

## 👥 Team

Built for **Softablitz 2025** Hackathon.
