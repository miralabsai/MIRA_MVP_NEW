# user_input.py

from retriever import retrieve, get_highest_similarity_score

def get_user_input():
    # Define a threshold for similarity. You may need to adjust this based on your data and embeddings.
    SIMILARITY_THRESHOLD = 0.50  # Example threshold; you might need to adjust this value based on testing
    
    while True:
        # Get user input
        user_input = input("Enter your question: ")

        # Check the highest similarity score for the user input
        similarity_score = get_highest_similarity_score(user_input)
        
        if similarity_score >= SIMILARITY_THRESHOLD:
            # Use the retrieve function to get the top 2 most similar chunks
            results = retrieve(user_input, k=2)

            # Print the results
            for result in results:
                print(result)
        else:
            print("Sorry, I can only assist with mortgage-related questions at this time.")

if __name__ == "__main__":
    get_user_input()
