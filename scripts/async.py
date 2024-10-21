import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue? Answer in 100 words maximum'}
  response = await AsyncClient(host='http://ollama_api:11434').chat(model='llama3.2', messages=[message])
  print(response)

asyncio.run(chat())
