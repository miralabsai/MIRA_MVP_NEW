import os
import pickle
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n\s*\n', '\n', text)
    return text

def split_text(text, chunk_size=1000, overlap_size=100):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap_size)]

def main():
    # Load extracted texts 
    with open(os.path.join('ai_chat/Extracted_Data', 'extracted.pkl'), 'rb') as f:
        extracted_texts = pickle.load(f)

    print(f"Loaded {len(extracted_texts)} extracted texts")
    print(f"Sample extracted text (first 100 characters): {extracted_texts[0][:100]}...")

    # Print some additional samples from the extracted texts
    print(f"Sample extracted text (500-600 characters): {extracted_texts[0][500:600]}...")
    print(f"Sample extracted text (last 100 characters): {extracted_texts[0][-100:]}...")

    # Clean texts
    cleaned_texts = [clean_text(text) for text in extracted_texts]

    print(f"Sample cleaned text (first 100 characters): {cleaned_texts[0][:100]}...")
    print(f"Sample cleaned text (500-600 characters): {cleaned_texts[0][500:600]}...")
    print(f"Sample cleaned text (last 100 characters): {cleaned_texts[0][-100:]}...")

    # Split cleaned texts into chunks
    chunks = []
    doc_ids = []
    tokens_counts = []
    chunk_ids = []
    global_chunk_id = 0
    for doc_id, text in enumerate(cleaned_texts):
        for chunk in split_text(text):
            chunks.append(chunk)
            doc_ids.append(doc_id)
            tokens_counts.append(len(chunk.split()))
            chunk_ids.append(global_chunk_id)
            global_chunk_id += 1

    print(f"Generated {len(chunks)} chunks")
    print(f"Sample chunk (first 100 characters): {chunks[0][:100]}...")
    print(f"Sample chunk (500-600 characters): {chunks[0][500:600]}...")
    print(f"Sample chunk's token count: {tokens_counts[0]}")

    # Create a list of tuples (chunk_id, chunk, doc_id, tokens_count)
    chunks_ids_and_tokens = list(zip(chunk_ids, chunks, doc_ids, tokens_counts))

    # Save the list in a single pickle file
    with open(os.path.join('ai_chat/Extracted_data', 'chunks_ids_and_tokens.pkl'), 'wb') as f:
        pickle.dump(chunks_ids_and_tokens, f)

    # Save the chunks in a separate pickle file
    with open(os.path.join('ai_chat/Extracted_data', 'chunks.pkl'), 'wb') as f:
        pickle.dump(chunks, f)

    print("Preprocessed data pickled")

if __name__ == "__main__":
    main()
