from warnings import filterwarnings
filterwarnings("ignore")
from config.path_manager import path_manager
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

"""
Task 3 : Meeting Recording and Tracking:
- The user  has the option to record or upload the meeting's video, and when it has been done, extract the audio.
extracted audio, which the whisper model was then used to transform to text.
than using Langchain, which stores transcripts in vector stores after being translated into manageable pieces.
Here, the relevant portion of the transcript is retrieved using RAG in accordance with each discussion point, 
and it is then submitted to Gemini LLM along with prompt
and it keeps track of which discussion points have been and have not been discussed for each one.

"""


def initalize_vector_store(index_name, transcript):
    """
    initalize Pinecone vector database ans create new index for the embeddings of transcript
    than use recursive character splitter and stores in vector store 
    here it uses google embeddings because it is effective and currently free to use
    at last it converts vector database in to retiriever for future use in RAG.
    """

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

    # initialize google embeddings
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)


    #splits transcript in to chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 150,
        chunk_overlap  = 30)

    texts = text_splitter.split_text(transcript)
    docs = [Document(page_content=text) for text in texts]

    uuids = [str(uuid4()) for _ in range(len(docs))]

    #insets all documents into database.
    vector_store.add_documents(documents=docs, ids=uuids)
    retriever = vector_store.as_retriever()

    logger.info("vector database setup done & retriever created")
    return retriever

def discussion_point_checker(transcript, discussion_points_path):

    """
    this function create RAG to check whether the point was discussed or not in transcript.
    it create retrieval chain and find appropriate part using RAG method
    i have designed prompt such that llm answer either 'yes' or 'no' if point is discussed or not.
    at last return the list of discussed and undiscuees points.
    """

    #pinecone integration
    index_name = "meeting-transcript-embeddings"
    retriever = initalize_vector_store(index_name, transcript)


    """
    below is prompt that i have designed and pushed into langchain hub to make it reusable.

    system

    You are an AI assistant that reviews meeting transcripts and determines if a given discussion point was addressed. 
    Your job is to check whether the discussion point was explicitly discussed in the meeting. 
    Your response must be either "yes" or "no" with no additional explanation. 
    Base your answer strictly on the meeting transcript provided.

    <context>

    Meeting Transcript:

    {context}

    </context>

    human

    Here is the discussion point:

    {input}
    
    """

    prompt = hub.pull("krish-goyani/meeting_discussion_point_checker")

    # configure gemini LLM
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key = google_api_key)

    # RAG chain of LangChain
    combine_docs_chain = create_stuff_documents_chain(
        llm, prompt
    )

    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    #load the discussion points
    with open(discussion_points_path, "r") as f:
        discussion_points = json.load(f)

    
    #list of discussed points and undiscussed points
    discussed_points = []
    undiscussed_points = []
    
    # for each discussion point invoke the rag chain and take decision.
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

# Function to generate transcipt from audio
def transcriber(meeting_audio_path, transcript_file_name):
    """
    takes meeting_audio_path and where to store generated transcript.
    by using openai's whisper it generates transcript from audio file.
    """

    transcriber = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-small.en"
                )
    result = transcriber(meeting_audio_path)
    transcript = result['text']

    # save transcript
    with open(transcript_file_name, 'w') as file:
            
            file.write(transcript)
    
    logger.info("transcribe generated")
    return transcript

# Function to extract audio from the video
def extract_audio(video_file_path, meeting_audio_path):
    """
    takes path of video file and where to store extracted audio
    it uses moviepy library to extract audio from video
    """

    video_clip = VideoFileClip(video_file_path)
    video_clip.audio.write_audiofile(meeting_audio_path)
    logger.info("audio extracted from video")


def discussion_point_tracker(meeting_video_path):
    """
    main drive code to track the discussion points
    first of all call the audio extractor function than create transcript
    and than all points tracked using discussion_point_checker function.
    """
    meeting_audio_path = path_manager.meeting_audio
    discussion_points_path = path_manager.discussion_points
    transcript_file_name = path_manager.meeting_transcript
    
    extract_audio(meeting_video_path, meeting_audio_path)

    transcript = transcriber(meeting_audio_path, transcript_file_name)

    discussed_points, undiscussed_points = discussion_point_checker(transcript, discussion_points_path)

    return discussed_points, undiscussed_points