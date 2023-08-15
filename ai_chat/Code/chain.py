# chain.py

from langchain.chains import LLMChain 
from langchain import PromptTemplate 
from langchain.llms import OpenAI
from prompt import NEW_SYSTEM_PROMPT
from generator_response import generate
from langchain.chat_models import ChatOpenAI

# Set up LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9, max_tokens=175)

# Create prompt template 
prompt = PromptTemplate(input_variables=['max_tokens', 'DATA'], template=NEW_SYSTEM_PROMPT)

# Initialize LLMChain with the callback
chain = LLMChain(llm=llm, prompt=prompt)

# Run chain
def run_chain(hits, query):
    # Generate response
    response = generate(hits, query)
    return response
