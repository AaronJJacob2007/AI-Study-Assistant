import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.title("AI Semester Companion")
question=st.text_input("Ask a question")

if st.button("Submit"):
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )
    st.write(response.text)
