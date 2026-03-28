import streamlit as st
from app import AdvancedCVBuilder, TemplateType, ContactInfo, Experience, Skill

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Resume Builder", layout="centered")

# -------- TITLE --------
st.markdown("<h1 style='text-align:center;'>🚀 AI Resume Builder</h1>", unsafe_allow_html=True)
st.markdown("### Create professional resumes in seconds")

st.divider()

# -------- INPUT FORM --------
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

with col2:
    location = st.text_input("Location")
    title = st.text_input("Job Title")
    company = st.text_input("Company")

duration = st.text_input("Duration (e.g., 2022 - Present)")

desc = st.text_area("Experience Description (one per line)")

skills_input = st.text_input("Skills (comma separated)")

use_ai = st.checkbox("✨ Use AI Summary")

st.divider()

# -------- GENERATE BUTTON --------
if st.button("🚀 Generate Resume"):

    if not name or not email:
        st.error("⚠️ Please fill at least Name and Email")
    else:
        builder = AdvancedCVBuilder()

        contact = ContactInfo(name, email, phone, location)

        experience = [
            Experience(
                title,
                company,
                duration,
                desc.split("\n") if desc else []
            )
        ]

        skills = [Skill(s.strip(), "intermediate") for s in skills_input.split(",") if s.strip()]

        # -------- SUMMARY --------
        if use_ai:
            summary = builder.generate_ai_summary(skills, experience)
        else:
            summary = "Motivated professional with strong skills and experience."

        builder.cv_data = {
            "contact": contact,
            "experience": experience,
            "skills": skills,
            "summary": summary,
        }

        # -------- GENERATE HTML --------
        html = builder.generate_cv(TemplateType.MODERN)

        # -------- PREVIEW --------
        st.subheader("📄 Resume Preview")
        st.components.v1.html(html, height=600, scrolling=True)

        # -------- DOWNLOAD --------
        st.download_button(
            "📥 Download Resume (HTML)",
            html,
            file_name="resume.html",
            mime="text/html"
        )

        st.success("✅ Resume Generated Successfully!")
