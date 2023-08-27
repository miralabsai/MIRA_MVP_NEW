# custom_router.py
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from nlu_agent import agent_executor as nlu_agent_executor, extract_from_response, calculate_confidence  # Import from nlu_agent
from GeneralInfo_agent import GeneralInfoAgent  # Import GeneralInfoAgent
from database_prep import DatabaseManager  # Import DatabaseManager
import logging
from logger import setup_logger
import os
import openai
import json


# 1. Specialist agent functions
def eligibility_process(query, entities):
    return "You asked about eligibility. We usually consider factors like income, credit score, etc."

def docs_process(query, entities):
    return "For a mortgage, you would typically need documents like proof of income, credit history, etc."

def followup_process(query, entities):
    return "Is there anything else you'd like to know?"

def app_process(query, entities):
    return "To apply, please fill out the application form on our website."

def doc_process(query, entities):
    return "Please upload your documents through our secure portal."

# 2. Initialize Tools with Specialist Agent Functions
eligibility_agent = Tool(name="Eligibility Agent", func=eligibility_process, description="Handles eligibility queries")
docs_agent = Tool(name="Docs Agent", func=docs_process, description="Handles document queries")
followup_agent = Tool(name="Followup Agent", func=followup_process, description="Handles follow-up actions")
app_agent = Tool(name="App Agent", func=app_process, description="Guides through the application process")
doc_agent = Tool(name="Doc Agent", func=doc_process, description="Handles document submission and review")

# Set up the logger
logger = setup_logger('router_agent', level=logging.INFO)

# Load environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
logger.info("OpenAI initialized with API key.")

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

# Define the PromptTemplate with input variables
class CustomRouterPrompt(StringPromptTemplate):
    template: str
    input_variables: List[str] = ['user_query', 'intents', 'entities']
    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

router_prompt = CustomRouterPrompt(template=f"""
# Custom Router Prompt
C: Context
-----------
You are the Router Agent, responsible for directing incoming user queries to one of the six specialist agents: GeneralInfo, Eligibility, Docs, Followup, App, or DocReview. Your role is crucial in ensuring that the user gets the most accurate and relevant information.

A: Action
----------
Based on the user query, along with its detected intents and entities, identify the specialist agent best suited to answer the user's question.

R: Result
----------
Output the name of the specialist agent that should handle this specific query. This will ensure that the user's needs are accurately addressed by the appropriate expert system.

E: Examples
-----------
Examples of user queries and the specialist agents best suited to handle them:
- GeneralInfo Example 1: What is a mortgage? [Primary Intent: Information, Secondary Intent: None]
- Eligibility Example 1: Am I eligible for a mortgage with a low credit score? [Primary Intent: Eligibility, Secondary Intent: Credit]
- Docs Example 1: What documents do I need for a loan application? [Primary Intent: Documentation, Secondary Intent: ApplicationProcess]
- Followup Example 1: What's the next step after my application? [Primary Intent: FollowUp, Secondary Intent: ApplicationProcess]
- App Example 1: How do I start the application process? [Primary Intent: Application, Secondary Intent: None]
- DocReview Example 1: Is my document verification complete? [Primary Intent: DocumentReview, Secondary Intent: FollowUp]

Given:
- User Query: {{user_query}}
- Detected Intents: {{intents}}
- Detected Entities: {{entities}}

Which specialist agent is best suited to handle this query?

""")

# Define the OutputParser
class CustomRouterOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Extract the relevant part of the sentence (assuming it ends with a dot)
        suggested_agent = llm_output.strip().split("is the ")[-1].rstrip(".")
        
        # Check if the suggested agent is in the list of available agents
        available_agents = ['GeneralInfo', 'Eligibility', 'Docs', 'Followup', 'App', 'DocReview']
        for agent in available_agents:
            if agent.lower() in suggested_agent.lower():
                logger.info(f"Suggested agent is {agent}.")
                return AgentFinish(return_values={"suggested_agent": agent, "output": llm_output}, log=llm_output)
                
        # If no match is found, default to GeneralInfo
        logger.info(f"Suggested agent is GeneralInfo.")
        return AgentFinish(return_values={"suggested_agent": "GeneralInfo", "output": llm_output}, log=llm_output)


# LLM Chain
llm_chain = LLMChain(llm=llm, prompt=router_prompt)

router_output_parser = CustomRouterOutputParser()

# LLMAgent
router_agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=router_output_parser,
    stop=["\n"]
)

# AgentExecutor
agent_executor = AgentExecutor(agent=router_agent, tools=[], verbose=True)

class RouterAgent:
    def __init__(self):
        self.agents = {
            'Eligibility': eligibility_agent,
            'Docs': docs_agent,
            'Followup': followup_agent,
            'App': app_agent,
            'DocReview': doc_agent
        }
        self.db_manager = DatabaseManager(BASE_ID, API_KEY, TABLE_NAME)  # Initialize DatabaseManager

    def route(self, input):
        logger.info(f"Routing input query: {input}")

        # NLU Agent Processing
        raw_response = nlu_agent_executor.run({"input": input, "agent_scratchpad": ""})
        parsed_response = extract_from_response(raw_response)
        primary_intents = parsed_response['primary_intent']
        secondary_intents = parsed_response['secondary_intent']
        entities = parsed_response['entities']
        confidence_score = calculate_confidence(input, raw_response)

        # Routing
        raw_agent_suggestion = agent_executor.run({"user_query": input, "intents": primary_intents, "entities": entities})
        
        # Parse raw output 
        parsed_suggestion = router_output_parser.parse(raw_agent_suggestion)
        
        # Extract suggested agent
        suggested_agent_key = parsed_suggestion.return_values["suggested_agent"]
        
        logger.info(f"Suggested agent is {suggested_agent_key}.")  # Added logging
        
        # Generate response
        selected_agent = self.agents.get(suggested_agent_key, GeneralInfoAgent())
        response = selected_agent.process(input, entities)

        # Database Insertion
        self.db_manager.insert_interaction(
            user_query=input,
            mira_response=response,
            primary_intents=primary_intents,
            secondary_intents=','.join(secondary_intents) if secondary_intents else 'None',
            entities=entities,
            action_taken=suggested_agent_key,
            confidence_score=confidence_score,
            session_id="N/A"  # Placeholder
        )

        return response

# Example usage
if __name__ == "__main__":
    router = RouterAgent()
    responses = {}

    queries = [
    "How do interest rates influence my monthly mortgage payments?",
    "What documents are required for refinancing my home?",
    "Can you explain the difference between a fixed-rate and an adjustable-rate mortgage?",
    "What's the process to apply for a jumbo loan, and what are the eligibility criteria?",
    "Are there any special programs for first-time homebuyers?"
    ]

    for query in queries:
        responses[query] = router.route(query)

    for query, response in responses.items():
        print(f"Query: {query}\nResponse: {response}\n{'-'*50}\n")
    
