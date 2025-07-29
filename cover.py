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

# Inject CSS + 3D particles background (HTML + JS)
html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}

canvas#bg-canvas {
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

.main .block-container {
    background-color: rgba(255, 255, 255, 0.92);
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    animation: fadeInUp 1.2s ease;
}

textarea, .stTextInput, .stFileUploader, .stButton button {
    border-radius: 12px;
}

.stButton button {
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    font-weight: 600;
    border: none;
}

.stDownloadButton button {
    border-radius: 12px;
    background: linear-gradient(to right, #43e97b, #38f9d7);
    color: white;
    font-weight: bold;
    border: none;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>

<canvas id="bg-canvas"></canvas>
<script>
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray = [];

class Particle {
  constructor(){
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size = Math.random() * 2 + 1;
    this.speedX = Math.random() * 1 - 0.5;
    this.speedY = Math.random() * 1 - 0.5;
  }

  update(){
    this.x += this.speedX;
    this.y += this.speedY;

    if(this.x < 0 || this.x > canvas.width) this.speedX *= -1;
    if(this.y < 0 || this.y > canvas.height) this.speedY *= -1;
  }

  draw(){
    ctx.fillStyle = 'rgba(0, 190, 255, 0.7)';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

function init(){
  particlesArray = [];
  for (let i = 0; i < 150; i++){
    particlesArray.push(new Particle());
  }
}

function animate(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < particlesArray.length; i++){
    particlesArray[i].update();
    particlesArray[i].draw();
  }
  requestAnimationFrame(animate);
}

window.addEventListener('resize', () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  init();
})

init();
animate();
</script>
""", height=0)

# App header
st.title("📄 AI Cover Letter Generator")
st.markdown("Create stunning, personalized cover letters using **Gemini 1.5 Flash**.\n\nCrafted for **Manjunathareddy** ✨")

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
                    file_name="Manjunathareddy_CoverLetter.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
