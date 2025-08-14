from fastapi import FastAPI, Response
from fpdf import FPDF
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with ["https://lovable.dev"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Education(BaseModel):
    degree: str
    school: str
    location_dates: str

class Experience(BaseModel):
    job_title: str
    company: str
    location_dates: str
    bullet_points: List[str]

class ResumeData(BaseModel):
    name: str
    email: str
    phone: str
    website: str
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: str

class ResumePDF(FPDF):
    def __init__(self, resume_data: ResumeData):
        super().__init__(format='Letter')
        self.resume_data = resume_data

    def header(self):
        self.set_font("Helvetica", 'B', 14)
        self.set_x(18)
        self.cell(0, 10, self.resume_data.name or '', ln=True, align='L')
        self.set_font("Helvetica", '', 10)
        self.set_x(18)
        contact_info = f"{self.resume_data.email or ''} | {self.resume_data.phone or ''} | {self.resume_data.website or ''}"
        self.cell(0, 6, contact_info, ln=True, align='L')
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", 'B', 12)
        self.set_x(18)
        self.cell(0, 8, title or '', ln=True)
        self.ln(1)

    def job_entry(self, job_title, company, location_dates):
        self.set_x(18)
        self.set_font("Helvetica", 'B', 10)
        self.cell(0, 5, f"{job_title or ''} - {company or ''}", ln=True)
        self.set_x(18)
        self.set_font("Helvetica", '', 10)
        self.cell(0, 5, location_dates or '', ln=True)
        self.ln(1)

    def section_body(self, body):
        self.set_font("Helvetica", '', 10)
        self.set_x(18)
        self.multi_cell(0, 5, body or '')
        self.ln(1)

    def bullet_points(self, points):
        self.set_font("Helvetica", '', 10)
        for point in points or []:
            if point:
                self.set_x(18)
                self.multi_cell(0, 5, f"- {point}")
        self.ln(1)

def create_resume_pdf(resume_data: ResumeData):
    pdf = ResumePDF(resume_data)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_margins(18, 10, 18)
    pdf.add_page()

    try:
        print("⚙️ Adding summary...")
        pdf.section_title("PROFESSIONAL SUMMARY")
        pdf.section_body(resume_data.summary or '')

        print("📚 Adding education...")
        pdf.section_title("EDUCATION")
        for edu in resume_data.education or []:
            pdf.job_entry(edu.degree or '', edu.school or '', edu.location_dates or '')

        print("💼 Adding experience...")
        pdf.section_title("EXPERIENCE")
        for i, exp in enumerate(resume_data.experience or []):
            pdf.job_entry(exp.job_title or '', exp.company or '', exp.location_dates or '')
            pdf.bullet_points(exp.bullet_points or [])
            if i < len(resume_data.experience) - 1:
                pdf.ln(3)

        print("🧠 Adding skills...")
        pdf.section_title("SKILLS")
        pdf.section_body(resume_data.skills or '')

    except Exception as e:
        print("❌ Error while building PDF:", e)

    print("✅ PDF created.")
    return pdf.output(dest='S').encode('latin1')

@app.get("/")
def generate_resume():
    pdf_output = create_resume_pdf(default_resume_data)
    return Response(content=pdf_output, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=hayley_palensky_resume.pdf"
    })

@app.post("/generate")
def generate_custom_resume(resume_data: ResumeData):
    print("Received resume data:", resume_data)
    pdf_output = create_resume_pdf(resume_data)
    filename = f"{(resume_data.name or 'resume').lower().replace(' ', '_')}_resume.pdf"
    return Response(content=pdf_output, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })

# Default resume data for GET request
default_resume_data = ResumeData(
    name="Hayley Palensky",
    email="hayleyjopalensky@gmail.com",
    phone="515-451-0500",
    website="https://www.hayleypalensky.com",
    summary="UI/UX Designer with 3 years of experience in user-centric design and strategic marketing, seeking to leverage expertise in enhancing user engagement and traffic growth. Proven track record in website rebranding, UX design collaboration, and market analysis, achieving significant traffic increases. Skilled in Adobe Suite, Figma, wireframing, prototyping, and user research with a Master's in Experiential Design (UX/UI Focus).",
    education=[
        Education(degree="Master's in User Experience", school="Iowa State University", location_dates="Aug 2021 - May 2022"),
        Education(degree="Bachelor's in Marketing", school="Iowa State University", location_dates="Aug 2019 - May 2021")
    ],
    experience=[
        Experience(
            job_title="Marketing Specialist & Graphic Designer",
            company="HarvestIQ/Stockguard",
            location_dates="Remote | Apr 2022 - Mar 2025",
            bullet_points=[
                "Directed website rebranding efforts with user centered design, achieving a 300% increase in traffic and significantly enhancing user engagement.",
                "Redesigned digital ads that increased traffic by 10%, contributing to 35% of total site traffic within the first 90 days post-launch.",
                "Conducted market research and competitive analysis to inform strategic marketing decisions and optimize campaign effectiveness.",
                "Achieved a 135% year-over-year increase in traffic since launch through strategic design and SEO optimization.",
                "Delivered over 3.4 million impressions on Meta platforms over the course of a year, achieving an average frequency of 4.36 views per person to reinforce brand messaging and drive awareness."
            ]
        ),
        Experience(
            job_title="Marketing Intern",
            company="Workiva",
            location_dates="Ames, IA | Apr 2021 - Apr 2022",
            bullet_points=[
                "Analyzed sales pipeline data using HubSpot to identify opportunities and align insights with product goals.",
                "Updated content to enhance brand consistency and user engagement across marketing materials.",
                "Assisted in modifying the sales enablement platform to improve usability and streamline sales processes."
            ]
        ),
        Experience(
            job_title="Marketing Intern",
            company="Elizabeth Erin Designs",
            location_dates="Des Moines, IA | Apr 2020 - Jul 2020",
            bullet_points=[
                "Conducted competitor analysis to inform strategic design decisions, contributing to improved campaign effectiveness.",
                "Managed a marketing calendar for events and social media posts, enhancing engagement and maintaining design consistency through digital content and print ads."
            ]
        )
    ],
    skills="Adobe Suite, Figma, Prototyping, Wireframing, HTML, CSS, User Research, Mobile Design, Web Design, Hubspot, Jira, Microsoft Office Suite, Google Suite"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
