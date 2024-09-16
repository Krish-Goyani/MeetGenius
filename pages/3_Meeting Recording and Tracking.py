import streamlit as st
import time  # Import time to add a delay for a better user experience
from src import task3

# Streamlit app with a more engaging title
st.title("Meeting Recording and Tracking Tool")

# Step 1: Upload video file with more detailed instructions
st.write("""
Welcome to the AI-powered tool that helps you analyze your meeting videos and track discussed vs. undiscussed points.
Simply upload a video file, and let the AI and RAG do the rest!
""")

# Allow the user to upload a meeting video
video_file = st.file_uploader("Upload Your Meeting Video", type=["mp4"])

if video_file is not None:
    # Save the uploaded video file to a specific path
    meeting_video_path = "database/meeting_video.mp4"
    
    # Save the file to the local directory
    with open(meeting_video_path, "wb") as f:
        f.write(video_file.getvalue())
    
    # Display the uploaded video in the app
    st.video(video_file)
    
    
    # Run the AI-based function to track discussion points
    discussed_points, undiscussed_points = task3.discussion_point_tracker()
    
    # Display the results with proper headings
    st.success("Analysis Complete!")

    col1, col2 = st.columns(2)
    # Column 1: Display Discussed Points
    with col1:
        st.header("Discussed Points")
        
        if len(discussed_points) == 0:
            st.write("All points were undiscussed.")
        else  :
            st.markdown("<ul>", unsafe_allow_html=True)  # Start of bullet list
            for point in discussed_points:
                st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)  # Each item in the list
            st.markdown("</ul>", unsafe_allow_html=True)  # End of bullet list
            

    # Column 2: Display Undiscussed Points
    with col2:
        st.header("Undiscussed Points")

        if len(undiscussed_points) == 0:
            st.write("All the points were discussed.")
        else:
            st.markdown("<ul>", unsafe_allow_html=True)  # Start of bullet list
            for point in undiscussed_points:
                st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)  # Each item in the list
            st.markdown("</ul>", unsafe_allow_html=True)  # End of bullet list

            