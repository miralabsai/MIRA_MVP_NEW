from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_agent import RouterAgent
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from logger import setup_logger  # Import the logger setup function
import uvicorn

# Define the log directory relative to the project root
log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
log_file_path = os.path.join(log_directory, 'main_logger.log')

# Ensure the directory exists
os.makedirs(log_directory, exist_ok=True)

# Set up the logger
logger = setup_logger('main_logger', log_file_path)

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
async def converse(query: ConverseRequest):  # Note the type change here
    logger.info(f"Received query: {query.query}")  # Log the received query
    try:
        response = generate_response(query.query)  # Extracting the query from the request object
        logger.info(f"Generated response: {response}")  # Log the generated response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")  # Log any exceptions
        response = "Sorry, something went wrong. Please try again later."

    return {"response": response}

 # at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)