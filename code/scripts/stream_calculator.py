import json
import ollama
import asyncio
import math

# Calculator tool to evaluate a mathematical expression
def calculate_expression(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})

async def run(model: str):
    client = ollama.AsyncClient(host='http://ollama_api:11434')
    # Initial user message requesting a calculation
    messages = [{'role': 'user', 'content': 'What is the result of 5 * (3 + 7) ** 2 / 2 + 45?'}]

    # First request to the model with the tool description, using streaming
    async for part in await client.chat(
        model=model,
        messages=messages,
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'calculate_expression',
                    'description': 'Calculate the result of a mathematical expression',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'expression': {
                                'type': 'string',
                                'description': 'The mathematical expression to evaluate',
                            },
                        },
                        'required': ['expression'],
                    },
                },
            },
        ],
        stream=True
    ):
        # Print each streaming part as it arrives
        print(part['message']['content'], end='', flush=True)
        # Check if the model decided to make a tool call
        if part['message'].get('tool_calls'):
            available_functions = {
                'calculate_expression': calculate_expression,
            }
            for tool in part['message']['tool_calls']:
                function_to_call = available_functions[tool['function']['name']]
                # Execute the function with provided arguments
                function_response = function_to_call(tool['function']['arguments']['expression'])
                # Add the tool's result as a message in the conversation history
                messages.append(
                    {
                        'role': 'tool',
                        'content': function_response,
                    }
                )
    
    # After the tool call, make a second request to get the final response
    async for part in await client.chat(model=model, messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)
    print("\n")

# Run the async function
asyncio.run(run('llama3.2'))
