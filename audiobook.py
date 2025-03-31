import streamlit as st
import pdfplumber
from gtts import gTTS
import os

# Set up the app
st.set_page_config(page_title="PDF to Audiobook", layout="centered")
st.title("📖 PDF to Audiobook Converter")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    if text.strip():
        st.success("✅ Text extracted successfully!")

        # Convert text to speech
        if st.button("🎧 Convert to Audiobook"):
            audio_file = "audiobook.mp3"
            tts = gTTS(text, lang="en")
            tts.save(audio_file)

            st.audio(audio_file, format="audio/mp3")
            with open(audio_file, "rb") as f:
                st.download_button("⬇ Download MP3", f, file_name="audiobook.mp3")
    else:
        st.error("❌ No readable text found in the PDF.")

