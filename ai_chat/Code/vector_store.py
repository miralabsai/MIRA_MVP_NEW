import os
import numpy as np
import pandas as pd
import faiss
import pickle  # Add this import for pickle
from sentence_transformers import SentenceTransformer
import logging

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('vector_store')

def main():
    try:
        # Load data
        logger.info("Loading data...")
        excel_path = 'ai_chat/Data/Knowledgebase/Merged_Master_Fannie_Freddie_Final.xlsx'
        df = pd.read_excel(excel_path)

        # Combine all columns into a single text chunk
        df['all_text'] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
        chunks = df['all_text'].tolist()

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
        output_dir = 'ai_chat/Extracted_data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the index to a file
        faiss.write_index(index, os.path.join(output_dir, 'faiss_index.bin'))

        # Save chunks to a pickle file
        with open(os.path.join(output_dir, 'chunks.pkl'), 'wb') as f:
            pickle.dump(chunks, f)

        logger.info(f"{len(chunks)} document embeddings and text chunks saved!")

    except Exception as e:
        logger.error(f"Error encountered: {str(e)}")

if __name__ == "__main__":
    main()
