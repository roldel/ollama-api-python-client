import asyncio
from ollama import AsyncClient

async def chat():
    message = {'role': 'user', 'content': 'Why is the sky blue? Answer in 100 words maximum'}
    async for part in await AsyncClient(host='http://ollama_api:11434').chat(model='llama3.2', messages=[message], stream=True):
        print(part['message']['content'], end='', flush=True)
    print("\n")


asyncio.run(chat())