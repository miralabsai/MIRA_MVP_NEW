import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Constants
CHUNK_SIZE = 166  # Adjust this value based on your specific needs

# Initialize Persistent Chroma Client
print("Initializing Persistent Chroma Client...")
chroma_client = chromadb.PersistentClient(path="ai_chat/Extracted_Data/Chroma_Db")

# Initialize Sentence Transformers Embedding Function
print("Initializing Sentence Transformer Embedding Function...")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create a Chroma collection with Sentence Transformers as the embedding function
print("Creating Chroma Collection...")
collection = chroma_client.create_collection(name="mortgage_data", embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})

# Load data from Excel into DataFrame
print("Loading Data from Excel...")
df = pd.read_excel('ai_chat/Data/Knowledgebase/Merged_Master_Fannie_Freddie_Final.xlsx')

# List of columns to convert to embeddings
columns_to_convert = df.select_dtypes(include=['object']).columns.tolist()

# Initialize Sentence Transformers model
print("Initializing Sentence Transformer Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Converting Text to Embeddings and Storing in Chroma Collection...")
for i, row in tqdm(df.iterrows(), total=df.shape[0], desc="Rows"):
    for column in columns_to_convert:
        text = str(row[column])
        embedding = model.encode([text])[0].tolist()  # Convert NumPy array to list
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

# Query function for semantic search
def query_chroma(query_text, n_results=2, column=None):
    query_embedding = model.encode([query_text])[0].tolist()  # Convert NumPy array to list
    where_filter = {"column": column} if column else None  # Adjusted this line
    
    print("Querying the Collection...")
    results = collection.query(
        query_embeddings=[query_embedding],  # Use the query embedding
        n_results=n_results,
        where=where_filter  # Adjusted this line
    )
    print(f"Query Results for '{query_text}':", results)
    return results

# Example query
query_text = "Tell me about fixed-rate mortgages"
query_results = query_chroma(query_text, column="Cleaned_Description")
