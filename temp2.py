from moviepy.editor import VideoFileClip
from config.path_manager import path_manager


def vid_to_audio():
        video_clip = VideoFileClip("records/meeting_recordinf.mp4")
        video_clip.audio.write_audiofile("records/temp.mp3")


print(path_manager.meeting_transcript)

    
