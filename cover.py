import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
import google.generativeai as genai
from streamlit.components.v1 import html

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Page setup
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📄", layout="centered")

# Custom CSS for neumorphism style
html(
    """
    <style>
    body {
        background: linear-gradient(145deg, #e6e6e6, #ffffff);
        font-family: 'Poppins', sans-serif;
    }
    .main .block-container {
        background: #f2f2f2;
        border-radius: 12px;
        box-shadow: 5px 5px 15px #cfcfcf,
                    -5px -5px 15px #ffffff;
        padding: 2rem;
    }
    textarea, .stTextInput, .stFileUploader, .stButton button {
        border-radius: 12px;
    }
    .stButton button {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
        font-weight: bold;
    }
    .stDownloadButton button {
        border-radius: 12px;
        background: linear-gradient(to right, #43cea2, #185a9d);
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    height=0
)

st.title("📄 AI Cover Letter Generator (Gemini 1.5 Flash)")
st.markdown("Generate a professional cover letter using your resume and job description.")

# Inputs
job_description = st.text_area("🧾 Job Description", height=250)
resume_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# Generate cover letter
if st.button("🚀 Generate Cover Letter"):
    if not job_description or not resume_file:
        st.warning("⚠️ Please provide both the job description and resume.")
    else:
        with st.spinner("🧠 Reading resume and generating cover letter..."):
            try:
                resume_text = extract_text_from_pdf(resume_file)

                prompt = f"""
You are a professional career coach and expert cover letter writer.

Your task is to generate a concise, highly personalized, and formal cover letter based on the information below.

---

🔹 Job Description:
{job_description}

🔹 Resume Text:
{resume_text}

---

🎯 Objectives:
- Tailor the cover letter to the job description.
- Highlight the candidate's most relevant skills, achievements, and experience.
- Demonstrate how the applicant fits the job role and company culture.
- Include a compelling introduction and a strong closing paragraph.
- Maintain a professional, polite, and enthusiastic tone.
- Keep the length between 250–300 words.

📌 Format:
- Start with a proper greeting (e.g., Dear Hiring Manager).
- Use paragraph structure (typically 3–4 concise paragraphs).
- Do **not** repeat the resume verbatim.
- Focus on value, alignment, and intent.
- End with a call to action (e.g., \"looking forward to the opportunity\").

---

Generate the final cover letter below.
"""

                response = model.generate_content(prompt)
                output = response.text

                st.success("✅ Cover Letter Generated!")
                st.subheader("📄 AI-Powered Cover Letter")
                st.write(output)

                st.download_button("⬇️ Download as TXT", data=output, file_name="cover_letter.txt")

            except Exception as e:
                st.error(f"❌ Error: {e}")
