import fitz  
from docx import Document
import re
import typesense
import os

client = typesense.Client({
    'nodes': [{
        'host': 'zesyao0hmni891d2p-1.a1.typesense.net',
        'port': '443',
        'protocol': 'https'
    }],
    'api_key': 'gFEXTdd67BicSxYxFnbWiJ9bDTccpW2K',
    'connection_timeout_seconds': 10 
})

def create_collection():
    schema = {
        'name': 'documents',
        'fields': [
            {'name': 'title', 'type': 'string'},
            {'name': 'author', 'type': 'string'},
            {'name': 'date', 'type': 'string'},
            {'name': 'content', 'type': 'string'}
        ]
    }
    try:
        client.collections.create(schema)
        print("Collection 'documents' created successfully")
    except Exception as e:
        print(f"error occurred in creation of collection: {e}")

def extract_from_pdf(pdf_path):
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
    except Exception as e:
        print(f"error while extracting text: {e}")
    return text

def extract_from_word(doc_path):
    text = ""
    try:
        document = Document(doc_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"error occurred while extracting text: {e}")
    return text

def extract_metadata(text):
    pattern = re.compile(r'title:\s*(.*?),\s*author:\s*(.*?),\s*date:\s*(.*?),\s*content:\s*(.*)')
    matches = pattern.findall(text)
    records = []
    for match in matches:
        record = {
            'title': match[0].strip(),
            'author': match[1].strip(),
            'date': match[2].strip(),
            'content': match[3].strip()
        }
        records.append(record)
    return records

def parse_and_index(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        text = extract_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        text = extract_from_word(file_path)
    else:
        raise ValueError(f"not supported file: {file_extension}")
    
    metadata = extract_metadata(text)
    if metadata:
        try:
            client.collections['documents'].documents.import_(metadata)
            print("Documents indexed successfully.")
        except Exception as e:
            print(f"error occurred while indexing documents: {e}")

if __name__ == "__main__":
    create_collection()
    file_path = 'example.pdf'  
    parse_and_index(file_path)

