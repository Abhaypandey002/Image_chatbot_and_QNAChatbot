from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# Function to generate and play TTS
def text_to_speech(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    return "response.mp3"

st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

if submit:
    response = get_gemini_response(input, image)
    st.subheader("The Response is")
    st.write(response)

    # Convert response to speech
    audio_file = text_to_speech(response)
    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")
