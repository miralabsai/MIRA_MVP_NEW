import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import pandas as pd
from tqdm import tqdm
from openai.embeddings_utils import get_embedding  # Assuming this is the correct import
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Constants
CHUNK_SIZE = 166  # Adjust this based on your specific needs
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"
max_tokens = 8000

# Initialize counters for skipped rows and columns
skipped_rows = 0
skipped_columns = 0

# Initialize Persistent Chroma Client
print("Initializing Persistent Chroma Client...")
chroma_client = chromadb.PersistentClient(path="ai_chat/Extracted_Data/Chroma_Db/OPENAI")

# Initialize OpenAI Embedding Function
print("Initializing OpenAI Embedding Function...")
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name=embedding_model)

# Create Chroma Collection
print("Creating Chroma Collection...")
collection = chroma_client.create_collection(name="mortgage_data", embedding_function=embedding_function, metadata={"hnsw:space": "cosine"})

# Load DataFrame
print("Loading Data from Excel...")
df = pd.read_excel('ai_chat/Data/Knowledgebase/Merged_Master_Fannie_Freddie_Final.xlsx')

# List of columns to convert to embeddings
columns_to_convert = ["Cleaned_Description", "summarized_text", "entities"]

print("Converting Text to Embeddings and Storing in Chroma Collection...")
for i, row in tqdm(df.iterrows(), total=df.shape[0], desc="Rows"):
    for column in columns_to_convert:
        text = str(row[column])
        
        # Check if the text exceeds the max token limit
        n_tokens = len(text.split())  # Simple whitespace-based tokenization
        if n_tokens > max_tokens:
            print(f"Skipping row {i} and column {column} due to exceeding max token limit.")
            skipped_rows += 1
            skipped_columns += 1
            continue

        # Replace with actual OpenAI call to get the embedding
        embedding = get_embedding(text, engine=embedding_model, encoding=embedding_encoding)  # Pseudo-code; replace with actual OpenAI call
        #embedding = embedding.tolist()  # Convert NumPy array to list if needed

        metadata = {
            "unique_id": f"{i}_{column}",
            "Category": row['Category'],
            "Sub_Category": row['Sub_Category'],
            "Sub_Sections": row['Sub_Sections'],
            "Cleaned_Description": row['Cleaned_Description'],
            "summarized_text": row['summarized_text'],
            "entities": row['entities'],
            "FAQ": row['FAQ'],
            "FAQ_Answers": row['FAQ_Answers'],
            "Intent": row['Intent'],
            "column": column
        }
        
        # Insert into ChromaDB collection
        collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[f"{i}_{column}"]
        )

# Print the total number of skipped rows and columns
print(f"Total skipped rows: {skipped_rows}")
print(f"Total skipped columns: {skipped_columns}")
