import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Title
st.title(" AI Semester Companion")

# Subject Selection
subject = st.selectbox(
    "Select Subject",
    ["DSA", "DBMS", "OS", "CN", "Python"]
)

difficulty = st.selectbox(
    "Select Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)


days_left = st.number_input(
    "Days Until Exam",
    min_value=1,
    max_value=365,
    value=30
)

# User Input
question = st.text_input("Enter a question or topic")

# -----------------------------
# Question Answering Feature
# -----------------------------
if st.button(" Submit"):

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

        try:
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.write(response.text)

        except Exception:
            st.error(
                "Gemini is currently busy. Please wait a few seconds and try again."
            )

# Divider
st.divider()

# -----------------------------
# Quiz Generator Feature
# -----------------------------
if st.button(" Generate Quiz"):

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

        try:
            with st.spinner("Generating Quiz..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=quiz_prompt
                )

            st.write(response.text)

        except Exception:
            st.error(
                "Gemini is currently busy. Please try again later."
            )

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

        try:
            with st.spinner("Generating Notes..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=notes_prompt
                )

            st.write(response.text)

        except Exception:
            st.error(
                "Gemini is currently busy. Please try again later."
            )

st.divider()

plan_type = st.selectbox(
    "Study Plan Type",
    ["Topic", "Entire Subject"]
)

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

            try:
                with st.spinner("Creating Study Plan..."):

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=study_prompt
                    )

                st.write(response.text)

            except Exception:
                st.error(
                    "Gemini is currently busy. Please try again later."
                )

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

        try:
            with st.spinner("Creating Study Plan..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=study_prompt
                )

            st.write(response.text)

        except Exception:
            st.error(
                "Gemini is currently busy. Please try again later."
            )