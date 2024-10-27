from pprint import pprint as pp

from ollama import Client
client = Client(host='http://ollama_api:11434')
response = client.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue? Answer in 100 words maximum',
  },
])

pp(response)