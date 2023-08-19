import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')


class DatabaseManager:
    def __init__(self, base_id, api_key, table_name):
        self.base_id = base_id
        self.api_key = api_key
        self.table_name = table_name
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def add_user(self, data):
        """Add a new user to the Airtable database."""
        response = requests.post(self.base_url, headers=self.headers, json={"fields": data})
        logging.debug(f"Add user response status: {response.status_code}, response text: {response.text}")
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.json()

    def get_user(self, username=None, email=None):
        """Retrieve a user's details based on username or email."""
        records = self.get_records()
        logging.debug(f"Retrieved {len(records)} user records from the database.")
        for record in records:
            record_username = record['fields'].get('Username')
            record_email = record['fields'].get('Email')
            logging.debug(f"Checking user record with username: {record_username}, email: {record_email}")
            if record_username == username or record_email == email:
                logging.debug(f"Matched user record with username: {record_username}, email: {record_email}")
                return record
        logging.warning(f"No user record found with username: {username}, email: {email}")
        return None

    def update_user(self, record_id, data):
        """Update user details."""
        logging.debug("Updating user with record_id: %s, data: %s", record_id, data) # Log the record ID and data
        response = requests.patch(f"{self.base_url}", headers=self.headers, json=data)
        
        if response.status_code != 200:
            print("Error updating user:", response.text)  # This will print the error message from Airtable
        response.raise_for_status()
        return response.json()

    def delete_user(self, record_id):
        """Delete a user from the database."""
        response = requests.delete(f"{self.base_url}/{record_id}", headers=self.headers)
        response.raise_for_status()
        return response.status_code == 200

    def get_records(self):
        """Utility function to get all records."""
        response = requests.get(self.base_url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('records')


# Testing the user addition function
def test_add_update_retrieve_user():
    db_manager = DatabaseManager(BASE_ID, API_KEY, TABLE_NAME)
    
    # Step 1: Add a user
    new_user_data = {
        "Username": "suketu.gaglani@gmail.com",
        "Password": "@022123suektu",
        "Full Name": "Suketu Gaglani",
        "Phone Number": "832-730-5114",
        "User Type": "Consumer"
    }
    added_user_response = db_manager.add_user(new_user_data)
    print("Added user:", added_user_response)

    user_record_id = added_user_response['id']  # Fetch the record ID of the newly added user

    # Step 2: Update the user
    update_data = {
        "Full Name": "Updated Add Update User"
    }
    updated_user_response = db_manager.update_user(user_record_id, update_data)
    print("Updated user:", updated_user_response)

    # Step 3: Retrieve the updated user
    retrieved_user = db_manager.get_user(username=new_user_data["Username"])
    print("Retrieved user:", retrieved_user)

    # Step 4: Delete the user
    delete_status = db_manager.delete_user(user_record_id)
    print(f"Deleted user with ID {user_record_id}: {delete_status}")

if __name__ == '__main__':
    test_add_update_retrieve_user()
