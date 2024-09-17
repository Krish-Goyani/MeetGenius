import streamlit as st
from config.path_manager import path_manager
from src import task3
import av
import streamlit as st
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import time
st.set_option('client.showErrorDetails', False)

# Streamlit app with a more engaging title
st.title("Meeting Recording and Tracking Tool")


if "final_discussed_points" not in st.session_state:
    st.session_state.final_discussed_points = []

if "final_undiscussed_points" not in st.session_state:
    st.session_state.final_undiscussed_points = []

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

option = st.radio(label="Select appropriate option to continue",
         options=['Record the meeting', 'Upload the meeting video'],
         index=None,
         horizontal=True
         )


if option == "Upload the meeting video" :
    meeting_video_path = path_manager.meeting_video
    
    # Step 1: Upload video file with more detailed instructions
    st.write("""
    Welcome to the AI-powered tool that helps you analyze your meeting videos and track discussed vs. undiscussed points.
    Simply upload a video file, and let the AI and RAG do the rest!
    """)

    # Allow the user to upload a meeting video
    video_file = st.file_uploader("Upload Your Meeting Video", type=["mp4"])

    if video_file is not None:
        # Save the file to the local directory
        with open(meeting_video_path, "wb") as f:
            f.write(video_file.getvalue())
        
        # Display the uploaded video in the app
        st.video(video_file)
        
        # Run the AI-based function to track discussion points
        discussed_points, undiscussed_points = task3.discussion_point_tracker(meeting_video_path)
        st.session_state.analyzed = True

        if st.session_state.analyzed == True:
            final_discussed_points = st.session_state.final_discussed_points
            final_discussed_points.extend(discussed_points)
            final_discussed_points = list(set(final_discussed_points))

            final_undiscussed_points = st.session_state.final_undiscussed_points
            final_undiscussed_points.extend(undiscussed_points)
            final_undiscussed_points = list(set(final_undiscussed_points))
            final_undiscussed_points = [point for point in final_undiscussed_points if point not in final_discussed_points]

            col1, col2 = st.columns(2)
            # Column 1: Display Discussed Points
            with col1:
                st.header("Discussed Points")
                
                if len(final_discussed_points) == 0:
                    st.write("All points were undiscussed.")
                else  :
                    st.markdown("<ul>", unsafe_allow_html=True)  # Start of bullet list
                    for point in final_discussed_points:
                        st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)  # Each item in the list
                    st.markdown("</ul>", unsafe_allow_html=True)  # End of bullet list
                    

            # Column 2: Display Undiscussed Points
            with col2:
                st.header("Undiscussed Points")

                if len(final_undiscussed_points) == 0:
                    st.write("All the points were discussed.")
                else:
                    st.markdown("<ul>", unsafe_allow_html=True)  # Start of bullet list
                    for point in final_undiscussed_points:
                        st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)  # Each item in the list
                    st.markdown("</ul>", unsafe_allow_html=True)  # End of bullet list

                


elif option == "Record the meeting":
    
    live_meeting_recording_path = path_manager.live_meeting_recording

    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        return frame

    def in_recorder_factory() -> MediaRecorder:
        return MediaRecorder(
            str(live_meeting_recording_path), format="mp4"
        )  

    webrtc_streamer(
        key="record",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={
            "video": True,
            "audio": True,
        },
        video_frame_callback=video_frame_callback,
        in_recorder_factory=in_recorder_factory
    )

    bt = st.button(label = "Track the progress")

    if bt:
        time.sleep(3)
        # Run the AI-based function to track discussion points
        discussed_points, undiscussed_points = task3.discussion_point_tracker(live_meeting_recording_path)
        st.session_state.analyzed = True

        if st.session_state.analyzed == True:
            final_discussed_points = st.session_state.final_discussed_points
            final_discussed_points.extend(discussed_points)
            final_discussed_points = list(set(final_discussed_points))

            final_undiscussed_points = st.session_state.final_undiscussed_points
            final_undiscussed_points.extend(undiscussed_points)
            final_undiscussed_points = list(set(final_undiscussed_points))
            final_undiscussed_points = [point for point in final_undiscussed_points if point not in final_discussed_points]

            col1, col2 = st.columns(2)
            # Column 1: Display Discussed Points
            with col1:
                st.header("Discussed Points")
                
                if len(final_discussed_points) == 0:
                    st.write("All points were undiscussed.")
                else  :
                    st.markdown("<ul>", unsafe_allow_html=True)  # Start of bullet list
                    for point in final_discussed_points:
                        st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)  # Each item in the list
                    st.markdown("</ul>", unsafe_allow_html=True)  # End of bullet list
                    

            # Column 2: Display Undiscussed Points
            with col2:
                st.header("Undiscussed Points")

                if len(final_undiscussed_points) == 0:
                    st.write("All the points were discussed.")
                else:
                    st.markdown("<ul>", unsafe_allow_html=True)  # Start of bullet list
                    for point in final_undiscussed_points:
                        st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)  # Each item in the list
                    st.markdown("</ul>", unsafe_allow_html=True)  # End of bullet list

                


else :
    while True:
        st.session_state.analyzed = False
        pass

