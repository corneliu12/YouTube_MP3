import streamlit as st
from pytubefix import YouTube
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("🎬 YouTube Video Downloader & MP3 Converter")

# Input: YouTube URL
url = st.text_input("Enter YouTube URL")

# Global paths
VIDEO_FILE = "downloaded_video.mp4"
SHORT_CLIP = "short_clip.mp4"
AUDIO_FILE = "audio.mp3"

# Download and preview button
if st.button("Download and Preview"):
    if not url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        try:
            st.info("Downloading video...")
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            video_path = stream.download(filename=VIDEO_FILE)
            st.success(f"Downloaded: {yt.title}")

            st.info("Generating 10-second preview...")
            clip = VideoFileClip(video_path)
            clip.subclip(0, 10).write_videofile(SHORT_CLIP, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            st.video(SHORT_CLIP)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Convert to MP3
if os.path.exists(VIDEO_FILE):
    if st.button("🎵 Convert to MP3"):
        try:
            st.info("Converting to MP3...")
            clip = VideoFileClip(VIDEO_FILE)
            clip.audio.write_audiofile(AUDIO_FILE, verbose=False, logger=None)
            st.success("MP3 conversion complete!")
            audio_bytes = open(AUDIO_FILE, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')
            st.download_button("⬇️ Download MP3", audio_bytes, file_name="audio.mp3", mime="audio/mp3")
        except Exception as e:
            st.error(f"Error during conversion: {e}")

# Cleanup button
if st.button("🗑️ Clean Up Files"):
    try:
        for f in [VIDEO_FILE, SHORT_CLIP, AUDIO_FILE]:
            if os.path.exists(f):
                os.remove(f)
        st.success("All files deleted.")
    except Exception as e:
        st.error(f"Error deleting files: {e}")
