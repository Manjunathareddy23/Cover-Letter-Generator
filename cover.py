import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
import google.generativeai as genai
from streamlit.components.v1 import html
from streamlit_lottie import st_lottie
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load Lottie animation safely
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# Load animation
lottie_bg = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_dyjl7fxv.json")

# Set page config
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📄", layout="wide")

# Custom CSS
html("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f0f2f6;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #e0eafc, #cfdef3);
    animation: fadeIn 1s ease-in-out;
}

.main .block-container {
    background-color: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    animation: slideUp 0.7s ease-out;
}

textarea, .stTextInput, .stFileUploader, .stButton button {
    border-radius: 12px;
}

.stButton button {
    background: linear-gradient(to right, #4facfe, #00f2fe);
    color: white;
    font-weight: 600;
    border: none;
}

.stDownloadButton button {
    border-radius: 12px;
    background: linear-gradient(to right, #43cea2, #185a9d);
    color: white;
    font-weight: bold;
    border: none;
}

@keyframes fadeIn {
    from { opacity: 0 }
    to { opacity: 1 }
}

@keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
</style>
""", height=0)

# App Header
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        if lottie_bg:
            st_lottie(lottie_bg, height=300, speed=1)
        else:
            st.markdown("🎬 *(Animation failed to load)*")
    with col2:
        st.title("📄 AI Cover Letter Generator")
        st.markdown("Craft personalized, formal cover letters from your resume & job descriptions using **Gemini 1.5 Flash**.")

# Input Section
st.subheader("📝 Provide Inputs")
job_description = st.text_area("Enter the Job Description", height=250)
resume_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

# PDF Text Extraction
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# Generate Cover Letter
if st.button("🚀 Generate Cover Letter"):
    if not job_description or not resume_file:
        st.warning("⚠️ Please provide both the job description and resume.")
    else:
        with st.spinner("🔍 Analyzing resume and generating cover letter..."):
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
- End with a call to action (e.g., "looking forward to the opportunity").

---

Generate the final cover letter below.
"""

                response = model.generate_content(prompt)
                output = response.text

                st.success("✅ Cover Letter Generated!")
                st.subheader("📄 Your AI-Powered Cover Letter")
                st.write(output)
                st.download_button("⬇️ Download as TXT", data=output, file_name="cover_letter.txt")

            except Exception as e:
                st.error(f"❌ Error: {e}")
