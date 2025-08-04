from fastapi import FastAPI, Response
from fpdf import FPDF

app = FastAPI()

class ResumePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 14)
        self.set_x(18)
        self.cell(0, 10, "Hayley Palensky", ln=True, align='L')
        self.set_font("Helvetica", '', 10)
        self.set_x(18)
        self.cell(0, 6, "hayleyjopalensky@gmail.com | 515-451-0500 | https://www.hayleypalensky.com", ln=True, align='L')
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", 'B', 12)
        self.set_x(18)
        self.cell(0, 8, title, ln=True)
        self.ln(1)

    def job_entry(self, job_title, company, location_dates):
        self.set_x(18)
        self.set_font("Helvetica", 'B', 10)
        self.cell(0, 5, f"{job_title} - {company}", ln=True)
        self.set_x(18)
        self.set_font("Helvetica", '', 10)
        self.cell(0, 5, location_dates, ln=True)
        self.ln(1)

    def section_body(self, body):
        self.set_font("Helvetica", '', 10)
        self.set_x(18)
        self.multi_cell(0, 5, body)
        self.ln(1)

    def bullet_points(self, points):
        self.set_font("Helvetica", '', 10)
        for point in points:
            self.set_x(18)
            self.multi_cell(0, 5, f"- {point}")
        self.ln(1)

@app.get("/")
def generate_resume():
    pdf = ResumePDF(format='Letter')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_margins(18, 10, 18)
    pdf.add_page()

    # Summary
    pdf.section_title("PROFESSIONAL SUMMARY")
    pdf.section_body(
        "UI/UX Designer with 3 years of experience in user-centric design and strategic marketing, seeking to leverage "
        "expertise in enhancing user engagement and traffic growth. Proven track record in website rebranding, UX design "
        "collaboration, and market analysis, achieving significant traffic increases. Skilled in Adobe Suite, Figma, "
        "wireframing, prototyping, and user research with a Master's in Experiential Design (UX/UI Focus)."
    )

    # Education
    pdf.section_title("EDUCATION")
    pdf.job_entry("Master's in User Experience", "Iowa State University", "Aug 2021 - May 2022")
    pdf.job_entry("Bachelor's in Marketing", "Iowa State University", "Aug 2019 - May 2021")

    # Experience
    pdf.section_title("EXPERIENCE")

    pdf.job_entry("Marketing Specialist & Graphic Designer", "HarvestIQ/Stockguard", "Remote | Apr 2022 - Mar 2025")
    pdf.bullet_points([
        "Directed website rebranding efforts with user centered design, achieving a 300% increase in traffic and significantly enhancing user engagement.",
        "Redesigned digital ads that increased traffic by 10%, contributing to 35% of total site traffic within the first 90 days post-launch.",
        "Conducted market research and competitive analysis to inform strategic marketing decisions and optimize campaign effectiveness.",
        "Achieved a 135% year-over-year increase in traffic since launch through strategic design and SEO optimization.",
        "Delivered over 3.4 million impressions on Meta platforms over the course of a year, achieving an average frequency of 4.36 views per person to reinforce brand messaging and drive awareness.",
    ])
    pdf.ln(3)

    pdf.job_entry("Marketing Intern", "Workiva", "Ames, IA | Apr 2021 - Apr 2022")
    pdf.bullet_points([
        "Analyzed sales pipeline data using HubSpot to identify opportunities and align insights with product goals.",
        "Updated content to enhance brand consistency and user engagement across marketing materials.",
        "Assisted in modifying the sales enablement platform to improve usability and streamline sales processes."
    ])
    pdf.ln(3)

    pdf.job_entry("Marketing Intern", "Elizabeth Erin Designs", "Des Moines, IA | Apr 2020 - Jul 2020")
    pdf.bullet_points([
        "Conducted competitor analysis to inform strategic design decisions, contributing to improved campaign effectiveness.",
        "Managed a marketing calendar for events and social media posts, enhancing engagement and maintaining design consistency through digital content and print ads."
    ])

    # Skills
    pdf.section_title("SKILLS")
    pdf.section_body("Adobe Suite, Figma, Prototyping, Wireframing, HTML, CSS, User Research, Mobile Design, Web Design, Hubspot, Jira, Microsoft Office Suite, Google Suite")

    pdf_output = pdf.output(dest='S').encode('latin1')
    return Response(content=pdf_output, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=hayley_palensky_resume.pdf"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
