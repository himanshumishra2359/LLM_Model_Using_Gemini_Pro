from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model_flash = genai.GenerativeModel('gemini-1.5-flash')
model_pro = genai.GenerativeModel('gemini-pro')

def get_gemini_response(input_text, image=None):
    if image is not None:
        model = model_flash  
        response = model.generate_content([input_text, image])  
    else:
        model = model_pro  
        response = model.generate_content(input_text)  
    return response.text


st.set_page_config(page_title="Gemini Application")

st.header("Gemini Q&A and Image Analysis")

input_text = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image...(Optional)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

submit = st.button("Submit")

if submit:
    if input_text or image:  
        response = get_gemini_response(input_text, image)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.error("Please provide either a question or an image.")
