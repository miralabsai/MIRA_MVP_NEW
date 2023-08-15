import os
import chainlit as cl 
from dotenv import load_dotenv
from router_agent import RouterAgent

# Load environment variables
load_dotenv()

# Pass the handler to the RouterAgent
router = RouterAgent()

def generate_response(message, history=[]):
    try:
        response = router.route(message)  # Directly route message through RouterAgent
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        response = "Sorry, something went wrong. Please try again later."
    return response

@cl.on_message
async def main(message: str):
    response = generate_response(message)
    await cl.Message(content=response).send()
