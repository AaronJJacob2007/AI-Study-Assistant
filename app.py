import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

st.set_page_config(page_title="AI Semester Companion", page_icon="🎓", layout="wide")


# Load environment variables
load_dotenv()

# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_content(prompt, spinner_text):
    try:
        with st.spinner(spinner_text):
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
        return response.text
    except Exception:
        return None


if "history" not in st.session_state:
    st.session_state.history = []

# Title
st.title("AI Semester Companion")
st.caption("Your AI-powered study assistant for college preparation")

st.sidebar.title("History")
if st.sidebar.button("Clear History"):
    st.session_state.history.clear()

for item in st.session_state.history:
    st.sidebar.write(item)

# Subject Selection
subject = st.selectbox("Select Subject", ["DSA", "DBMS", "OS", "CN", "Python"])

difficulty = st.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])


days_left = st.number_input("Days Until Exam", min_value=1, max_value=365, value=30)

# User Input
question = st.text_input("Enter a question or topic")

# -----------------------------
# Question Answering Feature
# -----------------------------
if st.button("Submit"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        prompt = f"""
You are a helpful {subject} tutor.

Answer as a teacher helping a college student.

Explain concepts at a {difficulty} level.

Question:
{question}
"""

        answer = generate_content(prompt, "Thinking...")

        if answer:
            st.write(answer)
            st.session_state.history.append(f"Question: {question}")
        else:
            st.error(
                "Gemini is currently busy. Please wait a few seconds and try again."
            )

# Divider
st.divider()

# -----------------------------
# Quiz Generator Feature
# -----------------------------
if st.button("Generate Quiz"):

    if not question.strip():
        st.warning("Please enter a topic for the quiz.")

    else:
        quiz_prompt = f"""
Generate 5 {difficulty} level multiple choice questions on {question}
for a college student studying {subject}.

For each question provide:

A)
B)
C)
D)

At the end provide the answer key.
"""

        answer = generate_content(quiz_prompt, "Generating Quiz...")

        if answer:
            st.write(answer)
            st.session_state.history.append(f"Quiz: {question}")

        else:
            st.error("Gemini is currently busy. Please try again later.")

st.divider()

if st.button("Generate Notes"):

    if not question.strip():
        st.warning("Please enter a topic for notes.")

    else:
        notes_prompt = f"""
Create structured study notes on {question}
for a college student studying {subject}
at a {difficulty} level.

Include:

1. Definition
2. Key Concepts
3. Important Points
4. Advantages
5. Disadvantages
6. Applications
7. Interview Questions
8. Quick Revision Summary

Use headings and bullet points.
"""

        answer = generate_content(notes_prompt, "Generating Notes...")

        if answer:
            st.write(answer)
            st.session_state.history.append(f"Notes: {question}")

        else:
            st.error("Gemini is currently busy. Please try again later.")

st.divider()

plan_type = st.selectbox("Study Plan Type", ["Topic", "Entire Subject"])

if st.button("Generate Study Plan"):

    if plan_type == "Topic":

        if not question.strip():
            st.warning("Please enter a topic for the study plan.")

        else:
            study_prompt = f"""
Create a detailed {days_left}-day study plan.

Subject: {subject}

Topic:
{question}

Difficulty Level:
{difficulty}

The plan should:

1. Divide study time logically
2. Include revision days
3. Include practice sessions
4. Be suitable for a college student
5. Be realistic and achievable

Present the plan day-by-day.
"""

            answer = generate_content(study_prompt, "Creating Study Plan...")

            if answer:
                st.write(answer)
                st.session_state.history.append(f"Study Plan: {question}")

            else:
                st.error("Gemini is currently busy. Please try again later.")

    else:

        study_prompt = f"""
Create a detailed {days_left}-day study plan
for the entire subject {subject}.

Difficulty Level:
{difficulty}

The plan should:

1. Cover all major concepts
2. Include revision days
3. Include practice sessions
4. Be suitable for a college student
5. Be realistic and achievable

Present the plan day-by-day.
"""

        answer = generate_content(study_prompt, "Creating Study Plan...")

        if answer:
            st.write(answer)
            st.session_state.history.append(f"Study Plan: {subject}")

        else:
            st.error("Gemini is currently busy. Please try again later.")
