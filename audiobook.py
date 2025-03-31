import streamlit as st
import pdfplumber
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

# Set up Streamlit App
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

        # Translate to Hindi using deep-translator
        st.subheader("🌍 Translating to Hindi...")
        translator = GoogleTranslator(source="auto", target="hi")
        translated_text = translator.translate(text)
        st.text_area("Translated Text (Hindi):", translated_text, height=200)

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
