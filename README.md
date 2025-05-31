# AI Code Assistant

A minimal AI coding agent that can read, write, and execute code in your projects using Google's Gemini API.

## Credit

This was heavily inspired and some pieces of the code come from an upcoming agent course on [boot.dev](https://www.boot.dev/dashboard?promo=ISAAC) that I have seen the beta version of (not yet released!).  If you want to learn to build a different coding agent step-by-step way, check out boot.dev.  The code in this repo is more minimal and less robust that you will learn in the boot.dev course.

## Setup

1. Install dependencies:
```bash
pip install requirements.txt
```

2. Set up your Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

```bash
python main.py "your prompt here" [--verbose]
```

The AI agent can:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Replace strings in files (shows diff of changes)
- Add todo items
- List todo items  
- Mark todo items as complete

All operations are scoped to the `todo/` directory for safety.

## Example Commands

### Basic File Operations

**List files in the todo directory:**
```bash
python main.py "What files are in the todo directory?"
```

**Read the todo app code:**
```bash
python main.py "What's the main.py file do?"
```

**Read the README:**
```bash
python main.py "What does the README say about the todo app?"
```

### Todo Management

**List current todos:**
```bash
python main.py "Show me my current todo list"
```

**Add a new todo:**
```bash
python main.py "Add a todo: Learn Python fundamentals"
```

**Mark a todo as complete:**
```bash
python main.py "Mark todo number 1 as done"
```

**Add multiple todos:**
```bash
python main.py "Add three todos: buy groceries, call mom, finish project"
```

### Running the Todo App

`cd` into the todo directory

**Test the todo app directly:**
```bash
python main.py "list my todoes"
```

### Code Analysis and Improvement

**Analyze the code:**
```bash
python main.py "Analyze the todo app code and suggest improvements"
```

**Check for bugs:**
```bash
python main.py "Review the todo app for potential bugs or issues"
```

**Explain the code:**
```bash
python main.py "Explain how the todo app works step by step"
```

### Code Modifications

**Add a new feature:**
```bash
python main.py "Add a delete todo function to the todo app"
```

Test it

```bash
cd todo
python main.py list
python main.py delete 1
python main.py list
```

## Verbose Mode

Add `--verbose` to see detailed function calls and token usage:

```bash
python main.py "Show me the todo app code" --verbose
```

This will display:
- The exact prompt sent to the AI
- Function calls being made
- Function responses
- Token usage statistics
