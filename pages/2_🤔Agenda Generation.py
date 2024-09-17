import streamlit as st
from src import task2 
st.set_option('client.showErrorDetails', False)

st.set_page_config(
    page_title="MeetGenius",
    page_icon="🤝",
    layout="wide"
)

with st.sidebar:
    st.markdown("\n\n")
    st.markdown("A comprehensive agenda will be created by integrating the provided materials and discussion points. ")

# Set title and introduction
st.header("AI Based Meeting Agenda Generator", divider="rainbow")

# Add some instructional text to engage users
st.subheader("""
This is your AI-powered agenda creation tool. Simply sit back, relax, and let the AI generate a well-structured agenda for you.
Please wait for a few seconds to see the magic unfold...
""", divider="gray")

# Generate the agenda using the AI task
response = task2.agenda_generation()

st.markdown(response)

