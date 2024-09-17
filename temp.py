import uuid
from pathlib import Path
import av
import cv2
import streamlit as st
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from moviepy.editor import VideoFileClip


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:

    return frame


RECORD_DIR = Path("./records")
RECORD_DIR.mkdir(exist_ok=True)


def app():
    if "prefix" not in st.session_state:
        st.session_state["prefix"] = str(uuid.uuid4())
    prefix = st.session_state["prefix"]
    in_file = RECORD_DIR / "meeting_recordinf.mp4"

    def in_recorder_factory() -> MediaRecorder:
        return MediaRecorder(
            str(in_file), format="mp4"
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

    if in_file.exists():
        with in_file.open("rb") as f:
            st.download_button(
                "Download the recorded video without video filter", f, "input."
            )

def vid_to_audio():
        video_clip = VideoFileClip("records/meeting_recordinf.mp4")
        video_clip.audio.write_audiofile("records/temp.mp3")

if __name__ == "__main__":
    app()