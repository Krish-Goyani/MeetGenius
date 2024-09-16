from warnings import filterwarnings
filterwarnings("ignore")
from moviepy.editor import VideoFileClip
from transformers import pipeline
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub
import time
from langchain_core.documents.base import Document
import json
import os
from uuid import uuid4
from MeetGenius_logger import logger
from dotenv import load_dotenv
load_dotenv()


def initalize_vector_store(index_name, transcript):

    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key = pinecone_api_key)

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

    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 150,
        chunk_overlap  = 30)

    texts = text_splitter.split_text(transcript)
    docs = [Document(page_content=text) for text in texts]

    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=uuids)
    retriever = vector_store.as_retriever()

    logger.info("vector database setup done & retriever created")
    return retriever

def discussion_point_checker(transcript, discussion_points_path):

    #pinecone integration
    index_name = "meeting-transcript-embeddings"
    retriever = initalize_vector_store(index_name, transcript)


    prompt = hub.pull("krish-goyani/meeting_discussion_point_checker")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key = google_api_key)

    combine_docs_chain = create_stuff_documents_chain(
        llm, prompt
    )

    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    with open(discussion_points_path, "r") as f:
        discussion_points = json.load(f)

    
    discussed_points = []
    undiscussed_points = []
    for point in discussion_points:
        response = retrieval_chain.invoke({"input" : point})

        response = response['answer']

        if response.lower().strip() == "yes":
            discussed_points.append(point)
            

        else :
            undiscussed_points.append(point)
        time.sleep(2)

    logger.info("discussed and undiscussed points classified")
    return discussed_points, undiscussed_points

def transcriber(meeting_audio_path, transcript_file_name):
    transcriber = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-small.en"
                )

    result = transcriber(meeting_audio_path)
    with open(transcript_file_name, 'w') as file:
            file.write(result['text'])

    logger.info("transcribe generated")
    return result['text']
# Function to extract audio from the video
def extract_audio(video_file_path,meeting_audio_path):

    video_clip = VideoFileClip(video_file_path)
    video_clip.audio.write_audiofile(meeting_audio_path)
    logger.info("audio extracted from video")


def discussion_point_tracker():
    meeting_audio_path = "database/meeting_audio.mp3"
    meeting_video_path = "database/meeting_video.mp4"
    discussion_points_path = "database/discussion_points.json"
    transcript_file_name = 'database/meeting_transcript.txt'

    extract_audio(meeting_video_path, meeting_audio_path)

    transcript = transcriber(meeting_audio_path, transcript_file_name)

    discussed_points, undiscussed_points = discussion_point_checker(transcript, discussion_points_path)

    return discussed_points, undiscussed_points