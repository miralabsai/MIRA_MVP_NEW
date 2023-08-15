import os
import PyPDF2
import pickle

data_dir = 'ai_chat/Data/Knowledgebase'

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        page_text = page.extract_text()
        text += page_text
    return text

pdfs = os.listdir(data_dir)

extracted_texts = []
for pdf in pdfs:
    pdf_path = os.path.join(data_dir, pdf)
    try:
        with open(pdf_path, 'rb') as f:
            text = extract_text(f)
            extracted_texts.append(text)
        print(f"Processed {pdf}")
    except PyPDF2.errors.PdfReadError:
        print(f"Error processing {pdf}. Possibly corrupted or invalid PDF.")
        continue

os.makedirs('ai_chat/Extracted_data', exist_ok=True)
pickle.dump(extracted_texts, open('ai_chat/Extracted_data/extracted.pkl', 'wb'))

print(f"Successfully processed {len(extracted_texts)} out of {len(pdfs)} PDFs and saved the extracted data.")
