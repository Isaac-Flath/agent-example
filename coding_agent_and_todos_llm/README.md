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

```bash
python main.py "Help me create a Python script"
```

```bash
python main.py "Read the main.py file"
```

```bash
python main.py "Add a todo to buy milk and another to call mom"
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