import os
import json
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


def chat(message):
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=200,
        temperature=0,
        messages=message,
        stop_sequences=["```"]
    )

    return response.content[0].text


def syntax_score(output):
    try:
        json.loads(output)
        return 10
    except:
        return 0


def quality_score(output):
    evaluator_prompt = f"""
        Evaluate this answer.

        Expected answer:
        {{
            "name": "John",
            "age": 25
        }}

        Actual answer:
        {output}

        Give a score from 0 to 10 and check if actual answer is as per expectation.
        Return ONLY the number.
    """

    messages = []
    add_user_message(messages, evaluator_prompt)

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=20,
        temperature=0,
        messages=messages
    )

    return int(response.content[0].text.strip())


prompt = """
    Extract the person's name and age.

    Return ONLY valid JSON.

    Text:
    John is 25 years old.
"""

messages = []
add_user_message(messages, prompt)
add_assistant_message(messages, "```json")

output = chat(messages)

syntax = syntax_score(output)
quality = quality_score(output)
final_score = (syntax + quality) / 2

print("MODEL OUTPUT:")
print(output)

print("SYNTAX SCORE:", syntax)
print("QUALITY SCORE:", quality)
print("FINAL SCORE:", final_score)

# Output:
# MODEL OUTPUT:

# {
#   "name": "John",
#   "age": 25
# }

# SYNTAX SCORE: 10
# QUALITY SCORE: 10
# FINAL SCORE: 10.0
