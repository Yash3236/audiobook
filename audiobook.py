import streamlit as st
import pdfplumber
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

# Function to split text into chunks (max 5000 characters per request)
def split_text(text, max_length=5000):
    chunks = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind(" ")  # Split at the last space to avoid breaking words
        if split_index == -1:
            split_index = max_length  # If no space is found, force split at max_length
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)  # Add remaining text
    return chunks

# Function to translate large text
def translate_text(text, source_lang="auto", target_lang="hi"):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    chunks = split_text(text)
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    return " ".join(translated_chunks)  # Combine translated chunks

# Streamlit App Setup
st.set_page_config(page_title="PDF to Hindi Audiobook", layout="centered")
st.title("📖 PDF to Hindi Audiobook Converter 🇮🇳")

# Upload PDF File
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"

    if text.strip():
        st.success("✅ Text extracted successfully!")

        # Translate to Hindi (Handling Large Text)
        st.subheader("🌍 Translating to Hindi...")
        translated_text = translate_text(text)
        st.text_area("Translated Text (Hindi):", translated_text, height=300)

        # Convert to Speech
        if st.button("🎧 Convert to Hindi Audiobook"):
            audio_file = "hindi_audiobook.mp3"
            tts = gTTS(translated_text, lang="hi")
            tts.save(audio_file)

            st.audio(audio_file, format="audio/mp3")
            with open(audio_file, "rb") as f:
                st.download_button("⬇ Download Hindi Audiobook", f, file_name="hindi_audiobook.mp3")
    else:
        st.error("❌ No readable text found in the PDF.")
