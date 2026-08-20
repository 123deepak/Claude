import os
from dotenv import load_dotenv
import anthropic
from params import MODEL_NAME


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

company_policy = """
Customers can return products within 30 days.
Refunds are processed within 7 business days.
Warranty is valid for 1 year.
Digital products are non-refundable.
""" * 100

def chat(user_question):

    message = client.messages.create(

        model=MODEL_NAME,

        max_tokens=500,

        system=[
            {
                "type": "text",
                "text": company_policy,

                # Tell Claude to cache this content
                "cache_control": {
                    "type": "ephemeral"
                }
            }
        ],

        messages=[
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    return message


response = chat("What is the refund policy?")

print(response)

# With caching, first trigger (1:02)
# Message(id='msg_011CeEZBf7ekjtMw5Gd4Rwbs', container=None, content=[TextBlock(citations=None, text="# Refund Policy\n\nBased on the information provided:\n\n- **Return Window:** Customers can return products within **30 days**\n- **Refund Processing:** Refunds are processed within **7 business days**\n- **Warranty:** Valid for **1 year**\n- **Digital Products:** **Non-refundable**\n\nIs there anything specific about the refund policy you'd like to know more about?", type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=4602), cache_creation_input_tokens=4602, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=12, output_tokens=96, output_tokens_details=None, server_tool_use=None, service_tier='standard'))
# With caching, Second trigger (1:03)
# Message(id='msg_011CeEZKMcfNxAR462CpRMc5', container=None, content=[TextBlock(citations=None, text="# Refund Policy\n\nBased on the information provided:\n\n- **Return Window:** Customers can return products within **30 days**\n- **Refund Processing:** Refunds are processed within **7 business days**\n- **Warranty:** Valid for **1 year**\n- **Digital Products:** **Non-refundable**\n\nIs there anything specific about the refund policy you'd like to know more about?", type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=4602, inference_geo='not_available', input_tokens=12, output_tokens=96, output_tokens_details=None, server_tool_use=None, service_tier='standard')
# With caching, Second trigger (1:04)
# Message(id='msg_011CeEZVpKnwLyEfQqvBZSuy', container=None, content=[TextBlock(citations=None, text='# Refund Policy\n\nBased on the information provided:\n\n- **Return Window**: Customers can return products within **30 days**\n- **Refund Processing Time**: Refunds are processed within **7 business days**\n- **Warranty**: Valid for **1 year**\n- **Digital Products**: **Non-refundable**\n\nIf you have any specific questions about a particular product or situation, ', type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=4602, inference_geo='not_available', input_tokens=12, output_tokens=98, output_tokens_details=None, server_tool_use=None, service_tier='standard'))
# With caching, Second trigger (1:11) [Notice it cached again, as previous cache was valid for 5 mins]
# Message(id='msg_011CeEa4EwXD1ffAPLDggEwh', container=None, content=[TextBlock(citations=None, text='# Refund Policy\n\nBased on the information provided, here are the key details:\n\n- **Return Window**: Customers can return products within **30 days**\n- **Refund Processing**: Refunds are processed within **7 business days**\n- **Warranty**: Valid for **1 year**\n- **Digital Products**: **Non-refundable**\n\nIf or need more specific details, please let me   know!', type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=4602), cache_creation_input_tokens=4602, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=12, output_tokens=107, output_tokens_details=None, server_tool_use=None, service_tier='standard'))