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

# Page config
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📄", layout="wide")

# Tailwind-style gradient background only
html("""
<style>
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: linear-gradient(to top right, #ec4899, #8b5cf6, #06b6d4);
    background-size: 200% 200%;
    animation: bgShift 15s ease infinite;
    opacity: 0.12;
}

@keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Cover letter box styling */
.cover-letter-box {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    line-height: 1.6;
    font-size: 1rem;
    color: #1f2937;
    white-space: pre-wrap;
}
</style>
""", height=0)

# Title & intro
st.title("📄 AI Cover Letter Generator")
st.markdown("Generate professional, personalized cover letters using **AI**.\n\nCrafted by **Manjunathareddy** ✨")

# Inputs
st.subheader("📝 Provide Your Details")
job_description = st.text_area("**Enter the Job Description**", height=250)
resume_file = st.file_uploader("**Upload Your Resume (PDF only)**", type=["pdf"])

# PDF text extractor
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "".join([page.extract_text() or "" for page in pdf_reader.pages]).strip()

# Generate button
if st.button("🚀 Generate Cover Letter"):
    if not job_description or not resume_file:
        st.warning("⚠️ Please provide both the job description and resume.")
    else:
        with st.spinner("✍️ Generating your cover letter..."):
            try:
                resume_text = extract_text_from_pdf(resume_file)

                prompt = f"""
You are a professional career advisor and expert cover letter writer.

Generate a **professional, neatly formatted cover letter** using the candidate's resume and job description.

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
- Output should look **clean, professional, and aligned**

Only return the final cover letter.
"""

                response = model.generate_content(prompt)
                output = response.text.strip()

                st.success("✅ Cover Letter Generated!")
                st.subheader("📄 Your AI-Powered Cover Letter")

                # Styled box output
                st.markdown(f"<div class='cover-letter-box'>{output}</div>", unsafe_allow_html=True)

                # Download option
                st.download_button(
                    label="⬇️ Download Cover Letter as TXT",
                    data=output,
                    file_name="CoverLetter.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")
