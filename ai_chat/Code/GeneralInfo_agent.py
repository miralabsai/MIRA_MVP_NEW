# general_info_agent.py

from retriever import retrieve_by_intent_and_entities
from chain import run_chain
from logger import setup_logger
import logging

# Set up the logger
logger = setup_logger('general_info_agent', level=logging.INFO)

class GeneralInfoAgent:
    # Modified to accept intents and entities
    def func(self, query, intents, entities):
        try:
            # Retrieve the most relevant chunks based on intents and entities
            hits = retrieve_by_intent_and_entities(intents, entities, k=2)
        
            # Generate a response using the run_chain function
            response = run_chain(hits, query)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            response = "Sorry, something went wrong. Please try again later."
        
        return response

