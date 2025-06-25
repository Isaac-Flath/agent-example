"""
Main EntryPoint for the AI.

- Takes a prompt from the user
- Generates content using the AI
- Calls the functions that are available to the AI
- If the function call is successful, the function response is added to the messages
- Returns the response to the user
"""
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import typer

from prompts import system_prompt
from call_function import call_function, available_functions

app = typer.Typer()

def generate_content(client, messages):
    """Generate content using AI with function calling capabilities."""
    max_iterations = 20 # Make sure we don't loop forever!
    for iteration in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        for candidate in response.candidates:
            # Add response to the conversation history
            messages.append(candidate.content)

        if not response.function_calls:
            # If no function calls, we are done!
            print("Final response:")
            print(response.text)
            break

        # If there are function calls, we need to call the functions
        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part)
            function_responses.append(function_call_result.parts[0])

        # Add the function responses to the conversation history
        for function_response_part in function_responses:
            messages.append(types.Content(role="user", parts=[function_response_part]))
    
    if iteration == max_iterations - 1:
        print("Maximum iterations reached.")

@app.command()
def main(prompt: str, verbose: bool = False):
    """Main entry point for the AI agent."""
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Start the conversation with the user's prompt
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    # Generate content and do the tool loop
    generate_content(client, messages)

if __name__ == "__main__":
    app()
