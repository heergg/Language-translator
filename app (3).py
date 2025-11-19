import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv, find_dotenv

# Load secrets
load_dotenv(find_dotenv())

KEY = os.getenv("AZURE_TRANSLATOR_KEY")
ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
REGION = os.getenv("AZURE_TRANSLATOR_REGION")

# Supported languages for output
LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-Hans",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
}

# Translation (Auto Detect Input Language)
def translate_text(text, to_lang):
    path = "/translate?api-version=3.0"
    params = f"&to={to_lang}"   # 👈 No "from=", so auto-detect works!
    constructed_url = ENDPOINT + path + params

    headers = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    body = [{"text": text}]
    response = requests.post(constructed_url, headers=headers, json=body)
    
    try:
        data = response.json()
        detected_lang = data[0]["detectedLanguage"]["language"]  # Auto-detected language
        translated_text = data[0]["translations"][0]["text"]
        return detected_lang, translated_text
    except:
        return None, "⚠ Error in translation."

# Streamlit UI
st.title("🌍 Multi-Language Translator (Azure API)")
st.write("Auto language detection enabled ✔")

text_input = st.text_area("Enter text to translate:")

target_language = st.selectbox("Select output language", list(LANGUAGES.keys()))

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text first.")
    else:
        detected, translated = translate_text(
            text_input,
            LANGUAGES[target_language]
        )
        
        if detected:
            st.info(f"Detected Language: **{detected.upper()}**")
        
        st.success("Translation:")
        st.write(translated)
