import streamlit as st
from app import AdvancedCVBuilder, TemplateType, ContactInfo, Experience, Skill

st.set_page_config(page_title="AI CV Builder", layout="centered")

st.title("🎯 AI CV Builder")

# -------- INPUT --------
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
location = st.text_input("Location")

st.subheader("💼 Experience")
title = st.text_input("Job Title")
company = st.text_input("Company")
duration = st.text_input("Duration")
desc = st.text_area("Description (one per line)")

st.subheader("⭐ Skills")
skills_input = st.text_input("Skills (comma separated)")

# -------- GENERATE --------
if st.button("Generate CV 🚀"):

    builder = AdvancedCVBuilder()

    contact = ContactInfo(name, email, phone, location)

    experience = [
        Experience(
            title,
            company,
            duration,
            desc.split("\n")
        )
    ]

    skills = [Skill(s.strip(), "intermediate") for s in skills_input.split(",")]

    builder.cv_data = {
        "contact": contact,
        "experience": experience,
        "skills": skills,
        "summary": builder.generate_ai_summary(skills, experience),
    }

    html = builder.generate_cv(TemplateType.MODERN)

    # Save files
    with open("resume.html", "w") as f:
        f.write(html)
    st.download_button("📄 Download Resume (HTML)", html, file_name="resume.html")

    st.success("✅ CV Generated!")

    with open("resume.pdf", "rb") as f:
        st.download_button("📄 Download PDF", f, file_name="resume.pdf")
