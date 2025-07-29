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

# Streamlit page config
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📄", layout="wide")

# Inject CSS animated background and theme
html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600;800&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(270deg, #00c9ff, #92fe9d, #ff9a9e, #fad0c4, #fbc2eb);
    background-size: 1000% 1000%;
    animation: gradientShift 20s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main .block-container {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 3rem;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    animation: fadeInUp 1.2s ease;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

textarea, .stTextInput, .stFileUploader, .stButton button {
    border-radius: 12px;
    font-weight: 500;
}

.stButton button {
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: linear-gradient(to right, #0072ff, #00c6ff);
}

.stDownloadButton button {
    border-radius: 12px;
    background: linear-gradient(to right, #43e97b, #38f9d7);
    color: white;
    font-weight: bold;
    border: none;
}
</style>
""", height=0)

# App title
st.title("📄 AI Cover Letter Generator")
st.markdown("Create stunning, personalized cover letters using **Gemini 1.5 Flash**.\n\nCrafted by **Manjunathareddy** ✨")

# Input section
st.subheader("📝 Provide Your Details")
job_description = st.text_area("**Enter the Job Description**", height=250)
resume_file = st.file_uploader("**Upload Your Resume (PDF only)**", type=["pdf"])

# Resume text extractor
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# Cover letter generator
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
