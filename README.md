```markdown
# ollama-cli

A feature-rich interactive command-line client for Ollama’s chat API. This script lets you chat with local models, manage conversation sessions, integrate with MCP and language servers, and even control it remotely via ntfy.sh notifications.[file:1]

---

## Features

- **Interactive chat** with streaming responses against your local Ollama server (`/api/chat`).[file:1]  
- **Model management**: list models, switch default model, and exclude models you do not want to use.[file:1]  
- **Session management**: save, load, and list past chat sessions stored under `~/.ollama-cli-sessions`.[file:1]  
- **Config file support** at `~/.ollama-cli-config.json` for excluded models, Ollama URL, MCP servers, git/Gitea, and ntfy settings.[file:1]  
- **Context files**: add local files as context for the assistant to use.[file:1]  
- **Knowledge base**: simple built-in knowledge storage and search.[file:1]  
- **MCP integration**: connect to MCP servers over stdio and expose their tools to the assistant.[file:1]  
- **LSP integration**: start language servers (Python, TypeScript/JavaScript, Rust, Go, etc.) via built-in commands.[file:1]  
- **Remote control via ntfy.sh**: send notifications to a topic and get answers back as notifications.[file:1]  
- **Export to Markdown** and basic git/Gitea helpers for working with repositories.[file:1]

---

## Requirements

- Python 3.8+.[file:1]  
- A running Ollama server (e.g. `ollama serve`) reachable at `http://localhost:11434` or another configured URL.[file:1]  
- Optional tools (only needed if you use the respective features):[file:1]  
  - MCP servers (any binaries you want to connect via `/mcp connect`).[file:1]  
  - Language servers: `pyright-langserver`, `typescript-language-server`, `rust-analyzer`, `gopls`, etc., on your `PATH`.[file:1]  
  - `git` and a Gitea instance if you use git / Gitea integration.[file:1]  

Install Python dependencies (if any external libraries beyond the standard library are used, such as `requests`):[file:1]

```bash
pip install requests
```

---

## Installation

1. Copy `ollama-cli.py` somewhere on your `PATH`, for example:[file:1]

   ```bash
   mkdir -p ~/.local/bin
   cp ollama-cli.py ~/.local/bin/ollama-cli
   chmod +x ~/.local/bin/ollama-cli
   ```

2. Ensure `~/.local/bin` is in your `PATH`.[file:1]  

3. Start your Ollama server, e.g.:[file:1]

   ```bash
   ollama serve
   ```

---

## Basic Usage

Run the CLI:

```bash
ollama-cli
# or
python3 ollama-cli.py
```

On startup it will:[file:1]

- Load `~/.ollama-cli-config.json` (or create defaults in memory).[file:1]  
- Detect available models from the Ollama server.[file:1]  
- Show the current directory, home directory, and a list of supported commands.[file:1]  

You then type messages at the `>` prompt and responses are streamed back to the terminal.[file:1]

Exit with:

```text
/quit
```

or `Ctrl+D` / `Ctrl+C`.[file:1]

---

## Commands

At the `>` prompt you can use various slash-commands.[file:1]

### Core commands

- `/quit` – Exit the program.[file:1]  
- `/clear` – Clear conversation history while keeping the system context.[file:1]  
- `/retry` – Retry the last request to the model.[file:1]  

### Sessions

- `/save` – Save current history to `chat_history.json` in the current directory.[file:1]  
- `/save [name]` – Save as a named session under `~/.ollama-cli-sessions/<name>.json`.[file:1]  
- `/load <name>` – Load a saved session by name.[file:1]  
- `/sessions` – List the most recent saved sessions.[file:1]

### Models

- `/models` – List available models from the Ollama server.[file:1]  
- `/model <name>` – Switch the default model for subsequent queries.[file:1]  
- `/exclude <name>` – Add a model to the excluded list in the config; takes effect after restart.[file:1]  
- `/list-excluded` – Show excluded models.[file:1]

### Configuration and server

- `/server` – Set the Ollama server URL (stored in config).[file:1]  
- `/config git` – Configure git credentials/remote in the config file.[file:1]  
- `/config gitea` – Configure Gitea server URL and token.[file:1]

### Files, context, and export

- `/run` – Execute a file (script helper, see implementation details in code).[file:1]  
- `/context` – Add a file to the context for the assistant.[file:1]  
- `/context list` – List context files.[file:1]  
- `/context clear` – Clear all context files.[file:1]  
- `/export` – Export the current conversation to Markdown.[file:1]

### Knowledge base

- `/kb add` – Add content to the internal knowledge base.[file:1]  
- `/kb search` – Search entries in the knowledge base.[file:1]

### MCP (Model Context Protocol)

- `/mcp connect <name> <command> [args...]` – Start an MCP server over stdio and register its tools.[file:1]  
- `/mcp list` – List connected MCP servers and their tools.[file:1]  
- `/mcp disconnect <name>` – Disconnect a specific MCP server.[file:1]

When connected, MCP tools are exposed to the assistant and described in the system prompt.[file:1]

### LSP (Language Server Protocol)

- `/lsp start <language> [path]` – Start a language server for a given language, optionally with a project root path.[file:1]  
  - Supported language keys include `python`, `javascript`, `typescript`, `rust`, `go` (see `start_lsp_server`).[file:1]

### Subagents

- `/agents` – Show status of running subagents.[file:1]

### Notifications (ntfy.sh)

- `/notify setup` – Configure ntfy settings in the config file (server, topic, enable flag).[file:1]  
- `/notify off` – Disable notifications in config.[file:1]  
- `/notify test` – Send a test notification.[file:1]

When notifications are enabled, the CLI starts an ntfy listener thread and:[file:1]

- Listens to `server/topic/json` for incoming notifications.[file:1]  
- Converts each notification into a user message.[file:1]  
- Sends back the assistant’s response as another notification (title `Response`).[file:1]

---

## Configuration

Config is stored at:

```text
~/.ollama-cli-config.json
```

A typical structure includes:[file:1]

```json
{
  "excluded_models": [],
  "git": {
    "remote_url": "",
    "username": "",
    "password": ""
  },
  "gitea": {
    "url": "",
    "token": ""
  },
  "auto_save_sessions": true,
  "mcp_servers": {},
  "ollama_url": "http://localhost:11434/api/chat",
  "ntfy": {
    "enabled": false,
    "topic": "",
    "server": "https://ntfy.sh"
  }
}
```

You can edit this by hand or through the `/config` and `/notify` commands.[file:1]

---

## Sessions Storage

Session files are stored under:

```text
~/.ollama-cli-sessions
```

Each session is a JSON document containing the messages and a timestamp, named like `YYYYMMDD_HHMMSS.json` (or your custom name).[[file:1]] You can back this folder up or sync it to move history between machines.[file:1]

---

## Development Notes

- The script uses `requests` for HTTP calls, `subprocess` for MCP/LSP processes, `threading` for the notification listener, and standard modules such as `json`, `os`, `sys`, and `pathlib`.[file:1]  
- The main loop keeps a `messages` list of system, user, and assistant messages and trims it to avoid unbounded context size.[file:1]  
- The default model is `llama3.2`, but this can be changed either at runtime via `/model` or by editing the script/config.[file:1]

---

## License

Add your preferred license here (e.g. MIT, Apache-2.0).

---

## Roadmap / Ideas

Some potential future improvements:

- Automatic reconnection and health checks for MCP and LSP servers.[file:1]  
- Richer TUI (colors, panes for context, session browser).[file:1]  
- Plugin system for additional transports or notification backends.[file:1]
```

Do you want this README tailored for publishing on GitHub (badges, screenshots, example configs), or kept minimal for local use?
