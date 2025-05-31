import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import typer

from prompts import system_prompt
from call_function import call_function, available_functions

app = typer.Typer()

def generate_content(client, messages, verbose):
    max_iterations = 20
    for iteration in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.function_calls:
            print("Final response:")
            print(response.text)
            break

        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")

        for function_response_part in function_responses:
            messages.append(types.Content(role="user", parts=[function_response_part]))
    
    if iteration == max_iterations - 1:
        print("Maximum iterations reached.")

@app.command()
def main(prompt: str, verbose: bool = False):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    generate_content(client, messages, verbose)

if __name__ == "__main__":
    app()
