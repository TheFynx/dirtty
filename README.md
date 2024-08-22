# Dirtty - Directory Chat AI Assistant

Dirtty (Directory + TTY) is a terminal-based AI assistant for querying your local document collections. It provides an intuitive interface for interacting with your files and directories using advanced language models and retrieval techniques.

## Features

- Terminal-based user interface built with Textual
- Integration with Ollama for local language model support
- Document indexing and querying powered by LlamaIndex
- Flexible configuration through command-line arguments and YAML files
- Custom theme support with YAML-based color schemes
- Comprehensive logging for troubleshooting

## Prerequisites

- Python 3.12 or higher
- Poetry (Python package manager)
- Ollama installed and running on your system

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/dirtty.git
   cd dirtty
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Ensure Ollama is running on your system:

   ```bash
   ollama serve
   ```

2. Run Dirtty:

   ```bash
   poetry run dirtty
   ```

   If you haven't specified a directory using the `--directory` flag, you'll be prompted to select a directory containing your documents.

3. Use the terminal user interface (TUI) to interact with the chatbot:
   - Navigate the directory structure using the tree view on the left
   - Type your questions in the input field at the bottom
   - Press Enter to submit your question
   - View the AI's responses in the main chat window

## Configuration

You can customize Dirtty's behavior using command-line arguments or by editing the `config.yaml` file.

### Command-line Arguments

- `--directory`: Specify the directory containing documents to index
- `--model-name`: Specify the name of the Ollama model to use (default: "llama3:latest")
- `--theme`: Specify the theme to use (default: "default")
- `-v`, `-vv`: Increase verbosity level (info, debug)

Example:

```bash
poetry run dirtty --directory /path/to/docs --model-name llama2:7b --theme synthwave -vv
```

### Configuration File

You can also create a `config.yaml` file in the project root to set default values:

```yaml
directory: /path/to/default/docs
model_name: llama3:latest
theme: default
log_level: INFO
```

## Custom Themes

You can create custom themes by adding YAML files to the `themes` directory. Here's an example structure for a theme file:

```yaml
name: synthwave
dark: true
colors:
  primary: "#ff00ff"
  secondary: "#721d89"
  background: "#2b213a"
  surface: "#241b2f"
  panel: "#362f45"
  boost: "rgba(255, 255, 255, 0.05)"
  success: "#72f1b8"
  warning: "#fede5d"
  error: "#fe4450"
  accent: "#f97e72"
```

## Development

Dirtty uses [Taskfile](https://taskfile.dev/) for common development tasks. Here are some useful commands:

- `task install`: Install project dependencies
- `task run`: Run the Dirtty application
- `task run:ollama`: Run Dirtty with a specific Ollama model
- `task test`: Run tests
- `task lint`: Run linter
- `task format`: Format code
- `task clean`: Clean up generated files

For a full list of available tasks, run `task --list-all`.

## Logging

Dirtty logs information to `~/.dirtty/logs/dirtty.log`. You can adjust the log level using the verbosity flags (`-v`, `-vv`) to get more detailed information for troubleshooting.

## Contributing

Contributions to Dirtty are welcome! Please feel free to submit a Pull Request.

## License

[Specify your chosen license here, e.g., MIT, GPL, etc.]

## Acknowledgments

- LlamaIndex for providing the core indexing and querying functionality
- Textual for the powerful TUI framework
- Ollama for local language model support
- The open-source community for various dependencies and inspirations