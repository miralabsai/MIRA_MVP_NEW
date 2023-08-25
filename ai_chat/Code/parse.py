import os
import PyPDF2
import pickle
from logger import setup_logger  # Import the logger setup function
import logging  # Import the logging module

# Set up the logger
logger = setup_logger('parse', level=logging.INFO)

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
        logger.info(f"Processed {pdf}")  # Log informational message
    except PyPDF2.errors.PdfReadError:
        logger.error(f"Error processing {pdf}. Possibly corrupted or invalid PDF.")  # Log error
        continue

os.makedirs('ai_chat/Extracted_data', exist_ok=True)
pickle.dump(extracted_texts, open('ai_chat/Extracted_data/extracted.pkl', 'wb'))

logger.info(f"Successfully processed {len(extracted_texts)} out of {len(pdfs)} PDFs and saved the extracted data.")  # Log informational message
