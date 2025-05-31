import os, subprocess
import difflib
import json
from google.genai import types


__all__ = [
    "list_files",
    "get_file_content",
    "overwrite_file",
    "replace_str_file",
    "todo_add",
    "todo_list", 
    "todo_done",
    "schema_list_files",
    "schema_get_file_content",
    "schema_overwrite_file",
    "schema_replace_str_file",
    "schema_todo_add",
    "schema_todo_list",
    "schema_todo_done",
]
MAX_CHARS = 100000


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

@handle_errors
def list_files(working_directory, directory=None):
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
        if not target_dir.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot access "{directory}" as it is outside the permitted working directory'
    else:
        target_dir = os.path.abspath(working_directory)
    
    if not os.path.exists(target_dir):
        return f'Error: Directory "{directory or "."}" does not exist'
    
    files_info = []
    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)
        is_dir = os.path.isdir(filepath)
        files_info.append(f"- {filename} {'(dir)' if is_dir else ''}")
    return "\n".join(files_info)

@handle_errors
def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" does not exist'
    
    with open(abs_path, "r", encoding='utf-8') as f:
        content = f.read(MAX_CHARS)
        if len(content) == MAX_CHARS:
            content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content

@handle_errors
def overwrite_file(working_directory, file_path, content):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding='utf-8') as f: f.write(content)
    return f'Successfully wrote to "{file_path}"'

@handle_errors
def replace_str_file(working_directory, file_path, old_str, new_str):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" does not exist'
    
    with open(abs_path, 'r', encoding='utf-8') as f: original_content = f.read()
    
    if old_str not in original_content:
        return f'String "{old_str}" not found in file "{file_path}"'
    
    new_content = original_content.replace(old_str, new_str)
    
    diff = list(difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f'a/{file_path}',
        tofile=f'b/{file_path}',
        lineterm=''))
    
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return ''.join(diff) if diff else f'Successfully replaced "{old_str}" with "{new_str}" in {file_path}'

@handle_errors
def todo_add(working_directory, task):
    """Add a new todo item"""
    todo_file = os.path.join(working_directory, "todos.json")
    if os.path.exists(todo_file):
        with open(todo_file, 'r', encoding='utf-8') as f:
            todos = json.load(f)
    else:
        todos = []
    
    todos.append({"task": task, "done": False})
    
    with open(todo_file, 'w', encoding='utf-8') as f:
        json.dump(todos, f, indent=2)
    
    return f"✅ Added: {task}"

@handle_errors
def todo_list(working_directory):
    """List all todo items"""
    todo_file = os.path.join(working_directory, "todos.json")
    if not os.path.exists(todo_file):
        return "📝 No todos found!"
    
    with open(todo_file, 'r', encoding='utf-8') as f:
        todos = json.load(f)
    
    if not todos:
        return "📝 No todos found!"
    
    result = ["📋 Your todos:"]
    for i, todo in enumerate(todos, 1):
        if todo["done"]:
            status = "✓"
            task_text = f"~~{todo['task']}~~"
        else:
            status = "○"
            task_text = todo["task"]
        result.append(f"  {i}. {status} {task_text}")
    
    return "\n".join(result)

@handle_errors
def todo_done(working_directory, index):
    """Mark a todo item as complete"""
    todo_file = os.path.join(working_directory, "todos.json")
    if not os.path.exists(todo_file):
        return "❌ No todos found!"
    
    with open(todo_file, 'r', encoding='utf-8') as f:
        todos = json.load(f)
    
    if not todos:
        return "❌ No todos found!"
    
    if 1 <= index <= len(todos):
        todos[index-1]["done"] = True
        with open(todo_file, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2)
        task = todos[index-1]["task"]
        return f"🎉 Completed: {task}"
    else:
        return "❌ Invalid todo number"

# Schemas
schema_list_files = types.FunctionDeclaration(
    name="list_files",
    description="Lists files and directories in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_overwrite_file = types.FunctionDeclaration(
    name="overwrite_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

schema_replace_str_file = types.FunctionDeclaration(
    name="replace_str_file",
    description="Replaces all occurrences of a string in a file and shows the diff of changes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to modify, relative to the working directory.",
            ),
            "old_str": types.Schema(
                type=types.Type.STRING,
                description="The string to find and replace.",
            ),
            "new_str": types.Schema(
                type=types.Type.STRING,
                description="The string to replace with.",
            ),
        },
        required=["file_path", "old_str", "new_str"],
    ),
)

schema_todo_add = types.FunctionDeclaration(
    name="todo_add",
    description="Add a new todo item to the todo list.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "task": types.Schema(
                type=types.Type.STRING,
                description="The task description to add to the todo list.",
            ),
        },
        required=["task"],
    ),
)

schema_todo_list = types.FunctionDeclaration(
    name="todo_list",
    description="List all todo items showing their status (completed or pending).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)

schema_todo_done = types.FunctionDeclaration(
    name="todo_done",
    description="Mark a todo item as complete by its number (1-based index).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "index": types.Schema(
                type=types.Type.INTEGER,
                description="The number of the todo item to mark as complete (starting from 1).",
            ),
        },
        required=["index"],
    ),
) 