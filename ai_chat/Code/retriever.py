import numpy as np
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from logger import setup_logger
import logging
import time

# Set up the logger
logger = setup_logger('retriever', level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

# Initialize Persistent Chroma Client and other global variables only once
try:
    chroma_client = chromadb.PersistentClient(path="../Extracted_Data/Chroma_Db")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = chroma_client.get_or_create_collection(name="mortgage_data", embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("ChromaDB collection loaded successfully")
except Exception as e:
    logger.exception("Error initializing ChromaDB client:")
    raise e

# New retrieve function that accepts intents and entities
def retrieve_by_intent_and_entities(intents, entities, k=5, column=None):
    try:
        logger.debug(f"About to call retriever. Intents: {intents}, Type: {type(intents)}")
        logger.debug(f"About to call retriever. Entities: {entities}, Type: {type(entities)}")

        # Check if entities are an iterable type and if they are empty
        if not isinstance(entities, (list, tuple, set)):
            logger.error("Entities should be of iterable types like list, tuple or set.")
            return []

        # Filter out None or empty strings from entities
        filtered_entities = list(filter(None, entities))

        # Check if entities are empty
        if not filtered_entities:
            logger.warning("Entities are empty.")
            return []

        # Create the query string based on entities
        query_string = ' '.join(filtered_entities)
        
        logger.debug(f"Generated query string for ChromaDB: {query_string}")

        where_filter = {"column": column} if column else None

        results = collection.query(
            query_texts=[query_string],
            n_results=k,
            where=where_filter
        )

        if not results or 'metadatas' not in results:
            logger.warning("Query returned empty or unexpected results")
            return []

        combined_strings = [f"{res.get('Cleaned_Description', '')}. {res.get('FAQ_Answers', '')}" for res in results['metadatas'][0]]
        logger.info(f"Retrieved results for query: {query_string}")
        
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
