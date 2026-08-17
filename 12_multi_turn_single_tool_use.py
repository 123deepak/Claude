import os
import anthropic
from dotenv import load_dotenv

MODEL_NAME = "claude-haiku-4-5-20251001"
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def add_user_message(messages, content):
    messages.append({
        "role": "user",
        "content": content
    })

def add_assistant_message(messages, content):
    messages.append({
        "role": "assistant",
        "content": content
    })

# -----------------------------
# Tool definition
# -----------------------------

tools = [
    {
        "name": "add_numbers",
        "description": "Add two numbers together.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    }
]

# -----------------------------
# Tool implementation
# -----------------------------
def add_numbers(a, b):
    return a + b

# -----------------------------
# Main
# -----------------------------
messages = []

add_user_message(
    messages,
    "What is 25 + 17?"
)

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# -----------------------------
# Handle Claude's response
# -----------------------------
if response.stop_reason == "tool_use":

    # Add Claude's response to conversation
    add_assistant_message(
        messages,
        response.content
    )

    # Find the tool Claude wants to use
    tool_call = None

    for block in response.content:
        if block.type == "tool_use":
            tool_call = block
            break

    print("tool call",tool_call)

    # Execute the tool
    if tool_call.name == "add_numbers":

        a = tool_call.input["a"]
        b = tool_call.input["b"]

        result = add_numbers(a, b)

    else:
        result = "Unknown tool"

    # Send tool result back to Claude
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": str(result)
            }
        ]
    })

    # Ask Claude for final response
    final_response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Print final answer
    for block in final_response.content:
        if block.type == "text":
            print(block.text)
else:

    for block in response.content:
        if block.type == "text":
            print(block.text)

# Output
# tool call ToolUseBlock(id='toolu_01Y6QCxF3jen1bvhe8Re8ZJA', caller=DirectCaller(type='direct'), input={'a': 25, 'b': 17}, name='add_numbers', type='tool_use')
# The result of 25 + 17 is **42**.