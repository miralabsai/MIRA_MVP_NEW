from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_agent import RouterAgent
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from logger import setup_logger  # Import the logger setup function

# Set up the logger
logger = setup_logger('main_logger', 'main.log')

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change this to your front-end domain in production
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
        logger.error(f"Error generating response: {str(e)}")  # Log the error
        response = "Sorry, something went wrong. Please try again later."
    return response

logger.info(f"Current working directory: {os.getcwd()}")  # Log the current directory

class ConverseRequest(BaseModel):
    query: str

@app.post("/converse")
async def converse(query: str):
    response = generate_response(query)
    return {"response": response}
