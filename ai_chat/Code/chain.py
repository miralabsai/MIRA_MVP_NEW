# chain.py
from langchain.chains import LLMChain 
from langchain import PromptTemplate 
from langchain.llms import OpenAI
from prompt import NEW_SYSTEM_PROMPT
from generator_response import generate
from langchain.chat_models import ChatOpenAI
from logger import setup_logger
import logging

# Set up the logger
logger = setup_logger('chain', level=logging.INFO)

# Set up LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9, max_tokens=175)
logger.info("LLM setup completed")

# Create prompt template 
prompt = PromptTemplate(input_variables=['max_tokens', 'DATA'], template=NEW_SYSTEM_PROMPT)
logger.info("Prompt template created")

# Initialize LLMChain with the callback
chain = LLMChain(llm=llm, prompt=prompt)
logger.info("LLMChain initialized")

# Run chain
def run_chain(hits, query):
    try:
        # Log the input data
        logger.info(f"Running chain with hits: {hits}, query: {query}")

        # Generate response
        response = generate(hits, query)

        return response
    except Exception as e:
        logger.error(f"Error in running chain: {str(e)}")
        return None
