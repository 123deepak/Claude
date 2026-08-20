# Load env variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

# Helper functions
from anthropic.types import Message

# Magic string to trigger redacted thinking
thinking_test_str = "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"

def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    params = {
        "model": model,
        "max_tokens": 2000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])

messages = []

add_user_message(messages, "Can we fit one refrigrator in a washing machine?")

print(chat(messages, thinking=True))
print("\n\n\n-----------------------\n\n\n")
messages = []

add_user_message(messages, thinking_test_str)

print(chat(messages, thinking=True))


# Message(id='msg_011CeEUe9ZpJbPvEGD2Kqh7f', container=None, content=
#   [ThinkingBlock(signature='EpMICpsBCBAYAipAOH49Em+kGmkh+wryaFZb/b6h+JCYPzV/jieUF+2b9S9AZg3GHwceg3n9xP+DpK7EBFVjt1XGjJMSFIAgvRsIaTIaY2xhdWRlLXNvbm5ldC00LTUtMjAyNTA5Mjk4AEIIdGhpbmtpbmdaJDNhNWM1MDFhLTAzZmItNDA5Yi05YjZkLWY4NWM5MDlhMGNlOagB8o+d1AYSDJ95eTWtIGD7AwAS5BoMphOFf33CFw8EJZA/IjAxdSCodwd0G7fdPLf8w1zDWfoQsvxkeZDxW74aTScD9qQjPVI+Vhf+IbMIp+8WKHAqpAb9ofUHYdBnssMXzUHAEKOStOWH69eBEoiFes1PvNmGCp04frmPeeMHsgbxUWlWwKt1vcrLTAgGiRXAxD5LBEuEUdLzh5iAU/PpiBRz9toof6VOd75sZ0rEJc7xmums+Yf1yTVvImkdjEZ5LoMcYEpfLesyI6ulw7Io1ZzA6z9KXIl8a6mrGX1larFU8H8XU1eewKJiX+WnvpkWtK6RyGKtmNLMD4jm9QmvMcNVzZndpRdURuKS1GO5bbid6qVK53hCuYLXLFF/+pNCEDUONLpfKLAaFg0tMhZPzMUZCHbR/QM5iiSwWeftpFqiHplLhXKMRMlbtiTti/jIFQrS+bE+QzNbhHFmke1srkt/pAA0jWbY/tdb33HEqm468X8ZhFlqDHDkdBFjQdBJqrjCOcX+Yh5TU8RsLTNk8WmQ2fi5CTFiIhJ6Bk5evURALoiOrok4zhmmDnbEvkJE9NdmnxwV4bVwY6Vw17BMcvJwrlze9loefVlyRxDcOpzApStAXNt1GtTqaX2VZMTo4fR7pQ+gm4aevPDHverz2hg4SUHO44swiq6FzkVCP/HgqES0RcFYAQRZ1qcC2zC0TRbQw1j5zLj/UDJGG44i58moA62CL1yW7brGr/ibfhBFQWdXeJbGDtJ4x+/+fnrab7UXqOCujM/8ciNESJhJNdzBIXyS3FdBtvx3CZweXbj/AYvR71Jpe8q8YcKZtabtXcTR2mIPWsgL70GrNFWXFX/G2G7a7Fsfyyl1t2HRF557N9o2fwT3gIyTVjVZnospgYlqLjTj8KLRm+W55y+1FMRUuP/3FhNQSOfYbGbWwLGE1tje4B5QCsijxlcLDlthgtSLbPgX9ScFbdSnfoSRJrqXYwG4lw/SXVKHDVzDhbWNV9nYHYaRnE4zrZ46KhnRLgW8mOTbL9phFmusdSM9m2eIcyrFp0k7SEnMEhI3ruex7c5npxaGOr6XKGh6USJjeXOcC+Yuw9meKVIi9/b+gI8K24GH5AptdfGYs35Ji3+sN9m6Diq5nnuLQS/zYbNR60KtOUE/MJckJVHnc/F7pHi2Blpgl3d2pAUYAQ==', 
#   thinking="This is a straightforward question about whether a refrigerator can fit inside a washing machine. 
#   \n\nLet me think about the typical sizes:\n- A standard refrigerator is much larger than a washing machine - 
#   typically 5-6 feet tall and 2-3 feet wide\n- A washing machine is much smaller - typically about 2-3 feet tall 
#   and 2 feet wide/deep\n\nSo no, you definitely cannot fit a refrigerator inside a washing machine. 
#   The refrigerator is significantly larger in all dimensions.\n\nThis seems like it might be:\n1. 
#   A genuine question from someone who doesn't know the relative sizes\n2. A test question to see if I give a 
#   sensible answer\n3. Perhaps they meant to ask the reverse (can a washing machine fit in a refrigerator? - 
#   also no, but closer in size)\n\nI'll give a straightforward, helpful answer.", type='thinking'), 
#   
#   TextBlock(citations=None, text="No, you cannot fit a refrigerator in a washing machine. \n\nRefrigerators 
#   are much larger than washing machines:\n- **Refrigerators** are typically 5-6 feet tall (150-180 cm) and 
#   2-3 feet wide (60-90 cm)\n- **Washing machines** are typically 2-3 feet tall (60-90 cm) and about 2 feet wide 
#   (60 cm)\n\nThe refrigerator is significantly bigger in every dimension, so it won't fit inside a washing 
#   machine.\n\nDid you perhaps mean to ask the opposite - whether a washing machine could fit in a refrigerator? 
#   (It still wouldn't, but they're closer in size.) Or were you asking about something else?", type='text')], 
#   model='claude-sonnet-4-5-20250929', role='assistant', stop_details=None, 
#   stop_reason='end_turn', stop_sequence=None, type='message', 
#   usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), 
#   cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', 
#   input_tokens=47, output_tokens=371, output_tokens_details=OutputTokensDetails(thinking_tokens=199), 
#   server_tool_use=None, service_tier='standard'))
# -----------------------
# Message(id='msg_011CeEUegvxdXsCUQk589qBN', container=None, content=[RedactedThinkingBlock(data='EoQECpsBCBAYAipAC9lPimkWW8dl1az+csCO0ndEKJVZueeUvg/xjhd40aV6ql5A1NB1znMtW4GLQ8Pn/qdmCeiwbAQcq2LNCpLf+TIaY2xhdWRlLXNvbm5ldC00LTUtMjAyNTA5Mjk4AEIIdGhpbmtpbmdaJDNhNWM1MDFhLTAzZmItNDA5Yi05YjZkLWY4NWM5MDlhMGNlOagB94+d1AYSDNWC4QRQhyM06gOXVRoM48/zH62HrrAIdKpqIjAo769lqZ3t+T+672ick+n1METewx9mRUEoNjyScA1QLC2pAlr4pazKP7W0SgU95lAqlQKPWyzfjMqQf7uwZG4XwHpLPir/g2QDmr0E4HfAbfyfumBvybEQubd6Z6CUPKbFG/OdvvKLQnmLTKZ+/o90fkvRy2E7wRcfIgp9RT7UtFuBsDLFwH6R1QTrxDL89axbfQ8bsDgJvsrKDGclUTrJQ7pZZzHYUrvBOFeikfB4g26Qqw2u5vcC1/wsDIOnlDRyvwc863JelpTdXRn8SWVstGiTZPbDM17kU8L2ujijEuFVB0xLTbFErqPuM5aAXwQBx3U4hJ8kUjGqkkN4nVgvKkDvSHk3PiuiJJ1kDBPCNp5mUEIbl/qrDtorafBO/s+2H89g82KPtlLRn10l5l0k94ySUMc5rD7n8H7CN15LFiDKl11CV5kNGAE=', type='redacted_thinking'), TextBlock(citations=None, text="I don't have any special response to that string. It appears to be a test or trigger phrase, but I don't have any hidden modes or special functionality that activates from particular strings.\n\nIs there something I can help you with today?", type='text')], model='claude-sonnet-4-5-20250929', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=93, output_tokens=113, output_tokens_details=OutputTokensDetails(thinking_tokens=57), server_tool_use=None, service_tier='standard'))