import os
from dotenv import load_dotenv
import openai
# Assume generate_prompt is imported or defined here
from logger import setup_logger
import logging
from prompt import generate_prompt

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate OpenAI API Key
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is not set.")
else:
    # Set OpenAI API key
    openai.api_key = OPENAI_API_KEY

# Set up the logger
logger = setup_logger('generator_response', level=logging.INFO)

def generate(chunks, query):
    # Validate and generate prompt
    prompt = generate_prompt(chunks, query)  # Using the imported function
    return "System Prompt: " + ", ".join(chunks) + " Query: " + query

def generate(chunks, query):
    # Validate and generate prompt
    prompt = generate_prompt(chunks, query)
    if not prompt:
        logger.error("Prompt generation failed.")
        return None
    
    logger.info(f"Generated prompt applied NEW_SYSTEM_PROMPT")
    
    try:
        # Generate response using the chat models endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=175,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        
        # Log the token usage
        token_count = response['usage']['total_tokens']
        logger.info(f"Total tokens used: {token_count}")
        
        # Validate the response format
        if 'choices' in response and 'message' in response['choices'][0] and 'content' in response['choices'][0]['message']:
            response_text = response['choices'][0]['message']['content']
            logger.info(f"Generated response: {response_text}")
        else:
            logger.error("Unexpected response format.")
            response_text = None
            
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        response_text = None

    return response_text


