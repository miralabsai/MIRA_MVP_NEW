import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from logger import setup_logger
import logging
import time

# Set up the logger
logger = setup_logger('retriever', level=logging.INFO)

def initialize_retriever():
    global index, embedder, chunks  # Declare as global so they can be accessed outside this function

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
    embedder = SentenceTransformer("../Extracted_Data/Sentence_Transformers")

    try:
        with open(CHUNKS_PATH, 'rb') as f:
            chunks = pickle.load(f)
            logger.info("Chunks loaded successfully")
    except Exception as e:
        logger.error(f"Error loading chunks: {str(e)}")

# Initialize right away so that the rest of the code has access to index and embedder
initialize_retriever()

def retrieve(query, k=2):
    try:
        # Encode input 
        query_embedding = embedder.encode(query)
        # Run search
        _, indices = index.search(np.expand_dims(query_embedding, 0), k)
        # Return chunks based on the found indices
        return [chunks[i] for i in indices[0]]  # Use 'chunks' directly as it's now a global variable
    except Exception as e:
        logger.error(f"Error in retrieval: {str(e)}")
        return []
    
# Add this function at the end of retriever.py
def get_embedder_and_index():
    return embedder, index

def get_highest_similarity_score(query, caller="Unknown"):
    unique_id = time.time()
    logger.info(f"[{unique_id}] Calculating similarity for query: {query}, Called by: {caller}")
    try:
        # Encode input
        query_embedding = embedder.encode(query)

        # Run search
        distances, _ = index.search(np.expand_dims(query_embedding, 0), 1)

        # Raw distance
        raw_distance = distances[0][0]
        logger.info(f"Raw distance for query '{query}': {raw_distance}")

        # Convert distance to similarity using different formulas
        # Formula 1: 1 / (1 + distance)
        similarity_score = 1 / (1 + raw_distance)

        # Formula 2: e^(-distance)
        similarity_score_2 = np.exp(-raw_distance)

        # Formula 3: 1 - distance
        similarity_score_3 = 1 - raw_distance

        # Log the calculated similarity scores
        logger.info(f"Calculated similarity scores for query '{query}':")
        logger.info(f"  Using Formula 1: {similarity_score}")
        logger.info(f"  Using Formula 2: {similarity_score_2}")
        logger.info(f"  Using Formula 3: {similarity_score_3}")

        # For now, return the similarity score calculated using the first formula
        return similarity_score
    except Exception as e:
        logger.error(f"Error in getting similarity score: {str(e)}")
        # Return -1 to indicate that an error occurred
        return -1


