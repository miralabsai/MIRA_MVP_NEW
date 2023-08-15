import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

try:
    # Load data
    with open('ai_chat/Extracted_Data/chunks_ids_and_tokens.pkl', 'rb') as f:
        chunk_ids, chunks, doc_ids, tokens_counts = zip(*pickle.load(f))

    # Generate embeddings  
    print("Generating embeddings...")
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

    print(f"{len(doc_ids)} document embeddings saved!")
except Exception as e:
    print(f"Error encountered: {str(e)}")
