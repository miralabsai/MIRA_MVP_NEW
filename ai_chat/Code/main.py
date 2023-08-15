from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_agent import RouterAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/dashboard/chat-ui"],  # Change this to your front-end domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pass the handler to the RouterAgent
router = RouterAgent()

def generate_response(message, history=[]):
    try:
        response = router.route(message)  # Directly route message through RouterAgent
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        response = "Sorry, something went wrong. Please try again later."
    return response

@app.post("/converse")
async def converse(query: str):
    response = generate_response(query)
    return {"response": response}
