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

# --------------------------------------------------
# Tool definitions
# --------------------------------------------------

tools = [

    {
        "name": "get_product_price",
        "description": "Get the price of a product in USD.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "string",
                    "description": "Name of the product"
                }
            },
            "required": ["product"]
        }
    },

    {
        "name": "get_exchange_rate",
        "description": "Get the current exchange rate between two currencies.",
        "input_schema": {
            "type": "object",
            "properties": {
                "from_currency": {
                    "type": "string",
                    "description": "Currency to convert from"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Currency to convert to"
                }
            },
            "required": ["from_currency", "to_currency"]
        }
    }
]


# --------------------------------------------------
# Tool implementations
# --------------------------------------------------
def get_product_price(product):
    # Simulated database/API
    prices = {
        "laptop": 1000,
        "macbook": 1500,
        "iphone": 800
    }
    return prices.get(product.lower(), 500)


def get_exchange_rate(from_currency, to_currency):

    # Simulated exchange-rate API
    if from_currency == "USD" and to_currency == "INR":
        return 85

    return 1


# --------------------------------------------------
# Main
# --------------------------------------------------

messages = []

add_user_message(
    messages,
    "I want to buy 3 laptops. What will the total cost be in INR?"
)

# --------------------------------------------------
# Keep talking to Claude until task is complete
# --------------------------------------------------

while True:

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # --------------------------------------------------
    # Claude has finished the task
    # --------------------------------------------------

    if response.stop_reason != "tool_use":
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    # --------------------------------------------------
    # Claude wants to use one or more tools
    # --------------------------------------------------
    add_assistant_message(
        messages,
        response.content
    )

    tool_results = []

    for block in response.content:
        if block.type != "tool_use":
            continue

        print("Tool call:", block.name)
        print("Input:", block.input)

        # --------------------------------------------------
        # Tool A
        # --------------------------------------------------

        if block.name == "get_product_price":
            product = block.input["product"]
            result = get_product_price(product)

        # --------------------------------------------------
        # Tool B
        # --------------------------------------------------

        elif block.name == "get_exchange_rate":
            from_currency = block.input["from_currency"]
            to_currency = block.input["to_currency"]
            result = get_exchange_rate(
                from_currency,
                to_currency
            )

        else:

            result = "Unknown tool"
        print("Tool result:", result)

        # --------------------------------------------------
        # Store tool result
        # --------------------------------------------------

        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result)
        })

    # --------------------------------------------------
    # Send tool results back to Claude
    # --------------------------------------------------

    messages.append({
        "role": "user",
        "content": tool_results
    })

print(messages)

# Output:
# Tool call: get_product_price
# Input: {'product': 'laptop'}
# Tool result: 1000
# Tool call: get_exchange_rate
# Input: {'from_currency': 'USD', 'to_currency': 'INR'}
# Tool result: 85
# Perfect! Here's the calculation:

# - **Price per laptop:** $1,000 USD
# - **Exchange rate:** 1 USD = 85 INR
# - **Number of laptops:** 3

# **Total cost calculation:**
# - 3 laptops × $1,000 = $3,000 USD
# - $3,000 USD × 85 INR/USD = **₹2,55,000 INR**

# So, the total cost for 3 laptops will be **₹2,55,000 (Two Lakh Fifty-Five Thousand Indian Rupees)**.
# [{'role': 'user', 'content': 'I want to buy 3 laptops. What will the total cost be in INR?'}, 
#  {'role': 'assistant', 'content': 
#       [TextBlock(citations=None, text="I'll help you find the cost of 3 laptops in INR. 
#                   Let me first get the price of a laptop in USD and then convert it to INR.", type='text'), 
#        ToolUseBlock(id='toolu_019BAaUeTqvzBZJHu6ZxYCNT', caller=DirectCaller(type='direct'), 
#                   input={'product': 'laptop'}, name='get_product_price', type='tool_use'), 
#        ToolUseBlock(id='toolu_018wVqDJvpm6UpuV9G2hmwYt', caller=DirectCaller(type='direct'), 
#                   input={'from_currency': 'USD', 'to_currency': 'INR'}, name='get_exchange_rate', type='tool_use')]}, 
#  {'role': 'user', 'content': 
#   [{'type': 'tool_result', 'tool_use_id': 'toolu_019BAaUeTqvzBZJHu6ZxYCNT', 'content': '1000'}, 
#    {'type': 'tool_result', 'tool_use_id': 'toolu_018wVqDJvpm6UpuV9G2hmwYt', 'content': '85'}]
# }]