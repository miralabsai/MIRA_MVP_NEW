import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load constants
INDEX_PATH = 'ai_chat/Extracted_data/faiss_index.bin'  
CHUNKS_PATH = 'ai_chat/Extracted_Data/chunks.pkl'  # Ensure this file contains the chunks

# Load index
index = faiss.read_index(INDEX_PATH)

# Load model
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open(CHUNKS_PATH, 'rb') as f:
    chunks = pickle.load(f)

def retrieve(query, k=2):
    try:
        # Encode input 
        query_embedding = embedder.encode(query)
    
        # Run search
        _, indices = index.search(np.expand_dims(query_embedding, 0), k)
    
        # Return chunks based on the found indices
        return [chunks[i] for i in indices[0]]
    except Exception as e:
        print(f"Error in retrieval: {str(e)}")
        return []

# New function to get the highest similarity score
def get_highest_similarity_score(query):
    # Encode input 
    query_embedding = embedder.encode(query)
    
    # Run search
    distances, _ = index.search(np.expand_dims(query_embedding, 0), 1)
    
    # Return the highest similarity score (or distance)
    return distances[0][0]>0.5

