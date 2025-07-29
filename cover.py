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

# Lottie animation
lottie_bg = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_9cyyl8i1.json")

# Page configuration
st.set_page_config(page_title="AI Cover Letter Generator by Manjureddy", page_icon="📄", layout="wide")

# Custom CSS with animated colorful background
html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

body {{
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}}

[data-testid="stAppViewContainer"] {{
    background: linear-gradient(135deg, #f9f9f9, #e0f7fa);
    animation: gradientShift 10s infinite ease-in-out alternate;
}}

@keyframes gradientShift {{
    0% {{ background: linear-gradient(135deg, #fceabb, #f8b500); }}
    50% {{ background: linear-gradient(135deg, #e0f7fa, #b2ebf2); }}
    100% {{ background: linear-gradient(135deg, #fceabb, #f8b500); }}
}}

.main .block-container {{
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    animation: fadeInUp 1.2s ease;
}}

textarea, .stTextInput, .stFileUploader, .stButton button {{
    border-radius: 12px;
}}

.stButton button {{
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    font-weight: 600;
    border: none;
}}

.stDownloadButton button {{
    border-radius: 12px;
    background: linear-gradient(to right, #43e97b, #38f9d7);
    color: white;
    font-weight: bold;
    border: none;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", height=0)

# Header layout
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        if lottie_bg:
            st_lottie(lottie_bg, height=280, speed=1)
        else:
            st.info("🎬 Animation not loaded.")
    with col2:
        st.title("📄 AI Cover Letter Generator")
        st.markdown("Create stunning, personalized cover letters in seconds using **Gemini 1.5 Flash**.\n\nCrafted for **Manjunathareddy** ✨")

# Inputs
st.subheader("📝 Provide Your Details")
job_description = st.text_area("Enter the Job Description", height=250)
resume_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])

# Extract resume text
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
        with st.spinner("✍️ Generating your cover letter..."):
            try:
                resume_text = extract_text_from_pdf(resume_file)

                prompt = f"""
You are a professional career advisor and expert cover letter writer.

Generate a professional cover letter using the candidate's resume and job description.

---

🧾 Candidate Name: Manjunathareddy  
📧 Email: manjukummathi@gmail.com  
📱 Phone: 630013836

---

🔹 Job Description:
{job_description}

🔹 Resume:
{resume_text}

---

✍️ Format:
- 3 to 4 short paragraphs
- Personalized and formal tone
- Greet with "Dear Hiring Manager"
- Use real insights from resume (not copied directly)
- Emphasize relevance to the role
- End with call-to-action and signature

---

Output only the final cover letter. Ready to send.
"""

                response = model.generate_content(prompt)
                output = response.text

                st.success("✅ Cover Letter Generated!")
                st.subheader("📄 Your AI-Powered Cover Letter")
                st.write(output)

                st.download_button(
                    label="⬇️ Download Cover Letter as TXT",
                    data=output,
                    file_name="CoverLetter.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
