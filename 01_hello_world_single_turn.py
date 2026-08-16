import os
from dotenv import load_dotenv
import anthropic
from params import MODEL_NAME

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

try:
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=10,
        messages=[
            {"role": "user", "content": "Say Hello in 3 words"}
        ]
    )

    print(message.content[0].text)

except Exception as e:
    print(f"Error: {e}")


# Output
# Hello, world friend
