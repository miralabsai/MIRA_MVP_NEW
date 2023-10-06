# user_input.py
from retriever import retrieve, get_highest_similarity_score, initialize_retriever
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('user_input')

# Initialize the retriever to make sure index and embedder are available
initialize_retriever()

# Define a threshold for similarity. Adjust based on your data and testing.
SIMILARITY_THRESHOLD = 0.10

def get_user_input():
    while True:
        # Get user input
        user_input = input("Enter your question: ")
        logger.info(f"Received user input: {user_input}")

        # Check the highest similarity score for the user input
        similarity_score = get_highest_similarity_score(user_input)
        logger.info(f"Similarity score for input: {similarity_score}")

        if similarity_score < SIMILARITY_THRESHOLD:
            # Retrieve the top 2 most similar chunks
            results = retrieve(user_input, k=2)
            logger.info(f"Retrieved results for input: {results}")

            # Print the results
            for result in results:
                print(result)
        else:
            print("Sorry, I can only assist with mortgage-related questions at this time.")
            logger.warning(f"Input did not meet similarity threshold: {user_input}")

if __name__ == "__main__":
    get_user_input()
