import json
import ollama
import asyncio
import math

# Simulates a calculator to evaluate a mathematical expression
# In a real application, this would include safety checks for complex calculations
def calculate_expression(expression: str) -> str:
    try:
        # Use Python's eval function, limiting the allowed operations for safety
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})

async def run(model: str):
    client = ollama.AsyncClient(host="http://ollama_api:11434")
    # Initialize conversation with a user query
    messages = [{'role': 'user', 'content': 'What is the result of 5 * (3 + 7) ** 2 / 2 + 45?'}]

    # First API call: Send the query and function description to the model
    response = await client.chat(
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
    )

    # Add the model's response to the conversation history
    messages.append(response['message'])

    # Check if the model decided to use the provided function
    if not response['message'].get('tool_calls'):
        print("The model didn't use the function. Its response was:")
        print(response['message']['content'])
        return

    # Process function calls made by the model
    if response['message'].get('tool_calls'):
        available_functions = {
            'calculate_expression': calculate_expression,
        }
        for tool in response['message']['tool_calls']:
            function_to_call = available_functions[tool['function']['name']]
            function_response = function_to_call(tool['function']['arguments']['expression'])
            # Add function response to the conversation
            messages.append(
                {
                    'role': 'tool',
                    'content': function_response,
                }
            )

    # Second API call: Get final response from the model
    final_response = await client.chat(model=model, messages=messages)
    print(final_response['message']['content'])

# Run the async function
asyncio.run(run('mistral'))
