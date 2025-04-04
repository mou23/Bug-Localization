import os
import json
import hashlib
from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-m3')

def count_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=False))

entity_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 0,
    length_function=count_tokens
)

def calculate_hash(content):
    content_bytes = content.encode('utf-8')
    hash_object = hashlib.sha256(content_bytes)
    hash_value = hash_object.hexdigest()
    return hash_value

def count_tokens(text):
    tokens = tokenizer.encode(text)
    number_of_tokens = len(tokens)
    return number_of_tokens

def get_chunks(entity):
    chunks = entity_splitter.split_text(entity)
    return chunks

def get_filename_from_path(fully_qualified_filename):
    return os.path.basename(fully_qualified_filename)

def save_data_to_json(retrieved_documents, retrieved_metadatas, retrieved_distances, output_file):
    output_dir = os.path.dirname(output_file)
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data_to_save = [
        {
            "document": doc,
            "metadata": meta,
            "distance": dist
        }
        for doc, meta, dist in zip(retrieved_documents, retrieved_metadatas, retrieved_distances)
    ]

    with open(output_file, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=4)