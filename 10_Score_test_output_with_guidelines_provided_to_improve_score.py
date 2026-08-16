import os
import json
from dotenv import load_dotenv
import anthropic
from params import MODEL_NAME

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


# --------------------------------------------------
# Matured PROMPT
# --------------------------------------------------

def run_prompt(text):
    prompt = f"""
    Summarize the customer review using these guidelines:

    1. Identify the main positive points.
    2. Identify the main negative points.
    3. Identify the customer's overall sentiment.
    4. Do not add information that is not present in the review.
    5. Keep the response concise.
    6. Use exactly this format:

    Positive:
    - point 1
    - point 2

    Negative:
    - point 1
    - point 2

    Overall sentiment:
    - Positive / Neutral / Negative / Mixed
    - One sentence explaining why

    Customer review:
    {text}
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=150,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text


# --------------------------------------------------
# EVALUATOR
# --------------------------------------------------

def grade_output(text, output):

    evaluator_prompt = f"""
    Evaluate the quality of the AI summary.

    Original customer review:
    {text}

    AI summary:
    {output}

    Evaluate these 4 criteria:

    1. POSITIVE POINTS
       Does the summary clearly mention the important positive points?

    2. NEGATIVE POINTS
       Does the summary clearly mention the important negative points?

    3. OVERALL SENTIMENT
       Does the summary clearly communicate whether the customer is
       positive, negative, or mixed overall?

    4. READABILITY
       Is the summary clear, concise, and easy to understand?

    Scoring:

    10 = All 4 criteria are clearly satisfied.
    8-9 = Almost all criteria are satisfied.
    6-7 = Most important information is present, but some criteria are weak.
    4-5 = Some information is present, but important points are missing.
    2-3 = Very incomplete summary.
    1 = Almost completely fails to summarize the review.

    Return ONLY the score as a number from 1 to 10.
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


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

test_cases = [
    "The phone has a very good camera and the battery lasts all day. "
    "The display is also excellent. However, the phone gets quite hot "
    "while gaming and sometimes the apps become slow. Overall, I like "
    "the phone but I think it is slightly overpriced."
]


# --------------------------------------------------
# RUN EVALUATION
# --------------------------------------------------

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

# Output
# [
#   {
#     "input": "The phone has a very good camera and the battery lasts all day. The display is also excellent. However, the phone gets quite hot while gaming and sometimes the apps become slow. Overall, I like the phone but I think it is slightly overpriced.",
#     "output": "Positive:\n- Very good camera\n- Battery lasts all day\n- Excellent display\n\n"
#     "Negative:\n- Phone gets hot while gaming\n- Apps sometimes become slow\n- "
#     "Slightly overpriced\n\nOverall sentiment:\n- "
#     "Mixed\n- The customer appreciates the phone's key features but has concerns about "
#     "performance issues and pricing.",
#     "score": 10
#   }
# ]
# Average Score: 10.0