import os
import json
from dotenv import load_dotenv
import anthropic
from params import MODEL_NAME

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


# --------------------------------------------------
# NAIVE PROMPT
# --------------------------------------------------

def run_prompt(text):

    prompt = f"""
    Classify the sentiment as Positive, Negative, or Mixed.

    Examples:

    Review:
    "The camera is excellent and the battery lasts all day."
    Sentiment: Positive

    Review:
    "The phone is slow and the battery dies very quickly."
    Sentiment: Negative

    Review:
    "The camera is great, but the phone gets hot and the battery is poor."
    Sentiment: Mixed

    Now classify this review:

    Review:
    {text}

    Just provide sentiment as output and no other explanation
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=20,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text.strip()

# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

test_cases = [
    "The phone has a very good camera and the battery lasts all day. "
    "The display is also excellent. However, the phone gets quite hot "
    "while gaming and sometimes the apps become slow. Overall, I like "
    "the phone but I think it is slightly overpriced."
]

results = []

for text in test_cases:

    output = run_prompt(text)

    results.append({
        "input": text,
        "output": output,
    })

print(results)

# Output (without saying: "Just provide sentiment as output and no other explanation")
# [{'input': 'The phone has a very good camera and the battery lasts all day. 
#   The display is also excellent. However, the phone gets quite hot while gaming and sometimes the 
#   apps become slow. Overall, I like the phone but I think it is slightly overpriced.', 
#   'output': 'Sentiment: Mixed\n\n**
#              Reasoning:** The review contains both positive and negative elements:\n-
#              '
#   }]

# Output (with saying: "Just provide sentiment as output and no other explanation")
# [{'input': 'The phone has a very good camera and the battery lasts all day. The display is also excellent. '
#             'However, the phone gets quite hot while gaming and sometimes the apps become slow. '
#             'Overall, I like the phone but I think it is slightly overpriced.', 

#   'output': 'Mixed'
# }]