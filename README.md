> ### WARNING
> This repo is not ready to be shared yet.  It will probably change drastically several more times and probably has some bugs
> I am building publicly for those that follow, but please do not share widely on social media or other sites just yet!


# AI Code Assistant

A minimal AI coding agent that can read, write, and execute code in your projects using Google's Gemini API.

## Credit

This was heavily inspired and some pieces of the code come from an upcoming agent course on [boot.dev](https://www.boot.dev/dashboard?promo=ISAAC) that I have seen the beta version of (not yet released!).  If you want to learn to build a different coding agent step-by-step way and learn all the details along the way, check out boot.dev.  The code in this repo is more minimal and less robust that you will learn in the boot.dev course.

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

**Add multiple todos:**
```bash
python main.py "Add three todos: buy groceries, call mom, finish project"
```

**Add multiple todos:**
```bash
python main.py "Mark all my todos as done"
```

### Coding Tasks

**Analyze the code:**

```bash
python main.py "Analyze the todo app code and suggest improvements without making any code changes"
```

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

# Future Plans for the Repo

- Add a variety of agent examples not just coding/todo
- Inspect for evals setup
- RL
- Tracing

# Things you could do for learning

Lots of options. 

**Complete Missing Todo Features:**
- Add delete option to todo app, then add it as a function for the agent to call
- Add todo priority levels (high, medium, low) with color coding and improve agent to be able to filter by them
- Add due dates to todos with simple date parsing

**Improve User Experience:**
- Add y/n confirmation prompts for destructive operations (file overwrites, deletions)
- Improve CLI output formatting with better colors so it feels good
- Add a verbose mode so when people want they can see more details of what's going on.  Format it so it's readable and feels good.

**Enhanced File Operations:**
- Add `search_files` function to find text patterns across multiple files
- Add `backup_file` and `restore_file` functions for file versioning
- Create `create_directory` and `remove_directory` functions
- Add metadata info to `list_files` (such as modified date)

**Evals:**
- Create a logging/tracing system to track all agent actions and errors
- Store traces somewhere (disk, pheonix, etc).
- Evaluate and create a eval set (see [AI Evals Course](bit.ly/evals-ai) for lots of information on how to do this)
- Iterate and improve prompt based on evals

**Add conversation memory to remember context between interactions**

**Development Tools:**
- Add git integration (status, add, commit, diff)
- Create `run_command` function to execute shell commands safely (with permission)

**Configuration & Extensibility:**
- Create a config file system for customizing agent behavior
- Add support for multiple working directories

**Implement streaming for large file operations**

**Create database integration for persistent data**
