import numpy as np
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from logger import setup_logger
import logging
import time
import nltk
from nltk.corpus import stopwords

# Initialize the set of stopwords
stop_words = set(stopwords.words('english'))

# Function to simplify queries by removing stop words

# Set up the logger
logger = setup_logger('retriever', level=logging.INFO)

# Initialize Persistent Chroma Client and other global variables only once
try:
    chroma_client = chromadb.PersistentClient(path="../Extracted_Data/Chroma_Db/ChromaDB")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = chroma_client.get_or_create_collection(name="mortgage_data", embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("ChromaDB collection loaded successfully")
except Exception as e:
    logger.exception("Error initializing ChromaDB client:")
    raise e

def simplify_query(query):
    query_words = query.split()
    simplified_query = ' '.join([word for word in query_words if word.lower() not in stop_words])
    return simplified_query

def retrieve(query, k=5):
    try:
        # Simplifying the query
        simplified_query = simplify_query(query)

        # Ensure the query is conducted on the Cleaned_Description column
        where_filter = {"column": "summarized_text"}

        # Convert query text to an embedding
        query_embedding = embedder.encode([query])[0].tolist()  # Convert NumPy array to list
        
        # Perform the query on the mortgage_data collection
        results = collection.query(
            query_embeddings=[query_embedding],  # Use the query embedding
            n_results=k,
            where=where_filter  # Apply the where filter
        )

        # Check for empty or unexpected results
        if not results or 'metadatas' not in results:
            logger.warning("Query returned empty or unexpected results")
            return []

        # Combine the Cleaned_Description and FAQ_Answers fields from the results
        combined_strings = [
            f"{res.get('Cleaned_Description', '')}. {res.get('FAQ_Answers', '')}" 
            for res in results['metadatas'][0]
        ]
        
        logger.info(f"Retrieved results for query: {simplified_query}")
        return combined_strings
        
    except Exception as e:
        logger.exception("Error in retrieval:")
        return []


def get_highest_similarity_score(query, caller="Unknown"):
    try:
        query_embedding = embedder.encode(query)
        
        results = collection.query(
            query_texts=[query],
            n_results=1
        )

        if results and 'distances' in results and results['distances']:
            raw_distance = results['distances'][0][0]
        else:
            logger.warning(f"No results found for the query: {query}")
            return -1

        logger.info(f"Raw distance for query '{query}': {raw_distance}")

        return raw_distance
    except Exception as e:
        logger.exception("Error in getting similarity score:")
        return -1