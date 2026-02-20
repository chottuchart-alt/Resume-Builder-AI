import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import HRFlowable
from reportlab.platypus import Frame
from reportlab.platypus import KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Builder PRO", page_icon="📄", layout="centered")

st.markdown("""
<style>
.main-title {
    font-size:36px;
    font-weight:700;
    text-align:center;
    color:#2563EB;
}
.section-box {
    background:#0f172a;
    padding:20px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📄 AI Resume Builder PRO (FREE)</p>', unsafe_allow_html=True)

st.write("Create modern professional resume instantly 🚀")

# ---------------- USER INPUT ----------------

name = st.text_input("Full Name")
role = st.text_input("Professional Title (Example: Python Developer)")
email = st.text_input("Email")
phone = st.text_input("Phone")
linkedin = st.text_input("LinkedIn URL")
github = st.text_input("GitHub URL")

st.subheader("Professional Summary")
summary = st.text_area("Write short professional summary")

st.subheader("Skills (comma separated)")
skills = st.text_input("Example: Python, SQL, React, Problem Solving")

st.subheader("Experience")
experience = st.text_area("Describe your experience")

st.subheader("Education")
education = st.text_area("Your education details")

photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])

# ---------------- AUTO BULLET GENERATOR ----------------

if st.button("✨ Generate Smart Bullet Points"):
    bullets = [
        "Developed scalable applications improving performance by 30%.",
        "Collaborated with cross-functional teams to deliver high-quality software.",
        "Optimized database queries reducing load time significantly.",
        "Implemented secure authentication systems.",
        "Built responsive UI improving user engagement."
    ]
    st.write("Suggested Points:")
    for b in bullets:
        st.write("•", b)

# ---------------- LIVE PREVIEW ----------------

st.subheader("👀 Resume Preview")

st.markdown("---")
st.markdown(f"## {name}")
st.write(role)
st.write(email, "|", phone)
st.write(linkedin)
st.write(github)

if photo:
    st.image(photo, width=120)

st.markdown("### Summary")
st.write(summary)

st.markdown("### Skills")
if skills:
    for skill in skills.split(","):
        st.write("•", skill.strip())

st.markdown("### Experience")
st.write(experience)

st.markdown("### Education")
st.write(education)

# ---------------- PDF GENERATOR ----------------

if st.button("📥 Download Resume as PDF"):

    pdf_file = tempfile.NamedTemporaryFile(delete=False)
    doc = SimpleDocTemplate(pdf_file.name, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"<b>{name}</b>", styles['Title']))
    elements.append(Paragraph(role, styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Contact</b>", styles['Heading2']))
    elements.append(Paragraph(email, styles['Normal']))
    elements.append(Paragraph(phone, styles['Normal']))
    elements.append(Paragraph(linkedin, styles['Normal']))
    elements.append(Paragraph(github, styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Summary</b>", styles['Heading2']))
    elements.append(Paragraph(summary, styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Skills</b>", styles['Heading2']))
    for skill in skills.split(","):
        elements.append(Paragraph(f"• {skill.strip()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Experience</b>", styles['Heading2']))
    elements.append(Paragraph(experience, styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Education</b>", styles['Heading2']))
    elements.append(Paragraph(education, styles['Normal']))

    doc.build(elements)

    with open(pdf_file.name, "rb") as f:
        st.download_button("Click to Download", f, file_name="resume.pdf")
