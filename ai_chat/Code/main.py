from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nlu_router import RouterAgent
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from logger import setup_logger
import uvicorn
import logging  # Added import for logging

# Set up the logger with the correct level
logger = setup_logger('main_logger', level=logging.INFO)

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
        response, confidence = router.route(message)  # This line changes to capture both response and confidence
        logger.info(f"Generated response: {response}, Confidence: {confidence}")  # Log the generated response and confidence
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")  # Log the error
        response = "Sorry, something went wrong. Please try again later."
    return response  # This remains the same, but you could also return confidence if needed

logger.info(f"Current working directory: {os.getcwd()}")  # Log the current directory

class ConverseRequest(BaseModel):
    query: str

@app.post("/converse")
async def converse(query: ConverseRequest):  # Note the type change here
    logger.info(f"Received query: {query.query}")  # Log the received query
    response = generate_response(query.query)  # Extracting the query from the request object

    return {"response": response}

# at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
