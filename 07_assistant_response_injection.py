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
add_user_message(messages, "What is the Capital of India")

# Add Claude's response to the conversation history
add_assistant_message(messages, "Capital of India is Pune")

# Add a follow-up question
add_user_message(messages, "No, it is incorrect")

# Get the follow-up response with full context
final_answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, final_answer)

print(messages)

# Output
# [
#     {'role': 'user', 'content': 'What is the Capital of India'}, 
#     {'role': 'assistant', 'content': 'Capital of India is Pune'}, 
#     {'role': 'user', 'content': 'No, it is incorrect'}, 
#     {'role': 'assistant', 'content': "You're absolutely right, I apologize for the error. 
#         The capital of India is **New Delhi**.\n\nNew Delhi is the capital city and 
#         serves as the seat of the Indian government. Thank you for the correction!"}
# ]
