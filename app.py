import json
import re
import os
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path
from groq import Groq


# ---------------- ENUM ----------------
class TemplateType:
    MODERN = "modern"
    ATS_FRIENDLY = "ats_friendly"


# ---------------- DATA CLASSES ----------------
@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str
    location: Optional[str] = None


@dataclass
class Experience:
    title: str
    company: str
    duration: str
    description: List[str]


@dataclass
class Skill:
    name: str
    level: str


# ---------------- MAIN CLASS ----------------
class AdvancedCVBuilder:
    def __init__(self, groq_api_key=None):
        self.templates = {
            TemplateType.MODERN: self._modern_template,
            TemplateType.ATS_FRIENDLY: self._ats_template,
        }

        self.cv_data = {}
        self.client = Groq(api_key=groq_api_key) if groq_api_key else None

    # -------- AI SUMMARY --------
    def generate_ai_summary(self, skills, experience):
        if not self.client:
            return "Motivated professional with strong technical and problem-solving skills."

        prompt = f"""
        Write a professional resume summary.
        Skills: {', '.join([s.name for s in skills])}
        Experience: {[e.title for e in experience]}
        """

        try:
            res = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
            )
            return res.choices[0].message.content.strip()
        except:
            return "Experienced professional with strong skills."

    # -------- INPUT --------
    def collect_data(self):
        print("📞 Enter Contact Info")
        contact = ContactInfo(
            name=input("Name: "),
            email=input("Email: "),
            phone=input("Phone: "),
            location=input("Location: "),
        )

        print("\n💼 Add Experience")
        experiences = []
        while input("Add experience? (y/n): ").lower() == "y":
            desc = []
            print("Enter description (type 'done'):")
            while True:
                d = input()
                if d == "done":
                    break
                desc.append(d)

            experiences.append(
                Experience(
                    input("Title: "),
                    input("Company: "),
                    input("Duration: "),
                    desc,
                )
            )

        print("\n⭐ Skills (comma separated)")
        skills = [Skill(s.strip(), "intermediate") for s in input().split(",")]

        summary = self.generate_ai_summary(skills, experiences)

        self.cv_data = {
            "contact": contact,
            "experience": experiences,
            "skills": skills,
            "summary": summary,
        }

    # -------- HTML GENERATION --------
    def generate_cv(self, template):
        return self.templates[template]()

    # -------- MODERN TEMPLATE --------
    def _modern_template(self):
        c = self.cv_data["contact"]

        exp_html = ""
        for e in self.cv_data["experience"]:
            exp_html += f"""
            <h3>{e.title} - {e.company}</h3>
            <p>{e.duration}</p>
            <ul>
                {''.join(f"<li>{d}</li>" for d in e.description)}
            </ul>
            """

        skills = ", ".join([s.name for s in self.cv_data["skills"]])

        return f"""
        <html>
        <body>
        <h1>{c.name}</h1>
        <p>{c.email} | {c.phone} | {c.location}</p>

        <h2>Summary</h2>
        <p>{self.cv_data['summary']}</p>

        <h2>Experience</h2>
        {exp_html}

        <h2>Skills</h2>
        <p>{skills}</p>
        </body>
        </html>
        """

    # -------- ATS TEMPLATE --------
    def _ats_template(self):
        c = self.cv_data["contact"]
        return f"""
        <html><body>
        <h1>{c.name}</h1>
        <p>{c.email} | {c.phone}</p>
        <p>{self.cv_data['summary']}</p>
        </body></html>
        """

    # -------- EXPORT --------
 
# ---------------- MAIN FUNCTION ----------------
def main():
    print("🎯 AI CV BUILDER\n")

    groq_key = input("Enter Groq API key (or press Enter): ")

    builder = AdvancedCVBuilder(groq_key if groq_key else None)

    builder.collect_data()

    print("\nChoose Template:")
    print("1. Modern")
    print("2. ATS")

    choice = input("Choice: ")
    template = TemplateType.MODERN if choice == "1" else TemplateType.ATS_FRIENDLY

    html = builder.generate_cv(template)

    print("\nExport:")
    print("1. PDF")
    print("2. HTML")

    export = input("Choice: ")

    if export == "1":
        builder.export_pdf(html, "resume")
    else:
        builder.export_html(html, "resume")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
