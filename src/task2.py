import json
import os
from MeetGenius_logger import logger
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import time 
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from config.path_manager import path_manager
from dotenv import load_dotenv
load_dotenv()

"""
task 2 : Agenda Creation
- in this task all content of the documents converted into chunks of text and than using HuggingFace Embeddings converted into vectors,
 all embeddings are stored in vector database for efficient retrieval.
 in later stage top 3 similar chunks to each discussion points are fetched and these all discussion points and their extra information feed to Gemini LLM
 that genrates agenda for the meeting.
"""


def split_document_content(file_path, words_per_chunk=70):
    """
    function to create chunks of the data
    """
    # Open and read the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Split the text into words
    words = text.split()
    
    chunks = [' '.join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]


    documents = []

    #all chunks are than converted in to langchain's Document formate for smooth storing in Pinecone database.
    for i, content in enumerate(chunks):
        doc = Document(page_content=content)
        documents.append(doc)
    logger.info("documents splited into chunks")
    return documents

def load_discussion_points(file_path):
    # Load list from a JSON file(discussion points)
    with open(file_path, "r") as file:
        discussion_points = json.load(file)
    logger.info("discussion points loaded")
    return discussion_points

def generate_agenda(discussion_points, vector_store):
    """
    takes discussion points and vector store as input 
    from the vector store fecth similar vectors for each discussion points 
    and than these whole data is passed with prompt to generate agenda in Google's Gemini LLM.

    """
    #llm configuration
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key = google_api_key)

    combined_input = ""

    for point in discussion_points:
        # Retrieve related documents for each discussion point

        results = vector_store.similarity_search(
            query = point,
            k=3
        )

        # Combine the discussion point with the related docs
        combined_input += f"Discussion Point: {point}\n"
        combined_input += "Related Information:\n"

        for res in results:
            combined_input += f"- {res.page_content}\n"
        combined_input += "\n"

    #prompt template for the agenda generation.
    prompt_template = PromptTemplate.from_template("""
        Generate a comprehensive meeting agenda based on the following meeting points. 
        Provide a clear and structured agenda in natural language, 
        Ensure the agenda is concise, well-organized, and directly reflects the provided input with time allocation for each points.

        Meeting Points: 
        {combined_input}
                                                   
        """)
    #langchain chain is used because it make adding of new components in future easy.
    chain = prompt_template | llm 

    response = chain.invoke({"combined_input" : combined_input})
    logger.info("agenda generated")
    return response

def initialize_vectore_database(documents, index_name):
    """
    takes input list of Documents(chunks) and name of index in which we want to store embeddings of documents.
    initialize the Pinecone vector database and add documents in it.
    at last it returns vector store.
    """
    
    #pinecone integration
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key = pinecone_api_key)

    #check whether index is already present in database otherwise it creates new index.
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name = index_name,
            dimension= 768,
            metric= "cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )

        while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)


    index = pc.Index(index_name)

    #initalize huggingface embeddings
    embeddings = HuggingFaceEmbeddings()
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    #generate unique ids for each documents
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store.add_documents(documents=documents, ids=uuids)

    logger.info("pinecone vector store invoked")
    return vector_store
     
def agenda_generation():
    """
    main driver functin for agenda geneartion
    that first all call the chunker function than load the discussion points 
    than initialize Pinecone and at last invoke the agenda generation chain.
    finally returns the genrated agenda
    """
    documents_content_file_path = path_manager.documents_content 
    discussion_points_file_path = path_manager.discussion_points
    
    index_name = "meeting-documents-embeddings"

    documents = split_document_content(documents_content_file_path)
    discussion_points = load_discussion_points(discussion_points_file_path)
    vector_store = initialize_vectore_database(documents, index_name)
    response = generate_agenda(discussion_points, vector_store)

    return response





