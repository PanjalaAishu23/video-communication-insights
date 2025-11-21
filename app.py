import streamlit as st
from processing import (
    download_video,
    extract_audio,
    transcribe_audio,
    analyze_transcript
)

st.set_page_config(page_title="Video Communication Insights")

st.title("🎥 Video Communication Insights")
st.write("Enter a public video URL to analyze clarity and communication quality.")


# -------------------------------
# Input
# -------------------------------
video_url = st.text_input("Video URL (YouTube or direct MP4 link):")

if st.button("Analyze Video"):

    if not video_url:
        st.error("Please enter a valid URL.")
        st.stop()

    # Download video
    with st.spinner("📥 Downloading video..."):
        video_path = download_video(video_url)

    # Extract audio
    with st.spinner("🎧 Extracting audio..."):
        audio_path = extract_audio(video_path)

    # Transcribe audio
    with st.spinner("🔊 Transcribing audio..."):
        transcript = transcribe_audio(audio_path)

    # Analyze transcript
    with st.spinner("🧠 Analyzing communication..."):
        results = analyze_transcript(transcript)

    # Display results
    st.success("Analysis Complete!")

    st.subheader("Results")
    st.write(f"**Clarity Score:** {results.get('clarity_score', 'N/A')}%")
    st.write(f"**Communication Focus:** {results.get('communication_focus', 'N/A')}")

    st.subheader("Transcript")
    st.write(transcript)
