import streamlit as st
# Install Streamlit if not already installed
!pip install streamlit

import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# Load secrets
load_dotenv()
KEY = os.getenv("AZURE_TRANSLATOR_KEY")
ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
REGION = os.getenv("AZURE_TRANSLATOR_REGION")

# Supported languages
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
    "Korean": "ko"
}

# Translation function
def translate_text(text, to_lang):
    path = "/translate?api-version=3.0"
    params = f"&to={to_lang}"
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
        return response.json()[0]["translations"][0]["text"]
    except:
        return "⚠ Error in translation. Please check API settings."

# Streamlit UI
st.title("🌍 Multi-Language Translator (Azure API)")
st.write("Simple and fast translator using Azure Cognitive Services.")

text_input = st.text_area("Enter text to translate:")
target_language = st.selectbox("Select target language", list(LANGUAGES.keys()))

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text first.")
    else:
        translated = translate_text(text_input, LANGUAGES[target_language])
        st.success("Translation Successful:")
        st.write(translated)
