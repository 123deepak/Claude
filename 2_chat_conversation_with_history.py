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

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=50,
        messages=messages,
    )
    return message.content[0].text

# Start with an empty message list
messages = []

# Add the initial user question
add_user_message(messages, "Define quantum computing in one sentence")

# Get Claude's response
answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)

# Add a follow-up question
add_user_message(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, final_answer)

print(messages)

# Output:
# [
#     {'role': 'user', 'content': 'Define quantum computing in one sentence'}, 
#     {'role': 'assistant', 'content': 'Quantum computing harnesses quantum mechanical phenomena '
#     'like superposition and entanglement to process information in fundamentally different ways '
#     'than classical computers, potentially solving certain complex problems exponentially faster.'}, 
#     {'role': 'user', 'content': 'Write another sentence'}, 
#     {'role': 'assistant', 'content': 'Unlike classical bits that are either 0 or 1, quantum bits '
#     '(qubits) can exist in multiple states simultaneously, allowing quantum computers to explore '
#     'many possible solutions in parallel.'}
# ]