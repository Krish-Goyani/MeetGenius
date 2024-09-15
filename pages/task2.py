import streamlit as st
import json
import os
from MeetGenius_logger import logger
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import time 
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document

from dotenv import load_dotenv
load_dotenv()

st.title("agenda creation")

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-mpnet-base-v2")

google_api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key = google_api_key)

def split_text_file(file_path, words_per_chunk=70):
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

for i, content in enumerate(chunks):
     doc = Document(page_content=content)
     

doc_embeddings = model.encode(chunks)
doc_embeddings = [embedding.tolist() for embedding in doc_embeddings]
#pinecone integration
from pinecone import Pinecone, ServerlessSpec
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key = pinecone_api_key)
index_name = "meeting-documents-embeddings"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name = index_name,
        dimension= 384,
        metric= "cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )

    while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)


index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

ids = [str(i) for i in range(len(doc_embeddings))]  # Generate unique string IDs for the sentences
vectors_to_upsert = list(zip(ids, doc_embeddings))
index.upsert(vectors=vectors_to_upsert) # L2 distance index
 # Add vectors to index

combined_input = ""

for point in discussion_points:
    # Retrieve related documents for each discussion point
    point_embedding = model.encode(point)
    point_embedding = point_embedding.tolist()

    result = index.query(quries = point_embedding, top_k=2)

    # Fetch related documents
    related_docs = [chunks[int(match['id'])] for match in result['matches']]

    # Combine the discussion point with the related docs
    combined_input += f"Discussion Point: {point}\n"
    combined_input += "Related Information:\n"

    for doc in related_docs:
        combined_input += f"- {doc}\n"
    combined_input += "\n"


prompt_template = PromptTemplate.from_template("""Generate a meeting agenda based on the following points: {combined_input}""")
chain = prompt_template | llm 

response = chain.invoke({"combined_input" : combined_input})
st.write(response)
