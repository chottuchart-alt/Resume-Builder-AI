import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import io

st.set_page_config(page_title="AI Resume Builder PRO", page_icon="📄", layout="centered")

st.title("📄 AI Resume Builder PRO (Free Version)")
st.write("Create modern resume instantly 🚀")

# ---------------- TEMPLATE SWITCHER ----------------
template = st.selectbox(
    "Select Resume Template",
    ["Modern Blue", "Minimal Black", "Professional Gray"]
)

# ---------------- USER INPUT ----------------
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
summary = st.text_area("Career Summary")

skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Experience Description")
education = st.text_area("Education Details")

# ---------------- AUTO BULLET GENERATOR ----------------
def generate_bullets(text):
    lines = text.split("\n")
    bullets = []
    for line in lines:
        if line.strip():
            bullets.append("• " + line.strip().capitalize())
    return bullets

# ---------------- PDF GENERATOR ----------------
def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # TEMPLATE STYLING
    if template == "Modern Blue":
        heading_color = colors.HexColor("#1E3A8A")
    elif template == "Minimal Black":
        heading_color = colors.black
    else:
        heading_color = colors.grey

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading1'],
        textColor=heading_color,
        fontSize=18,
        spaceAfter=10
    )

    normal_style = styles["Normal"]

    # NAME
    elements.append(Paragraph(name, heading_style))
    elements.append(Paragraph(f"{email} | {phone}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # SUMMARY
    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(summary, normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # SKILLS
    elements.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    skill_list = skills.split(",")
    skill_bullets = [ListItem(Paragraph(skill.strip(), normal_style)) for skill in skill_list]
    elements.append(ListFlowable(skill_bullets, bulletType='bullet'))
    elements.append(Spacer(1, 0.2 * inch))

    # EXPERIENCE
    elements.append(Paragraph("<b>Experience</b>", styles["Heading2"]))
    exp_bullets = generate_bullets(experience)
    exp_list = [ListItem(Paragraph(item, normal_style)) for item in exp_bullets]
    elements.append(ListFlowable(exp_list, bulletType='bullet'))
    elements.append(Spacer(1, 0.2 * inch))

    # EDUCATION
    elements.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    elements.append(Paragraph(education, normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- DOWNLOAD BUTTON ----------------
if st.button("🚀 Generate Resume PDF"):
    if name:
        pdf = create_pdf()
        st.download_button(
            label="📥 Download Resume",
            data=pdf,
            file_name="resume.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please enter your name.")
