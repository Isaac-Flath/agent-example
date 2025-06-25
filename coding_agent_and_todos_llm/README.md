# LLM Coding Agent

A lightweight implementation of a coding agent using Simon Willison's LLM library.

## Installation

```bash
pip install -r requirements.txt
```

## Setup

### API Key Configuration

Set up your Anthropic API key:

```bash
# Option 1: Environment variable
export ANTHROPIC_API_KEY='your-key-here'

# Option 2: Using LLM's key management
llm keys set claude
```

## Usage

### Basic Usage

```bash
python main.py "List all files in the todo directory"
```

### With Different Model

```bash
python main.py "Help me create a Python script" --model gpt-4
```

### Without Streaming

```bash
python main.py "Read the main.py file" --no-stream
```

### Verbose Mode

```bash
python main.py "Add a todo to buy milk" --verbose
```

## Examples

### File Operations

```bash
# List files
python main.py "Show me all files in the todo directory"

# Read a file
python main.py "Read the main.py file in the todo directory"

# Create a new file
python main.py "Create a new file called test.py with a hello world function"

# Modify existing file
python main.py "Add error handling to the main.py file"
```

### Todo Management

```bash
# Add todos
python main.py "Add a todo to finish the project documentation"

# List todos
python main.py "Show me all my todos"

# Complete a todo
python main.py "Mark the first todo as done"
```

## Architecture

The implementation uses LLM's Toolbox pattern:

- **FileTools**: Handles all file operations with path validation
- **TodoTools**: Manages todo items stored in JSON format
- **Security**: All operations are constrained to the `todo/` directory
- **Streaming**: Supports real-time output as the model generates responses

## Key Differences from Gemini Version

1. **Multi-model support**: Works with any model supported by LLM plugins
2. **Simpler architecture**: Single file implementation using Toolbox pattern
3. **Automatic tool execution**: Uses `model.chain()` for seamless tool usage
4. **Better error messages**: More descriptive and helpful error handling
5. **No manual schemas**: Tool schemas are auto-generated from docstrings

## Supported Models

Run this to see all available models:

```bash
llm models
```

Popular options:
- `claude-3.5-sonnet` (default)
- `gpt-4`
- `gpt-4o-mini`
- Any model from installed LLM plugins

## Troubleshooting

### API Key Not Found

If you get an API key error, make sure you've set up your key:

```bash
# For Anthropic/Claude
export ANTHROPIC_API_KEY='your-key'

# For OpenAI
export OPENAI_API_KEY='your-key'
```

### Model Not Found

Install the appropriate plugin:

```bash
# For Claude models
pip install llm-anthropic

# For other providers
llm install llm-ollama  # for local models
llm install llm-gemini  # for Google models
```

### Permission Errors

Make sure the script is executable:

```bash
chmod +x main.py
```