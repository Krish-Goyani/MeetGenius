import streamlit as st
from moviepy.editor import VideoFileClip
import os

transcript_path = "database/meeting_transcipt.mp3"
meeting_video_path = "database/meeting_video.mp4"

# Function to extract audio from the video
def extract_audio(video_file_path):
    video_clip = VideoFileClip(video_file_path)
    video_clip.audio.write_audiofile(transcript_path)
    return transcript_path



# Streamlit app
st.title("Meeting Recording and Tracking Tool")

# Step 1: Upload video file
video_file = st.file_uploader("Upload Meeting Video", type=["mp4", "mov", "avi"])

if video_file is not None:

    with open(meeting_video_path,"wb") as f:
        f.write(video_file.getvalue())
    # Step 2: Extract and process the video

    st.video(video_file)

    transcript_path = extract_audio(meeting_video_path)


    '''with st.spinner("Extracting audio from video..."):
        audio_file_path = extract_audio(video_save_path)'''
