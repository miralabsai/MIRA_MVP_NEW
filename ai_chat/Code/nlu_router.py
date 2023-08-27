from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from retriever import get_highest_similarity_score
from GeneralInfo_agent import GeneralInfoAgent  # Import GeneralInfoAgent
from database_prep import DatabaseManager  # Import DatabaseManager
from typing import List, Union
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

# Load the data from the JSON file
with open("ai_chat/Data/Prompt_Eg/router_prompt_ex.json", "r") as file:
    MORTGAGE_INTENTS = json.load(file)
logger.info("Data loaded from router_prompt_ex.json.")

# Create a list to store examples in the desired format
examples_list = []

# Iterate over each intent in MORTGAGE_INTENTS
for intent, intent_data_list in MORTGAGE_INTENTS.items():
    for i, intent_data in enumerate(intent_data_list):
        example = intent_data['query']
        entities_list = intent_data.get('entities', [])
        specialist_agent = intent_data.get('Specialist Agent', 'Not Specified')

        example_str = f"- {intent} Example {i+1}: {example}"
        
        # Include entities if available
        if entities_list:
            entities_str = ", ".join(entities_list)
            example_str += f" [Entities: {entities_str}]"
        
        # Include Specialist Agent
        example_str += f" [Specialist Agent: {specialist_agent}]"
        
        examples_list.append(example_str)

# Create the updated prompt template with the examples in JSON format
examples_str = "\n".join(examples_list)
template = f"""
Given a mortgage-related user query, identify Primary Intents, Secondary Intents, and Specialist Agent as explained in examples and format the response as follows:

- Start with "Primary Intent:" followed by the identified primary intent.
- Identify secondary intent, list it as "Secondary Intent:" followed by the identified secondary intent.
- List entities as comma-separated values after "Entities:".
- End with "Specialist Agent:" followed by the identified specialist agent best suited to handle the query.

For example: {examples_str}

Question: {{input}}
{{agent_scratchpad}}"""

def get_known_entities_and_agents():
    all_entities = []
    all_agents = set()  # Using a set to automatically remove duplicates
    for intent_data_list in MORTGAGE_INTENTS.values():
        for intent_data in intent_data_list:
            entities_list = intent_data.get('entities', [])
            specialist_agent = intent_data.get('specialist_agent', None)  # Assuming the key is 'specialist_agent' in JSON
            all_entities.extend(entities_list)
            if specialist_agent:
                all_agents.add(specialist_agent)
    return set(all_entities), all_agents


def calculate_confidence(input_query, output, specialist_agent):
    parsed_response = extract_from_response(output)
    primary_intent = parsed_response.get('primary_intent', '')
    secondary_intents = parsed_response.get('secondary_intent', [])
    extracted_entities = parsed_response.get('entities', [])
    specialist_agent = parsed_response.get('Specialist Agent', '')
    
    # Intent Confidence
    primary_intent_confidence = 1.0 if primary_intent in MORTGAGE_INTENTS else 0.0
    
    # Checking each secondary intent against MORTGAGE_INTENTS
    secondary_intent_confidence = all(intent in MORTGAGE_INTENTS for intent in secondary_intents)
    
    # Semantic Confidence
    similarity = get_highest_similarity_score(input_query)
    semantic_confidence = min(similarity, 1.0)
    
    # Entity Confidence
    known_entities, known_agents = get_known_entities_and_agents()
    entity_overlap = len(set(extracted_entities) & known_entities)
    entity_confidence = entity_overlap / len(extracted_entities) if extracted_entities else 1.0
    
    # Specialist Agent Confidence
    known_entities, known_agents = get_known_entities_and_agents()
    agent_confidence = 1.0 if specialist_agent in known_agents else 0.0
    
    # Overall confidence
    confidence = 0.5 * primary_intent_confidence + 0.30 * semantic_confidence + 0.1 * entity_confidence + 0.1 * agent_confidence
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

# Output Parser
class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        lines = llm_output.split('\n')

        # Initial values
        primary_intent = ""
        secondary_intent = None
        entities = ""
        specialist_agent = ""
        input_query = ""

        for line in lines:
            if "Primary Intent:" in line:
                primary_intent = line.split("Primary Intent:")[1].strip()
            elif "Secondary Intent:" in line:
                secondary_intent = line.split("Secondary Intent:")[1].strip()
            elif "Entities:" in line:
                entities = line.split("Entities:")[1].strip()
            elif "Specialist Agent:" in line:
                specialist_agent = line.split("Specialist Agent:")[1].strip()

        # Logging before applying additional agent selection logic
        logger.info(f"Agent before additional selection: {specialist_agent}")
        
        # Calculate confidence
        confidence = calculate_confidence(input_query, llm_output, specialist_agent)

        # Debugging: Why is GeneralInfo not being selected?
        if specialist_agent != "GeneralInfo":
            logger.debug(f"Why not GeneralInfo? Confidence: {confidence}, Specialist Agent: {specialist_agent}, Primary Intent: {primary_intent}")

        # Route to the appropriate specialist agent
        selected_agent = agents.get(specialist_agent, general_info_agent)  # Assuming GeneralInfoAgent exists
        response = selected_agent.func(input_query, entities)  # Assuming process is a method in the agents
        logger.info(f"Agent after additional selection: {specialist_agent}")

        # Inserting record into DB
        db_manager.insert_interaction(
            user_query=input_query,
            mira_response=response,
            primary_intents=primary_intent,
            secondary_intents=secondary_intent,
            entities=entities,
            action_taken=specialist_agent,
            confidence_score=confidence,
            session_id="N/A"  # Placeholder
        )

        logger.info(f"Primary Intent: {primary_intent}, Secondary Intent: {secondary_intent}, Entities: {entities}, Specialist Agent: {specialist_agent}, Confidence: {confidence}.")

        return AgentFinish(
            return_values={
                "primary_intent": primary_intent,
                "secondary_intent": secondary_intent,
                "entities": entities,
                "specialist_agent": specialist_agent,
                "output": llm_output.strip(),
                "confidence": confidence,
                "response": response  # New field
            },
            log={"llm_output": llm_output}
        )

output_parser = CustomOutputParser()

# Set up LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

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
            secondary_intents = line.split("Secondary Intent:")[1].strip().split(",")
            extracted_data["secondary_intent"] = [intent.strip() for intent in secondary_intents]
        elif "Entities:" in line:
            entities = line.split("Entities:")[1].strip().split(",")
            extracted_data["entities"] = [entity.strip() for entity in entities]
        elif "Specialist Agent:" in line:  # New condition
            extracted_data["specialist_agent"] = line.split("Specialist Agent:")[1].strip()

    logger.info(f"Extracted primary intent: {extracted_data['primary_intent']}, secondary intent: {extracted_data['secondary_intent']}, entities: {extracted_data['entities']}, specialist agent: {extracted_data['specialist_agent']}.")
    return extracted_data

def test_agent():
    sample_queries = [
    "How do interest rates influence my monthly mortgage payments?",
    "What documents are required for refinancing my home?",
    "Can you explain the difference between a fixed-rate and an adjustable-rate mortgage?",
    "What's the process to apply for a jumbo loan, and what are the eligibility criteria?",
    "Are there any special programs for first-time homebuyers?"
    ]

    for query in sample_queries:
        raw_response = agent_executor.run({"input": query, "agent_scratchpad": ""})
        
        print(f"Raw Response: {raw_response}\n")
        
        parsed_response = extract_from_response(raw_response)
        primary_intent = parsed_response.get('primary_intent', 'Error')
        secondary_intent = parsed_response.get('secondary_intent', '')
        entities = parsed_response.get('entities', [])
        specialist_agent = parsed_response.get('specialist_agent', '')  # Extracting specialist_agent
        
        # Note the change here: providing query, raw_response, and specialist_agent
        confidence = calculate_confidence(query, raw_response, specialist_agent)  # Passing specialist_agent
        
        print(f"Query: {query}")
        print(f"Primary Intent Identified: {primary_intent}")
        if secondary_intent:
            print(f"Secondary Intent Identified: {secondary_intent}")
        print(f"Entities: {', '.join(entities)}")
        print(f"Specialist Agent: {specialist_agent}")  # Outputting specialist_agent
        print(f"Confidence: {confidence}\n")

if __name__ == "__main__":
    test_agent()


def get_known_entities():
    all_entities = []
    for intent_data_list in MORTGAGE_INTENTS.values():
        for intent_data in intent_data_list:
            entities_list = intent_data.get('entities', [])
            all_entities.extend(entities_list)
    return set(all_entities)
