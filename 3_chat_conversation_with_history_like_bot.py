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

messages = []

while True:
	user_input = input("> ")
	# print(">", user_input)

	add_user_message(messages, user_input)
	answer = chat(messages)
	add_assistant_message(messages, answer)
	print("------")
	print(answer)
	print("------")

# Output
# > what is 10 + 30
# ------
# 10 + 30 = **40**
# ------
# > add 60 to it
# ------
# 40 + 60 = **100**
# ------