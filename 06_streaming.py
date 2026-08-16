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

messages = []
add_user_message(messages, "Write a 500 words description of a fake database")

with client.messages.stream(
    model=MODEL_NAME,
    max_tokens=300,
    messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="")

# Get the complete message for database storage
# with client.messages.stream(
#     model=model,
#     max_tokens=1000,
#     messages=messages
# ) as stream:
#     for text in stream.text_stream:
#         # Send each chunk to your client
#         pass

#     final_message = stream.get_final_message()
