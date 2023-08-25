import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from logger import setup_logger
import logging

# Set up the logger
logger = setup_logger('database_manager', level=logging.INFO)

load_dotenv()

API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')


class DatabaseManager:
    def __init__(self, BASE_ID, API_KEY, TABLE_NAME):
        logger.info("Initializing DatabaseManager.")
        self.base_id = BASE_ID
        self.api_key = API_KEY
        self.table_name = TABLE_NAME
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.verify_or_create_fields()

    def verify_or_create_fields(self):
        logger.info("Verifying or creating fields in the database.")
        response = requests.get(self.base_url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            existing_fields = {field for record in data.get('records', []) for field in record.get('fields', {})}
            required_fields = ["User Query", "MIRA Response", "Primary Intents", "Secondary Intents", "Entities",
                               "Timestamp", "Session ID", "Action Taken", "Confidence Score", "Feedback"]

            for field in required_fields:
                if field not in existing_fields:
                    self.create_field(field)
        else:
            logger.error(f"Error fetching fields from Airtable. Status Code: {response.status_code}. Response: {response.text}")

    def create_field(self, field_name):
        logger.warning(f"Field '{field_name}' does not exist. Please create it manually in Airtable.")

    def insert_interaction(self, user_query, mira_response, primary_intents, secondary_intents, entities, session_id, action_taken=None, confidence_score=None, feedback=None):
        logger.info("Inserting interaction into the database.")
        data = {
            "fields": {
                "User Query": user_query,
                "MIRA Response": mira_response,
                "Primary Intents": primary_intents,
                "Secondary Intents": secondary_intents,
                "Entities": ", ".join(entities),  # Convert list to comma-separated string
                "Action Taken": action_taken,
                "Confidence Score": confidence_score,
                "Feedback": feedback
            }
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        if response.status_code == 200:
            logger.info("Interaction inserted successfully!")
        else:
            logger.error(f"Failed to insert interaction. Status code: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    db_manager = DatabaseManager(BASE_ID, API_KEY, TABLE_NAME)
    # Sample interaction insertion, you can remove this or modify as per your requirements.
    db_manager.insert_interaction(
        user_query="How's the weather?",
        mira_response="It's sunny!",
        primary_intents=["weather_update"],
        secondary_intents=["sunny"],
        entities=[],
        session_id="session123"
    )