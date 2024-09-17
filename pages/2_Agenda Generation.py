import streamlit as st
from src import task2 

st.set_page_config(
    page_title="MeetGenius",
    page_icon="🤝",
    layout="wide"
)


# Set title and introduction
st.header("AI-Based Meeting Agenda Generator")

# Add some instructional text to engage users
st.subheader("""
This is your AI-powered agenda creation tool. Simply sit back, relax, and let the AI generate a well-structured agenda for you.
Please wait for a few seconds to see the magic unfold...
""")

# Generate the agenda using the AI task
response = task2.agenda_generation()

st.markdown(response)

