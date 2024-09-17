import streamlit as st

def main():
    
    st.set_page_config(page_title="MeetGenius", page_icon="🧠", layout="wide")

    with st.sidebar:
        st.markdown("The one-stop solution for the meeting life cycle🔁")

    # Header
    st.title("Welcome to MeetGenius 🧠")
    st.subheader("Your AI-powered meeting assistant", divider='rainbow')

    # Project Description
    st.header("About MeetGenius")
    st.write("""
    MeetGenius is an innovative tool designed to revolutionize the way organizations manage and document meetings. 
    By leveraging cutting-edge AI technologies, MeetGenius streamlines the entire meeting process from 
    preparation to follow-up, ensuring that every meeting is productive, well-documented, and actionable.
    
    Our platform addresses common pain points in meeting management, such as:
    - Lack of proper preparation and unclear agendas
    - Inefficient note-taking during discussions
    - Difficulty in tracking action items and decisions
    - Time-consuming post-meeting summary creation
   
    
    MeetGenius solves these issues by providing a comprehensive, AI-driven solution that covers the entire meeting lifecycle.
    """)

    # Key Features
    st.header("Key Features 🌟", divider="rainbow")
    
    st.subheader("1. Pre-Meeting Document Management", divider="gray")
    st.write("""
    - Upload and organize relevant documents before the meeting
    - Collaborative platform for participants to add discussion points
    """)

    st.subheader("2. Intelligent Agenda Creation", divider="gray")
    st.write("""
    - Automatic organization of discussion points into a logical flow
    - AI-driven time allocation suggestions for each agenda item
    - Smart linking of related topics to streamline the meeting flow
    - Generation of clear, concise meeting agendas with objectives and expected outcomes
    """)

    st.subheader("3. Meeting Recording and Real-Time Tracking", divider="gray")
    st.write("""
    - High-quality audio and video recording capabilities
    - The speech-to-text transcription for accurate documentation
    - AI-powered topic tracking to match discussions with agenda items
    - Automatic flagging of unresolved issues.
    """)

    st.subheader("4. Comprehensive Post-Meeting Summary", divider="gray")
    st.write("""
    - AI-generated detailed summaries of the entire meeting
    - Extraction and highlighting of key decisions made during the meeting
    - Clear listing of assigned action items with responsible participants
    """)


    # Technologies Used
    st.header("Powered by Advanced Technologies 🔬", divider="rainbow")
    st.write("""
    MeetGenius leverages state-of-the-art technologies to provide an unparalleled meeting management experience:

    1. **Large Language Models (LLMs)**:
       - Utilize advanced natural language processing for intelligent summarization
       - Extract key points, decisions, and action items with high accuracy
       - Generate meeting agendas and summaries

    2. **Retrieval-Augmented Generation (RAG)**:
       - Enhance LLM outputs with relevant context from your data
       - Improve the relevance and accuracy of AI-generated content

    3. **Vector Databases**:
       - Efficiently store and index meeting transcripts, summaries, and related documents
       - Enable semantic search capabilities for quick information retrieval

    4. **Speech-to-Text and Natural Language Understanding**:
       - Accurately transcribe meeting audio
       - Identify speakers and attribute statements correctly
       - Understand context, sentiment, and intent in spoken discussions

    """)



    # Footer
    st.markdown("---")
    st.write("© 2024 MeetGenius. All rights reserved. 🧠✨")

if __name__ == "__main__":
    main()