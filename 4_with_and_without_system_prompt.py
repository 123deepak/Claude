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

def chat(messages, system_prompt = None):

    params = {
        "model": MODEL_NAME,
        "max_tokens": 200,
        "messages": messages
    }
    if system_prompt:
        params["system"] = system_prompt

    message = client.messages.create(
        **params
    )
    return message.content[0].text

query = "How do I solve: If 5x + 2 = 5, find value of x? Answer in 50 words."
messages = []

add_user_message(messages, query)

# Without system prompt
answer = chat(messages)
print("Without system Prompt: ", answer)

# With system prompt
sprompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system_prompt=sprompt)
print("With system Prompt: ", answer)

# Without system Prompt:  
# # Solving 5x + 2 = 5
# **Step 1:** Subtract 2 from both sides
# - 5x + 2 - 2 = 5 - 2
# - 5x = 3
# **Step 2:** Divide both sides by 5
# - x = 3/5 or 0.6
# **Answer: x = 3/5 (or 0.6)**

# With system Prompt:  # Let's work through this together!
# **Step 1:** Look at your equation: 5x + 2 = 5
# **Step 2:** What's on the left side with x? (The 2 is extra!)
# **Step 3:** How can you remove the 2 from the left side? (Hint: use opposite operations)
# **Step 4:** Do the same operation to both sides to keep it balanced.
# **Step 5:** Now solve for x!
# What do you get?