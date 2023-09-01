# memory.py

from uuid import uuid4
from langchain.memory import ZepMemory
from langchain.schema import HumanMessage, AIMessage

class ChatMemory:

    def __init__(self):
      
        # Zep API credentials
        self.zep_api_url = "https://cloud.getzep.com" 
        self.zep_api_key = "xxx"  

        # Create a unique session ID        
        self.session_id = str(uuid4())

        # Initialize ZepMemory
        self.memory = ZepMemory(
            session_id=self.session_id,
            url=self.zep_api_url, 
            api_key=self.zep_api_key,
            memory_key="chat_history" 
        )

    def add_human_message(self, message):
        self.memory.add_message(
            HumanMessage(content=message)
        )

    def add_ai_message(self, message):
        self.memory.add_message(
            AIMessage(content=message)
        )
        
    # Other memory methods (get, search etc)