import os
import tempfile
import requests
from pytube import YouTube
from moviepy import VideoFileClip
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")


# -------------------------------
# 1. Download video from URL
# -------------------------------
def download_video(url: str) -> str:
    tmp_dir = tempfile.mkdtemp()
    out_path = os.path.join(tmp_dir, "video.mp4")

    # Handle YouTube URLs
    if "youtube.com" in url or "youtu.be" in url:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension="mp4", progressive=True).first()
        stream.download(output_path=tmp_dir, filename="video.mp4")
        return out_path

    # Otherwise treat as a direct video URL (e.g., MP4)
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(out_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return out_path


# -------------------------------
# 2. Extract audio from video
# -------------------------------
def extract_audio(video_path: str) -> str:
    audio_path = video_path.replace(".mp4", ".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path


# -------------------------------
# 3. Transcribe audio using Whisper API
# -------------------------------
def transcribe_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file,
            response_format="text"
        )
    return transcript


# -------------------------------
# 4. Analyze transcript with LLM
# -------------------------------
def analyze_transcript(transcript: str) -> dict:
    prompt = f"""
You are assessing spoken communication quality.

Transcript:
\"\"\"{transcript}\"\"\"

Return JSON with:
- clarity_score (0–100)
- communication_focus (one concise sentence)
"""

    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content
    return json.loads(reply)
