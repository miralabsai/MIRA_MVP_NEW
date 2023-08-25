# generator_response.py

import os
from dotenv import load_dotenv
import openai
from prompt import generate_prompt
from logger import setup_logger
import logging

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up the logger
logger = setup_logger('generator_response', level=logging.INFO)

def generate(chunks, query):
    # Generate prompt
    prompt = generate_prompt(chunks, query)
    logger.info(f"Generated prompt: {prompt}")

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
        response_text = response['choices'][0]['message']['content']
        logger.info(f"Generated response: {response_text}")
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        response_text = None

    return response_text
