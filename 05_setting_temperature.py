# Temperature = 0 → least random, more deterministic/predictable
# Temperature = 1 → more random/varied, potentially more creative
# Think of it as:
# 0 → consistency
# 1 → creativity/variation

import os
from dotenv import load_dotenv
import anthropic
from params import MODEL_NAME

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def chat(messages, temperature = None):

    params = {
        "model": MODEL_NAME,
        "max_tokens": 200,
        "messages": messages,
        "temperature": temperature
    }

    message = client.messages.create(
        **params
    )
    return message.content[0].text

query = "Give me a list of 5 business names which I can start in India. No commentary, just crips list and be creative"
messages = []

add_user_message(messages, query)

answer = chat(messages, temperature=0)
print("T=0:", answer)

print("\n----------------\n")

answer = chat(messages, temperature=1)
print("T=1:", answer)
