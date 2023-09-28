from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, AgentType
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from retriever import get_highest_similarity_score
from GeneralInfo_agent import GeneralInfoAgent  # Import GeneralInfoAgent
from database_prep import DatabaseManager  # Import DatabaseManager
from typing import List, Union, Optional
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import math
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

def Application(query, entities):
    return "To apply, please fill out the application form on our website."

def doc_process(query, entities):
    return "Please upload your documents through our secure portal."

def loan_comparison_process(query, entities):
    return "To compare loans, consider interest rates, terms, and fees."

def amortization_process(query, entities):
    return "Amortization involves paying off the loan in fixed installments."

def Scenario(query, entities):
    return "For different scenarios, we offer various mortgage solutions tailored to your needs."


# Initialize Tools with Specialist Agent Functions
eligibility_agent = Tool(name="Eligibility Agent", func=eligibility_process, description="Handles eligibility queries")
docs_agent = Tool(name="Docs Agent", func=docs_process, description="Handles document queries")
followup_agent = Tool(name="Followup Agent", func=followup_process, description="Handles follow-up actions")
app_agent = Tool(name="App Agent", func=Application, description="Guides through the application process")
doc_agent = Tool(name="Doc Agent", func=doc_process, description="Handles document submission and review")
loan_comparison_agent = Tool(name="Loan Comparison Agent", func=loan_comparison_process, description="Handles loan comparison queries")
amortization_agent = Tool(name="Amortization Agent", func=amortization_process, description="Handles amortization queries")
scenario_agent = Tool(name="Scenario Agent", func=Scenario, description="Handles different mortgage scenarios")



template = f"""
Given a mortgage-related user query, identify Primary Intents, Secondary Intents, and Specialist Agent as per the training provided and format the response as follows:

- Start with "Primary Intent:" followed by the identified primary intent.
- Identify secondary intent, list it as "Secondary Intent:" followed by the identified secondary intent.
- List entities as comma-separated values after "Entities:".
- End with "Specialist Agent:" followed by the identified specialist agent best suited to handle the query.

Question: {{input}}
{{agent_scratchpad}}"""

class ConfidenceCalculator:
    # Constants for component weights
    PRIMARY_INTENT_WEIGHT = 0.20
    SECONDARY_INTENT_WEIGHT = 0.15
    ENTITY_WEIGHT = 0.20
    AGENT_WEIGHT = 0.20
    SEMANTIC_WEIGHT = 0.10
    DOMAIN_SPECIFICITY_WEIGHT = 0.15

    def __init__(self, known_agents):
        self.known_agents = known_agents

    def calculate_confidence(self, input_query, output, specialist_agent, log=True):
        parsed_response = extract_from_response(output)
        primary_intent = parsed_response.get('primary_intent', '')
        secondary_intents = parsed_response.get('secondary_intent', [])
        extracted_entities = parsed_response.get('entities', [])
        
        # Intent Confidence
        primary_intent_confidence = self._calculate_intent_confidence(primary_intent)
        
        # Secondary Intent Confidence
        secondary_intent_confidence = self._calculate_intent_confidence(secondary_intents)
        
        # Semantic Confidence
        semantic_confidence = self._calculate_semantic_confidence(input_query)
        
        # Entity Confidence
        entity_confidence = self._calculate_entity_confidence(extracted_entities)
        
        # Specialist Agent Confidence
        agent_confidence = self._calculate_agent_confidence(specialist_agent)
        
        # Domain-Specificity Confidence
        domain_specificity = self._calculate_domain_specificity(input_query)
        
        # Overall confidence with new metric
        confidence = self._calculate_overall_confidence(primary_intent_confidence, semantic_confidence, secondary_intent_confidence, entity_confidence, agent_confidence, domain_specificity)
        
        if log:
            logger.info(f"Individual Components: Semantic: {semantic_confidence}, Primary: {primary_intent_confidence}, Entity: {entity_confidence}")
            logger.info(f"Confidence components: {semantic_confidence}, {primary_intent_confidence}, {entity_confidence}")
            logger.info(f"Calculated confidence for query '{input_query}': {confidence}")
        
        return confidence

    def _calculate_intent_confidence(self, intent):
        return 1.0 if intent else 0.0

    def _calculate_semantic_confidence(self, input_query):
        similarity_score = get_highest_similarity_score(input_query)
        return similarity_score  # Use the raw score

    def _calculate_entity_confidence(self, entities):
        return 1.0 if entities else 0.0

    def _calculate_agent_confidence(self, agent):
        return 1.0 if agent in self.known_agents else 0.0

    def _calculate_domain_specificity(self, input_query):
        similarity_score = get_highest_similarity_score(input_query)
        return 1.0 if similarity_score > 0.7 else 0.0

    def _calculate_overall_confidence(self, primary_intent_confidence, semantic_confidence, secondary_intent_confidence, entity_confidence, agent_confidence, domain_specificity):
        confidence = (self.PRIMARY_INTENT_WEIGHT * primary_intent_confidence +
                      self.SEMANTIC_WEIGHT * semantic_confidence +
                      self.SECONDARY_INTENT_WEIGHT * secondary_intent_confidence +
                      self.ENTITY_WEIGHT * entity_confidence +
                      self.AGENT_WEIGHT * agent_confidence +
                      self.DOMAIN_SPECIFICITY_WEIGHT * domain_specificity)
        
        # Clip to valid range [0, 1]
        return max(0.0, min(1.0, confidence))

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
    'Appication': app_agent,
    'DocReview': doc_agent,
    'GeneralInfo': general_info_agent,  # Add this line
    'LoanComparison': loan_comparison_agent,
    'Amortization': amortization_agent,
    'Scenario': scenario_agent
}

# Initialize ConfidenceCalculator with known agents
confidence_calculator = ConfidenceCalculator(known_agents=agents.keys())

# RouterAgent Class
class RouterAgent:
    def route(self, user_query):
        response = None  # Initialize response to None or some default value
        confidence = 0.0  # Initialize confidence to a default value
        try:
            output_parser.set_user_query(user_query)  # Set the user_query for CustomOutputParser
            raw_response = agent_executor.run({"input": user_query, "agent_scratchpad": ""})
            parsed_response = output_parser.parse(raw_response)  # No need to pass user_query here

            primary_intent = parsed_response.return_values.get('primary_intent', 'Error')
            secondary_intent = parsed_response.return_values.get('secondary_intent', '')
            entities = parsed_response.return_values.get('entities', [])
            specialist_agent = parsed_response.return_values.get('specialist_agent', '')

            confidence = confidence_calculator.calculate_confidence(user_query, raw_response, specialist_agent, log=True)

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

        return response, confidence, specialist_agent
    
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
        confidence = confidence_calculator.calculate_confidence(user_query, llm_output, specialist_agent, log=False)  # use user_query

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
llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0613:personal::7scg7esv", temperature=0.7)

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
        "Can you provide some information about FHA loans?",
        "What are the documents required to start the pre-approval process?",
        "How to check if I am eligible for a mortgage",
        "What is the status of my Loan Application",
        "How do I submit my documents?",
        "I have scenario I want to discuss?"
    ]

    for query in sample_queries:
        response, confidence, specialist_agent = router_agent.route(query)  # This will internally handle everything

        # Print results
        print(f"Query: {query}")
        print(f"Response: {response}")
        print(f"Specialist Agent: {specialist_agent}")
        print(f"Confidence: {confidence}")

if __name__ == "__main__":
    test_agent()