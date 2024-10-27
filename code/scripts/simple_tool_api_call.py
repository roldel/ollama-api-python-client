import json
import ollama
import asyncio
import requests

# Function to get current weather data for a fixed location (latitude 52.52, longitude 13.41)
def get_weather_info() -> str:
    url = "http://localhost:8000/api/simple-json/"
    response = requests.get(url)
    return response.text if response.ok else json.dumps({'error': 'Unable to fetch weather data'})

async def run(model: str):
    client = ollama.AsyncClient(host="http://ollama_api:11434")
    # Initialize conversation with a user query
    messages = [{'role': 'user', 'content': 'What does the weather forecast report for Tuesday morning ?'}]

    # First API call: Send the query and function description to the model
    response = await client.chat(
        model=model,
        messages=messages,
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'get_weather_info',
                    'description': 'Get current weather data for Bourges, France',
                    'parameters': {
                        'type': 'object',
                        'properties': {},  # No parameters required since the location is fixed
                    },
                },
            },
        ],
    )

    # Add the model's response to the conversation history
    messages.append(response['message'])

    # Process function calls made by the model
    if response['message'].get('tool_calls'):
        available_functions = {
            'get_weather_info': get_weather_info,
        }
        for tool in response['message']['tool_calls']:
            function_name = tool['function']['name']
            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                function_response = function_to_call()
                # Add function response to the conversation
                messages.append({'role': 'tool', 'content': function_response})

    # Second API call: Get final response from the model
    final_response = await client.chat(model=model, messages=messages)
    print(final_response['message']['content'])

# Run the async function
asyncio.run(run('llama3.2'))
