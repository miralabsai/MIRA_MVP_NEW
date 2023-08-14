#generator_response.py

import os
from dotenv import load_dotenv
import openai
from prompt import generate_prompt

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def generate(chunks, query):
    # Generate prompt
    prompt = generate_prompt(chunks, query)

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
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        response_text = None

    return response_text
