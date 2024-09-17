import streamlit as st
import json
from  src import task1 
import os
from MeetGenius_logger import logger
from config.path_manager import path_manager
st.set_page_config(
    page_title="MeetGenius",
    page_icon="🤝",
    layout="wide"
)

ALLOWED_EXTENSIONS = ['txt', 'docx', 'pptx', 'pdf']

# Streamlit interface
st.header("Pre-Meeting Document Management",divider="rainbow")
st.write('''Please enter meeting related documents, like as presentations, word documents, and reports, before the meeting begins. 
         You should also include discussion points for the meeting.''')
with st.form(key = "form"):
    
    # Step 1: Add Discussion Points
    st.subheader("Add Discussion Points")
    discussion_points = st.text_area("Enter your discussion points (make sure new point will be in new line)", height=200)
        
    # Step 2: Upload Meeting Documents
    st.subheader("Upload Relevant Documents")
    uploaded_files = st.file_uploader("Upload files (txt, docx, pptx, pdf)", type=ALLOWED_EXTENSIONS, accept_multiple_files=True)

    submitted = st.form_submit_button("Submit")

    if submitted:

        logger.info("files and discussion points uploaded")

        documents_content = task1.pre_process_documents(uploaded_files)
        discussion_points = [x.strip() for x in discussion_points.split("\n")]
        
        os.makedirs(path_manager.local_database, exist_ok=True)
        with open(path_manager.discussion_points, "w") as file:
            json.dump(discussion_points, file)

        with open(path_manager.documents_content, "w") as file:
            file.write(documents_content)

        st.success("Thank you. You may now proceed to the next phase, where the agenda will be created based on your discussion points and the documents. ")

        logger.info("cleaned version of files and discussion points saved")
        




