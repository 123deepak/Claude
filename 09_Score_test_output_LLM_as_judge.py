import os
import json
from dotenv import load_dotenv
import anthropic
from params import MODEL_NAME

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def run_prompt(text):
    prompt = f"""
    Summarize the following text in one sentence:

    {text}
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=100,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text


def grade_output(text, output):
    evaluator_prompt = f"""
    Evaluate the AI's summary.

    Original text:
    {text}

    AI summary:
    {output}

    Give a score from 1 to 10.

    10 = accurate and captures the main point
    5 = partially correct
    1 = incorrect

    Return ONLY the number.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=10,
        temperature=0,
        messages=[
            {"role": "user", "content": evaluator_prompt}
        ]
    )

    return int(response.content[0].text.strip())


test_cases = [
    "Python is a programming language commonly used for data science.",
    "The Earth revolves around the Sun once every year.",
    "Machine learning allows computers to learn patterns from data."
]


results = []

for text in test_cases:

    output = run_prompt(text)
    score = grade_output(text, output)

    results.append({
        "input": text,
        "output": output,
        "score": score
    })


average_score = sum(r["score"] for r in results) / len(results)

print(json.dumps(results, indent=2))
print("Average Score:", average_score)

# Output:
# [
#   {
#     "input": "Python is a programming language commonly used for data science.",
#     "output": "Python is a programming language widely used in data science.",
#     "score": 9
#   },
#   {
#     "input": "The Earth revolves around the Sun once every year.",
#     "output": "The Earth completes one full orbit around the Sun annually.",
#     "score": 10
#   },
#   {
#     "input": "Machine learning allows computers to learn patterns from data.",
#     "output": "Machine learning enables computers to automatically identify and learn patterns from data without being explicitly programmed.",
#     "score": 8
#   }
# ]
# Average Score: 9.0
