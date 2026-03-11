# Gemini Chatbot with File System and Code Execution Capabilities

This repository contains a Python-based chatbot powered by Google Gemini. This AI agent is designed to interact with the file system and execute Python code, making it a powerful tool for various automation and development tasks.

**⚠️ IMPORTANT NOTICE: This is a purely educational project and is not recommended for production use in any way. Executing arbitrary code from an AI model can introduce serious security vulnerabilities. For real applications, please consider more robust and secure tools like OpenCode or Claude Code.**

## Features

- **Google Gemini Integration**: Leverages the Google Gemini API for natural language understanding and generation.
- **File System Interaction**: Can list files and directories, read file content, and write to files.
- **Code Execution**: Capable of executing Python files with specified arguments.
- **Conversational Interface**: Engages in multi-turn conversations, allowing for complex task execution.
- **Detailed Output**: Provides detailed output, including token counts and function responses for better debugging and understanding.

## Available Functions

The chatbot has access to the following functions:

- `get_files_info()`: Lists files and directories in a specified path.
- `get_file_content(file_path)`: Reads the content of a specified file.
- `write_file(file_path, content)`: Writes or overwrites content to a specified file.
- `run_python_file(file_path, args)`: Executes a Python file with optional arguments.

## Setup and Installation

1.  **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Configure your Google Gemini API Key**: Obtain a Gemini API key from the Google Cloud Console or AI Studio. Create a `.env` file in the root directory of this project and add your API key:

    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

3.  **Install dependencies with `uv`**:
    Make sure you have `uv` installed (if not, you can install it with `curl -LsSf https://astral.sh/uv/install.sh | sh`).
    Then, activate the virtual environment and sync dependencies:
    ```bash
    uv venv
    source .venv/bin/activate # On Linux/macOS
    # Or: .venv\\Scripts\\activate # On Windows
    uv sync
    ```

## Usage

To run the chatbot, execute the `main.py` script with an initial prompt:

```bash
uv run python main.py "Your initial prompt here"
```

### Verbose Mode

To enable detailed output, use the `--verbose` flag:

```bash
uv run python main.py "Your initial prompt here" --verbose
```

## Project Structure

- `main.py`: The main entry point for the chatbot.
- `available_functions.py`: Defines the functions that the Gemini model can call.
- `core/`: Contains the core logic for function handling.
- `functions/`: Houses the implementations of the AI-callable functions.
- `utils/`: Utility functions and configurations.
- `prompts.py`: Stores the system prompt used to guide the AI's behavior.
- `config.py`: Configuration settings for the chatbot.

