# Ollama CLI v3.0 Documentation

Ollama CLI is a professional-grade, multi-modal autonomous agent interface for local Ollama LLMs. It transforms a standard chat interface into a powerful system-wide tool capable of coding, web research, project management, and media generation.

## 🏛 Architecture

The project follows a modular, extensible architecture:

- **`src/ollama_cli/main.py`**: The central orchestrator. Manages the chat loop, REPL, and the iterative "Agentic" reasoning cycle.
- **`src/ollama_cli/core/`**: Foundation modules for API communication, configuration management, and persistent sessions.
- **`src/ollama_cli/tools/`**: The agent's "hands." Modular tool definitions for Filesystem, System, Code, Web, Media, and Memory.
- **`src/ollama_cli/integrations/`**: Third-party protocols including MCP, LSP, and ntfy.sh.
- **`src/ollama_cli/ui/`**: User interface components for rich formatting and interactive input.

---

## 🛠 Toolset

The agent has access to 20+ specialized tools. It decides when to use them based on your prompts.

### Filesystem
- `read_file(path)`: Reads content from a local file.
- `write_file(path, content)`: Creates or overwrites a file.
- `list_directory(path)`: Lists files in a folder.
- `grep_search(pattern, path)`: Advanced regex searching across files.
- `get_tree(path, depth)`: Visualizes the project structure.

### Code & Execution
- `run_python(code)`: Executes Python snippets locally and returns output.
- `replace_text(path, old, new)`: Performs surgical text replacements in files.
- `code_analyze_file(path)`: Structural analysis of source code (detects classes, functions, and issues).
- `run_linter(path)`: Runs pylint or eslint on a file.

### Web & Research
- `web_search(query)`: Searches the web via DuckDuckGo.
- `read_url(url)`: Fetches and extracts text from any webpage for deep analysis.

### Media (Visual & Audio)
- `generate_image(prompt)`: Queues a ComfyUI stable diffusion job with realtime progress tracking.
- `speak_text(text)`: Generates and plays ultra-realistic human speech using Kokoro or Piper TTS.
- `get_comfy_status(id)`: Checks the status of image generation jobs.

### Memory & Knowledge
- `remember_fact(fact)`: Stores project-specific context (e.g., "Main DB is PostgreSQL").
- `recall_facts()`: Lists all remembered project information.
- `kb_add/kb_search`: Manages a global knowledge base.

---

## ⚙️ Configuration

Settings are stored in `~/.ollama-cli-config.json`. You can view and update them via the CLI.

### Command: `/config`
Type `/config` without arguments to see your current setup.

### Update Settings:
- `/config ollama <url>`: Set your Ollama API endpoint.
- `/config comfy <url>`: Set your ComfyUI server address.
- `/config comfy_output <path>`: Set where the agent looks for generated images.
- `/config piper_path/piper_model <path>`: Configure TTS binary and voices.

---

## 🚀 Advanced Usage

### Autonomous Multi-Step Tasks
Because of the iterative reasoning loop, you can give complex commands:
> "Search the web for the latest version of FastAPI, create a main.py file with a basic API using that version, and run it to make sure it works."

### Codebase Investigation
The agent can map out unfamiliar projects:
> "Use get_tree to show me this project, then grep for 'API_KEY' to see how secrets are handled."

### Remote Control (ntfy.sh)
Enable `/notify setup <topic>`. You can then send prompts to your agent via any ntfy client (mobile app or web) and get results back as push notifications.

---

## 🧪 Testing

The project includes a full test suite to ensure stability.
To run tests:
```bash
python3 tests/test_all.py
```

## 📜 License
MIT
