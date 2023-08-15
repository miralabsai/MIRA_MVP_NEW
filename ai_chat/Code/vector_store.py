import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from logger import setup_logger

# Define the log directory relative to the project root
log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
log_file_path = os.path.join(log_directory, 'vector_store_logger.log')

# Ensure the directory exists
os.makedirs(log_directory, exist_ok=True)

# Set up the logger
logger = setup_logger('vector_store_logger', log_file_path)

try:
    # Load data
    logger.info("Loading data...")
    with open('ai_chat/Extracted_Data/chunks_ids_and_tokens.pkl', 'rb') as f:
        chunk_ids, chunks, doc_ids, tokens_counts = zip(*pickle.load(f))

    # Generate embeddings
    logger.info("Generating embeddings...")
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    doc_embeddings = embedder.encode(chunks)

    # Infer the dimension from the generated embeddings
    dimension = len(doc_embeddings[0])

    # FAISS parameters
    index = faiss.IndexFlatL2(dimension)  # Use a flat L2 index for simplicity

    # Add vectors to FAISS index
    index.add(np.array(doc_embeddings))

    # Check if the directory exists and create it if necessary
    if not os.path.exists('ai_chat/Extracted_data'):
        os.makedirs('ai_chat/Extracted_data')

    # Save the index to a file
    faiss.write_index(index, 'ai_chat/Extracted_data/faiss_index.bin')

    logger.info(f"{len(doc_ids)} document embeddings saved!")
except Exception as e:
    logger.error(f"Error encountered: {str(e)}")
