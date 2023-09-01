from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from retriever import get_highest_similarity_score
from GeneralInfo_agent import GeneralInfoAgent  # Import GeneralInfoAgent
from database_prep import DatabaseManager  # Import DatabaseManager
from typing import List, Union, Optional
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import json
import os
import openai
import dotenv
from logger import setup_logger
import logging  # Added import for logging

# Set up the logger with the correct level
logger = setup_logger('nlu_logger', level=logging.INFO)

dotenv.load_dotenv()

logger.info("Initializing OpenAI with API key...")

# Initialize OpenAI
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
logger.info("OpenAI initialized with API key.")
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

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

# Initialize Tools with Specialist Agent Functions
eligibility_agent = Tool(name="Eligibility Agent", func=eligibility_process, description="Handles eligibility queries")
docs_agent = Tool(name="Docs Agent", func=docs_process, description="Handles document queries")
followup_agent = Tool(name="Followup Agent", func=followup_process, description="Handles follow-up actions")
app_agent = Tool(name="App Agent", func=app_process, description="Guides through the application process")
doc_agent = Tool(name="Doc Agent", func=doc_process, description="Handles document submission and review")

template = f"""
Given a mortgage-related user query, identify Primary Intents, Secondary Intents, and Specialist Agent as explained in examples and format the response as follows:

- Start with "Primary Intent:" followed by the identified primary intent.
- Identify secondary intent, list it as "Secondary Intent:" followed by the identified secondary intent.
- List entities as comma-separated values after "Entities:".
- End with "Specialist Agent:" followed by the identified specialist agent best suited to handle the query.

Question: {{input}}
{{agent_scratchpad}}"""

def calculate_confidence(input_query, output, specialist_agent, log=True):
    parsed_response = extract_from_response(output)
    primary_intent = parsed_response.get('primary_intent', '')
    secondary_intents = parsed_response.get('secondary_intent', [])
    extracted_entities = parsed_response.get('entities', [])
    specialist_agent = parsed_response.get('specialist_agent', '')  # Note: Corrected the key to be lowercase
    
    # Intent Confidence
    primary_intent_confidence = 1.0 if primary_intent else 0.0  # Trusting the fine-tuned model for accuracy
    
    # Secondary Intent Confidence (updated)
    secondary_intent_confidence = 1.0 if secondary_intents else 0.0  # Trusting the fine-tuned model for accuracy
    
    # Get the actual float similarity score instead of boolean
    similarity_score = get_highest_similarity_score(input_query)  # Assuming this function now returns a float
    
    # Semantic Confidence
    semantic_confidence = similarity_score  # Use the float score directly
    
    # Entity Confidence (updated)
    entity_confidence = 1.0 if extracted_entities else 0.0  # Trusting the fine-tuned model for entity extraction
    
    # Specialist Agent Confidence (updated)
    known_agents = ["Eligibility", "Docs", "Followup", "App", "DocReview", "GeneralInfo"] # Define known agents
    agent_confidence = 1.0 if specialist_agent in known_agents else 0.0
    
     # Overall confidence
    confidence = 0.2 * primary_intent_confidence + 0.3 * semantic_confidence + 0.1 * secondary_intent_confidence + 0.1 * entity_confidence + 0.3 * agent_confidence
    
    if log:
        logger.info(f"Calculated confidence for query '{input_query}': {confidence}.")
    return confidence

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps", [])
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts
        return self.template.format(**kwargs)

prompt = CustomPromptTemplate(template=template, input_variables=["input", "agent_scratchpad"], tools=[])

# Initialize Database Manager (Assuming DatabaseManager class exists)
db_manager = DatabaseManager(BASE_ID, API_KEY, TABLE_NAME)  # Initialize DatabaseManager

# Initialize the GeneralInfoAgent class
general_info_agent = GeneralInfoAgent()

# Define agents (Assuming these agents are already initialized)
agents = {
    'Eligibility': eligibility_agent,
    'Docs': docs_agent,
    'Followup': followup_agent,
    'App': app_agent,
    'DocReview': doc_agent,
    'GeneralInfo': general_info_agent  # Add this line
}

# RouterAgent Class
class RouterAgent:
    def route(self, user_query):
        response = None  # Initialize response to None or some default value
        try:
            output_parser.set_user_query(user_query)  # Set the user_query for CustomOutputParser
            raw_response = agent_executor.run({"input": user_query, "agent_scratchpad": ""})
            parsed_response = output_parser.parse(raw_response)  # No need to pass user_query here

            primary_intent = parsed_response.return_values.get('primary_intent', 'Error')
            secondary_intent = parsed_response.return_values.get('secondary_intent', '')
            entities = parsed_response.return_values.get('entities', [])
            specialist_agent = parsed_response.return_values.get('specialist_agent', '')

            confidence = calculate_confidence(user_query, raw_response, specialist_agent, log=True)

            # Make sure selected_agent.func() returns a value
            selected_agent = agents.get(specialist_agent, general_info_agent)
            response = selected_agent.func(user_query, entities)

            # Inserting record into DB
            db_manager.insert_interaction(
                user_query=user_query,
                mira_response=response,
                primary_intents=primary_intent,
                secondary_intents=','.join(secondary_intent) if isinstance(secondary_intent, list) else secondary_intent,
                entities=entities,
                action_taken=specialist_agent,
                confidence_score=confidence,
                session_id="N/A"  # Placeholder
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle the exception and set response accordingly if needed

        return response, confidence
    
# Output Parser
class CustomOutputParser(AgentOutputParser):
    user_query: Optional[str] = None  # Specify type hint and set default to None

    def set_user_query(self, user_query):
        self.user_query = user_query  # Set user_query as an instance variable

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        lines = llm_output.split('\n')
        parsed_data = extract_from_response(llm_output)
        primary_intent = parsed_data['primary_intent']
        secondary_intent = parsed_data['secondary_intent']
        entities = parsed_data['entities']
        specialist_agent = parsed_data['specialist_agent']

        for line in lines:
            if "Primary Intent:" in line:
                primary_intent = line.split("Primary Intent:")[1].strip()
            elif "Secondary Intent:" in line:
                secondary_intent = line.split("Secondary Intent:")[1].strip()
            elif "Entities:" in line:
                entities = line.split("Entities:")[1].strip().split(", ")
            elif "Specialist Agent:" in line:
                specialist_agent = line.split("Specialist Agent:")[1].strip()

        user_query = self.user_query.strip()
        # Calculate confidence
        confidence = calculate_confidence(user_query, llm_output, specialist_agent, log=False)  # use user_query

        logger.info(f"Primary Intent: {primary_intent}, Secondary Intent: {secondary_intent}, Entities: {entities}, Specialist Agent: {specialist_agent}, Confidence: {confidence}.")

        return AgentFinish(
            return_values={
                "primary_intent": primary_intent,
                "secondary_intent": secondary_intent,
                "entities": entities,
                "specialist_agent": specialist_agent,
                "output": llm_output.strip(),
                "confidence": confidence
            },
            log={"llm_output": llm_output}
        )

output_parser = CustomOutputParser()

# Set up LLM
llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0613:personal::7sczKPwS", temperature=0.9)

# LLM Chain
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Set up the Agent
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservations"]
)

# Agent Executor (turning off verbose mode)
agent_executor = AgentExecutor(agent=agent, tools=[], verbose=False)

def extract_from_response(output: str):
    """
    Extracts primary intent, secondary intent, entities, and specialist agent from the raw LLM output.
    """
    lines = output.strip().split("\n")
    extracted_data = {
        "primary_intent": "",
        "secondary_intent": [],
        "entities": [],
        "specialist_agent": ""  # New field
    }

    for line in lines:
        if "Primary Intent:" in line:
            extracted_data["primary_intent"] = line.split("Primary Intent:")[1].strip()
        elif "Secondary Intent:" in line:
            # Splitting by comma to extract multiple secondary intents, if present
            secondary_intents = line.split("Secondary Intent:")[1].strip().split(", ")
            extracted_data["secondary_intent"] = [intent.strip() for intent in secondary_intents]
        elif "Entities:" in line:
            entities = line.split("Entities:")[1].strip().split(", ")
            extracted_data["entities"] = [entity.strip() for entity in entities]
        elif "Specialist Agent:" in line:  # New condition
            extracted_data["specialist_agent"] = line.split("Specialist Agent:")[1].strip()

    #logger.info(f"Extracted primary intent: {extracted_data['primary_intent']}, secondary intent: {extracted_data['secondary_intent']}, entities: {extracted_data['entities']}, specialist agent: {extracted_data['specialist_agent']}.")
    return extracted_data

# Initialize RouterAgent
router_agent = RouterAgent()

def test_agent():
    sample_queries = [
        "Are there any special programs for first-time homebuyers?"
    ]

    for query in sample_queries:
        response, confidence = router_agent.route(query)  # This will internally handle everything

        # Print results
        print(f"Query: {query}")
        print(f"Response: {response}")
        print(f"Confidence: {confidence}")

if __name__ == "__main__":
    test_agent()