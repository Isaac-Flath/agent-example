#!/usr/bin/env python3
import json
import os
import typer

TODO_FILE = "todos.json"
app = typer.Typer()

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.command()
def add(task: str):
    """Add a new todo"""
    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)
    typer.echo(f"✅ Added: {typer.style(task, fg=typer.colors.GREEN)}")

@app.command()
def list():
    """List all todos"""
    todos = load_todos()
    if not todos:
        typer.echo(typer.style("📝 No todos found!", fg=typer.colors.YELLOW))
        return
    
    typer.echo(typer.style("📋 Your todos:", fg=typer.colors.BLUE, bold=True))
    for i, todo in enumerate(todos, 1):
        if todo["done"]:
            status = typer.style("✓", fg=typer.colors.GREEN)
            task_text = typer.style(todo["task"], fg=typer.colors.BRIGHT_BLACK, strikethrough=True)
        else:
            status = typer.style("○", fg=typer.colors.YELLOW)
            task_text = todo["task"]
        typer.echo(f"  {i}. {status} {task_text}")

@app.command()
def done(index: int):
    """Mark a todo as complete"""
    todos = load_todos()
    if 1 <= index <= len(todos):
        todos[index-1]["done"] = True
        save_todos(todos)
        task = todos[index-1]["task"]
        typer.echo(f"🎉 Completed: {typer.style(task, fg=typer.colors.GREEN)}")
    else:
        typer.echo(typer.style("❌ Invalid todo number", fg=typer.colors.RED))

if __name__ == "__main__":
    app()