# Ollama CLI v3.0

An extremely powerful, modular, and commercially-ready CLI for local Ollama LLMs. Inspired by Gemini CLI and Kiro CLI.

## Features

- **Rich UI:** Beautifully formatted output using `rich`.
- **Powerful REPL:** Multi-line input, history, and completions via `prompt_toolkit`.
- **Modular Tool System:** Easily extensible tool architecture (Filesystem, System, Web, etc.).
- **Session Management:** Save and resume conversations with ease.
- **Model Intelligence:** Automatically switches models based on task type (coding vs. general).
- **Streaming Responses:** Real-time feedback as the model generates text.
- **MCP Support:** Ready for Model Context Protocol integration.
- **Local First:** Everything runs locally on your machine.

## Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running.

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ollama-cli.git
   cd ollama-cli
   ```

2. Install in editable mode:
   ```bash
   pip install -e .
   ```

## Usage

Run the CLI:
```bash
ollama-cli
```

### Full Documentation
For detailed information on architecture, tool list, and advanced configurations, see **[DOCUMENTATION.md](./DOCUMENTATION.md)**.

### Slash Commands
- `/quit` - Exit the CLI.
- `/clear` - Clear conversation history.
- `/models` - List available models.
- `/model <name>` - Switch to a specific model.
- `/sessions` - List recent sessions.
- `/save [name]` - Save the current session.
- `/load <name>` - Load a saved session.

## Configuration

Config is stored at `~/.ollama-cli-config.json`. You can configure:
- `ollama_url`: The URL of your Ollama server.
- `default_model`: The model to use by default.
- `excluded_models`: Models to hide from the list.

## Architecture

- `src/ollama_cli/core`: Core logic (API, Config, Sessions).
- `src/ollama_cli/tools`: Tool implementations and registry.
- `src/ollama_cli/ui`: REPL and rich formatting.
- `src/ollama_cli/integrations`: External integrations (MCP, LSP, Notify).

## License
MIT
