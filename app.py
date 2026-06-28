import streamlit as st
from dotenv import load_dotenv
import os
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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


def create_pdf(notes_text):

    pdf_file = "study_notes.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("<b>AI Semester Companion</b>", styles["Title"]))

    # Space
    content.append(Spacer(1, 12))

    # Subject
    content.append(Paragraph(f"<b>Subject:</b> {subject}", styles["Normal"]))

    # Difficulty
    content.append(Paragraph(f"<b>Difficulty:</b> {difficulty}", styles["Normal"]))

    content.append(Spacer(1, 20))

    for line in notes_text.split("\n"):
        line = line.strip()
        line = line.replace("**", "")
        line = line.replace("`", "")
        if line == "---":
         continue

        if not line:
            continue
        # Main Heading
        if line.startswith("#"):

          heading = line.lstrip("#").strip()

          content.append(
          Paragraph(
            f"<b>{heading}</b>",
            styles["Heading1"]
          )
        )

          content.append(Spacer(1, 8))
        
        # Bullet Points
        elif line.startswith("* "):
            bullet = line.replace("* ", "", 1)
            bullet = bullet.replace("*", "")

            content.append(Paragraph(f"• {line.replace('* ', '')}", styles["BodyText"]))
            content.append(Spacer(1,3))
        # Numbered Lists
        elif line[:2].isdigit() or (
            len(line) > 2 and line[0].isdigit() and line[1] == "."
        ):
            content.append(Paragraph(line, styles["BodyText"]))
            content.append(Spacer(1, 4))

        # Normal Text
        else:
            content.append(Paragraph(line, styles["BodyText"]))
            content.append(Spacer(1, 4))

    doc.build(content)

    return pdf_file


if "history" not in st.session_state:
    st.session_state.history = []

if "generated_notes" not in st.session_state:
    st.session_state.generated_notes = ""

if "generated_answer" not in st.session_state:
    st.session_state.generated_answer = ""

if "generated_quiz" not in st.session_state:
    st.session_state.generated_quiz = ""

if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = ""

# Title
st.title("AI Semester Companion")
st.caption("Your AI-powered study assistant for college preparation")

st.sidebar.title("History")
if st.sidebar.button("Clear History"):
    st.session_state.history.clear()

st.sidebar.write(f"Items: {len(st.session_state.history)}")


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
            st.session_state.generated_answer = answer
            st.session_state.history.append(f"Question: {question}")
        else:
            st.error(
                "Gemini is currently busy. Please wait a few seconds and try again."
            )
if st.session_state.generated_answer:

    with st.expander("📖 Answer", expanded=True):
        st.write(st.session_state.generated_answer)

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
            st.session_state.generated_quiz=answer
            st.session_state.history.append(f"Quiz: {question}")

        else:
            st.error("Gemini is currently busy. Please try again later.")

if st.session_state.generated_quiz:

    with st.expander("📝 Quiz", expanded=False):
        st.write(st.session_state.generated_quiz)

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
            st.session_state.generated_notes = answer
            st.session_state.history.append(f"Notes: {question}")
           

        else:
            st.error("Gemini is currently busy. Please try again later.")



if st.session_state.generated_notes:
    with st.expander("📚Notes",expanded=False):
        st.write(st.session_state.generated_notes)

        st.download_button(
            label="Download Notes (.txt)",
            data=st.session_state.generated_notes,
            file_name="study_notes.txt",
            mime="text/plain"
        )

        pdf_file = create_pdf(st.session_state.generated_notes)

        with open(pdf_file, "rb") as pdf:
            st.download_button(
            label="Download Notes (.pdf)",
            data=pdf,
            file_name="study_notes.pdf",
            mime="application/pdf",
        )

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
                st.session_state.generated_plan = answer
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
            st.session_state.generated_plan = answer
            st.session_state.history.append(f"Study Plan: {subject}")

        else:
            st.error("Gemini is currently busy. Please try again later.")

if st.session_state.generated_plan:

    with st.expander("📅 Study Plan", expanded=False):
        st.write(st.session_state.generated_plan)
