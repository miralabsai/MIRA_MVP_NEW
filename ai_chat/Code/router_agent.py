from nlu_agent import agent_executor, extract_from_response, calculate_confidence  # Added imports
from GeneralInfo_agent import GeneralInfoAgent
from database_prep import DatabaseManager  # Import DatabaseManager
import os

# Load environment variables
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

# Specialist Agents
class EligibilityPrequalAgent:
    def process(self, input, entities):
        return "Assessment regarding eligibility and prequalification."

class DocsAgent:
    def process(self, input, entities):
        return "Information about document submission."

class FollowUpAgent:
    def process(self, input, entities):
        return "Follow-up details."

class ApplicationAgent:
    def process(self, input, entities):
        return "Guidance on mortgage application."

class DocumentAgent:
    def process(self, input, entities):
        return "Handling document collection and processing."

# Router Agent
class RouterAgent:
    def __init__(self):
        self.agents = {
            'general_info': GeneralInfoAgent(),
            'eligibility': EligibilityPrequalAgent(),
            'preapproval': DocsAgent(),
            'follow_up': FollowUpAgent(),
            'application_process': ApplicationAgent(),
            'document_submission': DocumentAgent()
        }
        self.db_manager = DatabaseManager(BASE_ID, API_KEY, TABLE_NAME)  # Initialize DatabaseManager

    def route(self, input):
        # Fetching intent, entities, and confidence score from nlu_agent.py
        raw_response = agent_executor.run({"input": input, "agent_scratchpad": ""})
        parsed_response = extract_from_response(raw_response)

        primary_intents = parsed_response['primary_intent']
        secondary_intents = parsed_response['secondary_intent']
        entities = parsed_response['entities']
        confidence_score = calculate_confidence(input, raw_response)

        agent_key = self.get_agent_based_on_intent(primary_intents)
        agent = self.agents.get(agent_key, GeneralInfoAgent())
        response = agent.process(input, entities)

        # Store data in the database with placeholders for session_id and updated intent storage
        self.db_manager.insert_interaction(
        user_query=input,
        mira_response=response,
        primary_intents=primary_intents,
        secondary_intents=','.join(secondary_intents) if secondary_intents else 'None',
        entities=entities,
        action_taken=agent_key,
        confidence_score=confidence_score,
        session_id="N/A"  # Placeholder for session_id
        )

        return response

    def get_agent_based_on_intent(self, intent):
        # This logic determines which agent the query goes to based on the intent
        return intent  # Return the intent as key to fetch the agent. Adjust if the logic changes.

# Test section
if __name__ == "__main__":
    router = RouterAgent()
    responses = {}

    queries = [
        "Can you explain the concept of down payment assistance and share appreciation in mortgage lending?",
        "Can I use a 5/1 ARM mortgage on an investment property",
        "What is the difference between FHA loans and Conventional Loans",
        "What documents do I need to apply for a mortgage?",
        "Should I take out a 15 or 30 year mortgage?",
        "What documents are required for refinancing my home?"
    ]

    for query in queries:
        responses[query] = router.route(query)

    for query, response in responses.items():
        print(f"Query: {query}\nResponse: {response}\n{'-'*50}\n")
