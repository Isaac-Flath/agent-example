#!/usr/bin/env python3
"""
LLM-based coding agent with file and todo management capabilities.
Uses claude-3.5-sonnet by default with support for other models.
"""

import llm
import typer
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
import difflib
from datetime import datetime

app = typer.Typer(help="AI coding assistant powered by LLM")


class FileTools(llm.Toolbox):
    """File operations toolbox."""
    
    def __init__(self, working_directory: str = "."):
        """Initialize with current directory as default."""
        self.working_directory = Path(working_directory).resolve()
        
    def _resolve_path(self, file_path: str) -> Path:
        """Resolve path relative to working directory."""
        if Path(file_path).is_absolute():
            return Path(file_path).resolve()
        return (self.working_directory / file_path).resolve()
    
    def list_files(self, directory: Optional[str] = None) -> str:
        """List files and directories.
        
        Args:
            directory: Directory path (absolute or relative to working directory)
        """
        target_dir = self._resolve_path(directory) if directory else self.working_directory
        
        if not target_dir.exists():
            return f"Error: Directory '{directory}' not found"
            
        if not target_dir.is_dir():
            return f"Error: '{directory}' is not a directory"
            
        items = []
        for item in sorted(target_dir.iterdir()):
            if item.is_dir():
                items.append(f"{item.name}/ [DIR]")
            else:
                size = item.stat().st_size
                items.append(f"{item.name} ({size} bytes)")
                
        if not items:
            return "No files found in directory"
            
        return f"Files in {target_dir}:\n" + "\n".join(items)
    
    def read_file(self, file_path: str) -> str:
        """Read content from a file.
        
        Args:
            file_path: Path to file (absolute or relative)
        """
        full_path = self._resolve_path(file_path)
        
        if not full_path.exists():
            return f"Error: File '{file_path}' not found"
            
        if not full_path.is_file():
            return f"Error: '{file_path}' is not a file"
            
        content = full_path.read_text(encoding='utf-8', errors='replace')
        
        if len(content) > 100_000:
            content = content[:100_000] + "\n... (truncated)"
            
        return content
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file.
        
        Args:
            file_path: Path to file (absolute or relative)
            content: Content to write
        """
        full_path = self._resolve_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        
        return f"Successfully wrote {len(content):,} characters to '{file_path}'"
    
    def replace_in_file(self, file_path: str, old_string: str, new_string: str) -> str:
        """Replace string in file and show diff.
        
        Args:
            file_path: Path to file (absolute or relative)
            old_string: String to find and replace
            new_string: Replacement string
        """
        full_path = self._resolve_path(file_path)
        
        if not full_path.exists():
            return f"Error: File '{file_path}' not found"
            
        original_content = full_path.read_text(encoding='utf-8')
        
        if old_string not in original_content:
            return f"Error: String '{old_string}' not found in '{file_path}'"
            
        new_content = original_content.replace(old_string, new_string)
        
        diff_lines = list(difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{file_path} (before)",
            tofile=f"{file_path} (after)",
            n=3
        ))
        
        full_path.write_text(new_content, encoding='utf-8')
        
        diff_output = "".join(diff_lines) if diff_lines else "No visible changes in diff"
        return f"Successfully replaced in '{file_path}':\n\n{diff_output}"


class TodoTools(llm.Toolbox):
    """Todo management toolbox."""
    
    def __init__(self, todos_file: str = "todo/todos.json"):
        """Initialize with todos file path."""
        self.todos_file = Path(todos_file)
        self.todos_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        """Create todos file if it doesn't exist."""
        if not self.todos_file.exists():
            self.todos_file.write_text("[]", encoding='utf-8')
            
    def _load_todos(self) -> List[Dict[str, Any]]:
        """Load todos from file."""
        if not self.todos_file.exists():
            return []
            
        content = self.todos_file.read_text(encoding='utf-8')
        if not content:
            return []
            
        return json.loads(content)
            
    def _save_todos(self, todos: List[Dict[str, Any]]):
        """Save todos to file."""
        content = json.dumps(todos, indent=2, ensure_ascii=False)
        self.todos_file.write_text(content, encoding='utf-8')
    
    def add_todo(self, task: str) -> str:
        """Add a new todo item.
        
        Args:
            task: Description of the task
        """
        todos = self._load_todos()
        new_todo = {
            "task": task,
            "done": False,
            "created": datetime.now().isoformat()
        }
        todos.append(new_todo)
        self._save_todos(todos)
        
        return f"✅ Added todo: '{task}'"
    
    def list_todos(self) -> str:
        """List all todos with their status."""
        todos = self._load_todos()
        
        if not todos:
            return "No todos found. Add one with add_todo()"
            
        lines = ["Todo List:"]
        for i, todo in enumerate(todos):
            status = "✓" if todo.get("done", False) else "○"
            task = todo.get("task", "Unknown task")
            lines.append(f"{i + 1}. [{status}] {task}")
            
        return "\n".join(lines)
    
    def mark_todo_done(self, index: int) -> str:
        """Mark a todo as completed.
        
        Args:
            index: 1-based index of the todo to mark as done
        """
        todos = self._load_todos()
        
        if not todos:
            return "Error: No todos found"
            
        if index < 1 or index > len(todos):
            return f"Error: Invalid index {index}. Valid range: 1-{len(todos)}"
            
        todo = todos[index - 1]
        if todo.get("done", False):
            return f"Todo '{todo['task']}' is already marked as done"
            
        todo["done"] = True
        todo["completed"] = datetime.now().isoformat()
        self._save_todos(todos)
        
        return f"✅ Marked as done: '{todo['task']}'"


def create_system_prompt() -> str:
    """Create the system prompt for the agent."""
    return """You are an AI coding assistant with file and todo management capabilities.

You have access to the following tools:

File Operations:
- list_files(directory): List files and directories
- read_file(file_path): Read file content  
- write_file(file_path, content): Write content to file
- replace_in_file(file_path, old_string, new_string): Replace text in file

Todo Operations:
- add_todo(task): Add a new todo item
- list_todos(): List all todos with their status
- mark_todo_done(index): Mark a todo as completed (1-based index)

Be helpful and concise in your responses."""


@app.command()
def main(
    prompt: str = typer.Argument(..., help="Your prompt for the AI assistant"),
    model: str = typer.Option("claude-3.5-sonnet", "--model", "-m", help="LLM model to use"),
):
    """AI coding assistant with file and todo management."""
    try:
        # Initialize model
        try:
            llm_model = llm.get_model(model)
        except llm.UnknownModelError:
            typer.secho(f"Error: Unknown model '{model}'", fg=typer.colors.RED)
            typer.echo("Try: claude-3.5-sonnet, gpt-4o-mini, or run 'llm models'")
            raise typer.Exit(1)
            
        # Create toolboxes
        file_tools = FileTools()
        todo_tools = TodoTools()
        
        # Create conversation with tools
        conversation = llm_model.conversation(tools=[file_tools, todo_tools])
        
        # Execute prompt
        response = conversation.chain(prompt, system=create_system_prompt())
        
        # Collect all tool calls before displaying
        all_tool_calls = []
        
        # Output response
        for chunk in response:
            print(chunk, end="", flush=True)
        print()
            
        # Show tool usage in verbose mode
        if hasattr(response, 'responses'):
            seen_calls = set()  # Track unique tool calls
            for r in response.responses():
                if hasattr(r, 'tool_calls'):
                    calls = r.tool_calls()
                    if calls:
                        for call in calls:
                            # Create a unique identifier for each tool call
                            call_id = f"{call.name}_{call.arguments}"
                            if call_id not in seen_calls:
                                seen_calls.add(call_id)
                                all_tool_calls.append(call)
        
        # Display unique tool calls once at the end
        if all_tool_calls:
            typer.secho("\nTool calls:", fg=typer.colors.GREEN)
            for call in all_tool_calls:
                args = ', '.join(f'{k}={v!r}' for k,v in call.arguments.items())
                typer.echo(f"  - {call.name}({args})")
            
    except llm.APIError as e:
        if "api" in str(e).lower() and "key" in str(e).lower():
            typer.secho("Error: Missing API key. Set with:", fg=typer.colors.RED)
            typer.echo("  llm keys set anthropic  # for Claude")
            typer.echo("  llm keys set openai    # for GPT")
        else:
            typer.secho(f"API Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)
    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()