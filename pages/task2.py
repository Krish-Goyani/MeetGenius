import streamlit as st
import faiss
from sentence_transformers import SentenceTransformer
import json


st.title("agenda creation")

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def split_text_file(file_path, words_per_chunk=80):
    # Open and read the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into words
    words = text.split()

    # Group the words into chunks of specified size (100 words by default)
    chunks = [' '.join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]

    return chunks

def load_discussion_points(file_path):
    # Load list from a JSON file
    with open(file_path, "r") as file:
        discussion_points = json.load(file)
    return discussion_points


documents_content_file_path = 'database\documents_content.txt'  
discussion_points_file_path = "database\discussion_points.json"

chunks = split_text_file(documents_content_file_path)
discussion_points = load_discussion_points(discussion_points_file_path)

doc_embeddings = model.encode(chunks)


index = faiss.IndexFlatL2(doc_embeddings.shape[1])  # L2 distance index
index.add(doc_embeddings)  # Add vectors to index

combined_input = ""

for point in discussion_points:
    # Retrieve related documents for each discussion point
    point_embedding = model.encode(point)
    D, I = index.search(point_embedding.reshape(1, -1), k=2)

    # Fetch related documents
    related_docs = [chunks[i] for i in I[0]]

    # Combine the discussion point with the related docs
    combined_input += f"Discussion Point: {point}\n"
    combined_input += "Related Information:\n"
    for doc in related_docs:
        combined_input += f"- {doc}\n"
    combined_input += "\n"

print(combined_input)
