import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image as PILImage
import tempfile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Resume Builder PRO MAX", page_icon="📄", layout="centered")

st.markdown("""
<style>
.main-title {
    font-size:38px;
    font-weight:800;
    text-align:center;
    color:#1D4ED8;
}
.preview-box {
    background:#f3f4f6;
    padding:30px;
    border-radius:15px;
}
.section-title {
    color:#1D4ED8;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📄 Resume Builder PRO MAX</p>', unsafe_allow_html=True)
st.write("Modern 2-Column Professional Resume Generator 🚀")

# ---------------- INPUT SECTION ----------------

name = st.text_input("Full Name")
role = st.text_input("Professional Title")
location = st.text_input("Location")
phone = st.text_input("Phone")
email = st.text_input("Email")

st.subheader("Summary")
summary = st.text_area("Professional Summary")

st.subheader("Education")
education = st.text_area("Education Details")

st.subheader("Skills (comma separated)")
skills = st.text_input("Python, SQL, React, Leadership")

st.subheader("Experience")
experience = st.text_area("Work Experience")

st.subheader("Achievements")
achievements = st.text_area("Achievements")

photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])

# ---------------- LIVE PREVIEW ----------------

st.subheader("👀 Live Preview")

st.markdown('<div class="preview-box">', unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    if photo:
        st.image(photo, width=150)
    st.markdown("### Skills")
    if skills:
        for skill in skills.split(","):
            st.write("•", skill.strip())

with col2:
    st.markdown(f"# {name}")
    st.write(role)
    st.write(location)
    st.write(phone, "|", email)

    st.markdown("### Summary")
    st.write(summary)

    st.markdown("### Experience")
    st.write(experience)

    st.markdown("### Education")
    st.write(education)

    st.markdown("### Achievements")
    st.write(achievements)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PDF DOWNLOAD ----------------

if st.button("📥 Download Professional Resume PDF"):

    pdf_file = tempfile.NamedTemporaryFile(delete=False)
    doc = SimpleDocTemplate(pdf_file.name, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal = styles["Normal"]

    # Name
    elements.append(Paragraph(f"<b>{name}</b>", title_style))
    elements.append(Paragraph(role, normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Contact</b>", styles["Heading2"]))
    elements.append(Paragraph(f"{location}", normal))
    elements.append(Paragraph(f"{phone}", normal))
    elements.append(Paragraph(f"{email}", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(summary, normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    if skills:
        for skill in skills.split(","):
            elements.append(Paragraph(f"• {skill.strip()}", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Experience</b>", styles["Heading2"]))
    elements.append(Paragraph(experience, normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    elements.append(Paragraph(education, normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Achievements</b>", styles["Heading2"]))
    elements.append(Paragraph(achievements, normal))

    doc.build(elements)

    with open(pdf_file.name, "rb") as f:
        st.download_button("Click to Download Resume", f, file_name="Professional_Resume.pdf")
