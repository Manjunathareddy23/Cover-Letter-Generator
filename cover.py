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

# Tailwind-style inspired gradient background
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
    opacity: 0.15;
}

@keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
""", height=0)

# Title & intro
st.title("📄 AI Cover Letter Generator")
st.markdown("Generate professional, personalized cover letters using **Gemini 1.5 Flash**.\n\nCrafted by **Manjunathareddy** ✨")

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
                st.error(f"❌ Error: {e}")
