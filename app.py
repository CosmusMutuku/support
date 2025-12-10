# import gradio as gr
# import os
# from openai import OpenAI
# from mcp_client import call_mcp
# import json  # Add at top if not there
# from dotenv import load_dotenv
# load_dotenv()

# ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# client = OpenAI(base_url=ANTHROPIC_BASE_URL, api_key=ANTHROPIC_API_KEY)

# SYSTEM_PROMPT = """
# You are a Customer Support AI Assistant for a computer products company (monitors, printers, accessories).

# Available MCP Tools:
# 1. search_products - Search products by keyword
#    MCP_CALL: {"action": "search_products", "query": "monitor"}

# 2. list_products - List all products (with optional filters)
#    MCP_CALL: {"action": "list_products"}
#    MCP_CALL: {"action": "list_products", "category": "Monitors"}

# 3. get_product - Get product details by SKU
#    MCP_CALL: {"action": "get_product", "sku": "MON-0054"}

# 4. verify_customer_pin - Verify customer identity (IMPORTANT!)
#    MCP_CALL: {"action": "verify_customer_pin", "email": "customer@example.com", "pin": "1234"}

# 5. list_orders - List orders for a customer
#    MCP_CALL: {"action": "list_orders", "customer_id": "uuid-here"}

# 6. get_order - Get specific order details
#    MCP_CALL: {"action": "get_order", "order_id": "uuid-here"}

# 7. create_order - Create new order
#    MCP_CALL: {"action": "create_order", "customer_id": "uuid", "items": [...]}

# Example interaction:
# Customer: "Hi, I'm donaldgarcia@example.net, PIN 7912. Can you check my orders?"
# You: "Let me verify your account!"
# MCP_CALL: {"action": "verify_customer_pin", "email": "donaldgarcia@example.net", "pin": "7912"}

# After verification, use the customer_id from the response to list their orders:
# MCP_CALL: {"action": "list_orders", "customer_id": "customer-uuid-from-verification"}

# Be brief, helpful, and friendly.
# """

# def chatbot(user_message, chat_history):
#     # Build messages for API call
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         *chat_history,
#         {"role": "user", "content": user_message},
#     ]
    
#     # Run LLM
#     llm = client.chat.completions.create(
#         model="claude-haiku-4-5",  
#         messages=messages,
#         max_tokens=200
#     )

#     reply = llm.choices[0].message.content

#     # Check if LLM requested an MCP action (simple detection)
#     if "MCP_CALL:" in reply:
#         try:
#             json_payload = reply.split("MCP_CALL:")[1].strip()
#             mcp_data = call_mcp(json.loads(json_payload))
#             reply += f"\n\n(MCP Result: {mcp_data})"
#         except Exception as e:
#             reply += f"\n\n[MCP ERROR: {str(e)}]"

#     # Update chat history with message dictionaries
#     chat_history.append({"role": "user", "content": user_message})
#     chat_history.append({"role": "assistant", "content": reply})
    
#     # Return the updated history for display
#     return chat_history, chat_history, ""

# def clear():
#     return [], []

# with gr.Blocks(title="Customer Support Chatbot") as demo:
#     gr.Markdown("# Customer Support Chatbot\nAsk me anything about monitors, printers, and accessories!")

#     chatbot_ui = gr.Chatbot()
#     msg = gr.Textbox(label="Your Message", placeholder="Type your question here...")
#     state = gr.State([])
    
#     with gr.Row():
#         submit_btn = gr.Button("Submit", variant="primary")
#         clear_btn = gr.Button("Clear Chat")

#     submit_btn.click(chatbot, [msg, state], [chatbot_ui, state, msg])
#     msg.submit(chatbot, [msg, state], [chatbot_ui, state, msg])
#     clear_btn.click(clear, None, [chatbot_ui, state])

# demo.launch()


import gradio as gr
import os
import json
from openai import OpenAI
from mcp_client import call_mcp
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = OpenAI(base_url=ANTHROPIC_BASE_URL, api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
You are a Customer Support AI Assistant for a computer products company.

Available MCP Tools (call them when needed):

1. **search_products** - Search by keyword
   MCP_CALL: {"action": "search_products", "query": "4K monitor"}

2. **list_products** - List all products
   MCP_CALL: {"action": "list_products"}

3. **get_product** - Get product by SKU
   MCP_CALL: {"action": "get_product", "sku": "MON-0054"}

4. **verify_customer_pin** - Verify customer identity
   MCP_CALL: {"action": "verify_customer_pin", "email": "customer@email.com", "pin": "1234"}

5. **list_orders** - List customer orders (need customer_id from verification)
   MCP_CALL: {"action": "list_orders", "customer_id": "uuid-here"}

6. **get_order** - Get specific order
   MCP_CALL: {"action": "get_order", "order_id": "uuid-here"}

When a customer provides email and PIN, immediately verify them and then you can look up their orders.

Be brief, helpful, and friendly. Only call tools when you actually need data.
"""

def chatbot(user_message, chat_history):
    # Build messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *chat_history,
        {"role": "user", "content": user_message},
    ]
    
    # Run LLM
    llm = client.chat.completions.create(
        model="claude-haiku-4-5",
        messages=messages,
        max_tokens=500  # Increased for better responses
    )
    
    reply = llm.choices[0].message.content
    print(f"\n🤖 LLM Reply: {reply}\n")  # Debug
    
    # Check for MCP calls
    if "MCP_CALL:" in reply:
        try:
            json_str = reply.split("MCP_CALL:")[1].strip()
            # Clean up any text after the JSON
            if '\n' in json_str:
                json_str = json_str.split('\n')[0]
            
            print(f"📞 Calling MCP with: {json_str}")  # Debug
            
            payload = json.loads(json_str)
            mcp_result = call_mcp(payload)
            
            print(f"✅ MCP Response: {mcp_result}\n")  # Debug
            
            # Extract clean text from MCP response
            if 'content' in mcp_result and len(mcp_result['content']) > 0:
                mcp_text = mcp_result['content'][0].get('text', str(mcp_result))
            else:
                mcp_text = str(mcp_result)
            
            # Remove MCP_CALL from reply and add result
            reply = reply.split("MCP_CALL:")[0].strip()
            reply += f"\n\n{mcp_text}"
            
        except Exception as e:
            print(f"❌ MCP Error: {str(e)}")  # Debug
            reply += f"\n\n[Error: {str(e)}]"
    
    # Update history
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": reply})
    
    return chat_history, chat_history, ""

def clear():
    return [], []

with gr.Blocks(title="Customer Support Chatbot") as demo:
    gr.Markdown("# 🛒 Customer Support Chatbot\nAsk about products, check orders, or get help!")
    
    chatbot_ui = gr.Chatbot()
    msg = gr.Textbox(label="Your Message", placeholder="Try: 'Show me 4K monitors' or 'I'm donaldgarcia@example.net, PIN 7912'")
    state = gr.State([])
    
    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        clear_btn = gr.Button("Clear Chat")
    
    submit_btn.click(chatbot, [msg, state], [chatbot_ui, state, msg])
    msg.submit(chatbot, [msg, state], [chatbot_ui, state, msg])
    clear_btn.click(clear, None, [chatbot_ui, state])

demo.launch()