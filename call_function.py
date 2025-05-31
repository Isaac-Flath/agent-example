from google.genai import types
from functions import *

available_functions = types.Tool(
    function_declarations=[
        schema_list_files,
        schema_get_file_content,
        schema_overwrite_file,
        schema_replace_str_file,
        schema_todo_add,
        schema_todo_list,
        schema_todo_done,
    ])

function_map = {
    "list_files": list_files,
    "get_file_content": get_file_content,
    "overwrite_file": overwrite_file,
    "replace_str_file": replace_str_file,
    "todo_add": todo_add,
    "todo_list": todo_list,
    "todo_done": todo_done,
}


def call_function(function_call_part, verbose=False):
    if verbose: print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else: print(f" - Calling function: {function_call_part.name}")
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(name=function_name,
                    response={"error": f"Unknown function: {function_name}"})])
    
    args = dict(function_call_part.args)
    args["working_directory"] = 'todo'
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(name=function_name,
                response={"result": function_result})])
