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
        self.working_directory = Path(working_directory).resolve()
        
    def _resolve_path(self, file_path: str) -> Path:
        if Path(file_path).is_absolute():
            return Path(file_path).resolve()
        return (self.working_directory / file_path).resolve()
    
    def list_files(self, directory: Optional[str] = None) -> str:
        """List files and directories."""
        target_dir = self._resolve_path(directory) if directory else self.working_directory
        
        items = []
        for item in sorted(target_dir.iterdir()):
            if item.is_dir():
                items.append(f"{item.name}/ [DIR]")
            else:
                items.append(f"{item.name} ({item.stat().st_size} bytes)")
                
        return f"Files in {target_dir}:\n" + "\n".join(items) if items else "No files found"
    
    def read_file(self, file_path: str) -> str:
        """Read content from a file."""
        full_path = self._resolve_path(file_path)
        content = full_path.read_text(encoding='utf-8', errors='replace')
        
        if len(content) > 50_000:
            content = content[:50_000] + "\n... (truncated)"
            
        return content
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file."""
        full_path = self._resolve_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        
        return f"Wrote {len(content):,} characters to '{file_path}'"
    
    def replace_in_file(self, file_path: str, old_string: str, new_string: str) -> str:
        """Replace string in file and show diff."""
        full_path = self._resolve_path(file_path)
        original_content = full_path.read_text(encoding='utf-8')
        new_content = original_content.replace(old_string, new_string)
        
        diff_lines = list(difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{file_path} (before)",
            tofile=f"{file_path} (after)",
            n=3
        ))
        
        full_path.write_text(new_content, encoding='utf-8')
        diff_output = "".join(diff_lines)
        
        return f"Replaced in '{file_path}':\n{diff_output}" if diff_output else f"No changes made to '{file_path}'"


class TodoTools(llm.Toolbox):
    """Todo management toolbox."""
    
    def __init__(self, todos_file: str = "todo/todos.json"):
        self.todos_file = Path(todos_file)
        self.todos_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.todos_file.exists():
            self.todos_file.write_text("[]", encoding='utf-8')
            
    def _load_todos(self) -> List[Dict[str, Any]]:
        content = self.todos_file.read_text(encoding='utf-8')
        return json.loads(content) if content else []
            
    def _save_todos(self, todos: List[Dict[str, Any]]):
        content = json.dumps(todos, indent=2, ensure_ascii=False)
        self.todos_file.write_text(content, encoding='utf-8')
    
    def add_todo(self, task: str) -> str:
        """Add a new todo item."""
        todos = self._load_todos()
        todos.append({
            "task": task,
            "done": False,
            "created": datetime.now().isoformat()
        })
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
            lines.append(f"{i + 1}. [{status}] {todo['task']}")
            
        return "\n".join(lines)
    
    def mark_todo_done(self, index: int) -> str:
        """Mark a todo as completed."""
        todos = self._load_todos()
        
        todo = todos[index - 1]
        todo["done"] = True
        todo["completed"] = datetime.now().isoformat()
        self._save_todos(todos)
        
        return f"✅ Marked as done: '{todo['task']}'"


def create_system_prompt() -> str:
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
    llm_model = llm.get_model(model)
    file_tools = FileTools()
    todo_tools = TodoTools()
    conversation = llm_model.conversation(tools=[file_tools, todo_tools])
    response = conversation.chain(prompt, system=create_system_prompt())
    
    # Output response
    for chunk in response:
        print(chunk, end="", flush=True)
    print()
    
    # Show tool calls
    tool_calls = []
    for r in response.responses():
        if hasattr(r, 'tool_calls'):
            tool_calls.extend(r.tool_calls())
    
    if tool_calls:
        typer.secho("\nTool calls:", fg=typer.colors.GREEN)
        for call in tool_calls:
            args = ', '.join(f'{k}={v!r}' for k, v in call.arguments.items())
            typer.echo(f"  - {call.name}({args})")
                

if __name__ == "__main__":
    app()