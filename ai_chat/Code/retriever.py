import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from logger import setup_logger
import logging

# Set up the logger
logger = setup_logger('retriever', level=logging.INFO)

# Load constants
INDEX_PATH = "../Extracted_Data/faiss_index.bin"  
CHUNKS_PATH = "../Extracted_Data/chunks.pkl"

# Log the paths being used
logger.info(f"Index path: {INDEX_PATH}")
logger.info(f"Chunks path: {CHUNKS_PATH}")

# Load index
try:
    index = faiss.read_index(INDEX_PATH)
    logger.info("Index loaded successfully")
except Exception as e:
    logger.error(f"Error loading index: {str(e)}")

# Load model
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

try:
    with open(CHUNKS_PATH, 'rb') as f:
        chunks = pickle.load(f)
        logger.info("Chunks loaded successfully")
except Exception as e:
    logger.error(f"Error loading chunks: {str(e)}")

def retrieve(query, k=2):
    try:
        # Encode input 
        query_embedding = embedder.encode(query)
        # Run search
        _, indices = index.search(np.expand_dims(query_embedding, 0), k)
        # Return chunks based on the found indices
        return [chunks[i] for i in indices[0]]
    except Exception as e:
        logger.error(f"Error in retrieval: {str(e)}")
        return []

# New function to get the highest similarity score
def get_highest_similarity_score(query):
    try:
        # Encode input 
        query_embedding = embedder.encode(query)
        # Run search
        distances, _ = index.search(np.expand_dims(query_embedding, 0), 1)
        # Return the highest similarity score (or distance)
        return distances[0][0] > 0.5
    except Exception as e:
        logger.error(f"Error in getting similarity score: {str(e)}")
        return False
