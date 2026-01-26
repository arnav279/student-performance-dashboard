from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUTPUT_PATH = Path("Minor_Project_Progress_Report_Styled_v2.docx")


def run_props(size=24, bold=False):
    parts = [
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>',
        f'<w:sz w:val="{size}"/>',
        f'<w:szCs w:val="{size}"/>',
    ]
    if bold:
        parts.append("<w:b/>")
    return "".join(parts)


def paragraph(text="", *, size=24, bold=False, align="both", before=0, after=120, page_break=False, indent=0):
    if page_break:
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    if text == "":
        return '<w:p/>'
    escaped = escape(text)
    indent_xml = f'<w:ind w:left="{indent}"/>' if indent else ""
    return (
        f'<w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:before="{before}" w:after="{after}" '
        f'w:line="360" w:lineRule="auto"/>{indent_xml}</w:pPr>'
        f'<w:r><w:rPr>{run_props(size=size, bold=bold)}</w:rPr>'
        f'<w:t xml:space="preserve">{escaped}</w:t></w:r></w:p>'
    )


def bullet(text):
    return (
        '<w:p><w:pPr><w:jc w:val="both"/><w:spacing w:after="80" w:line="360" w:lineRule="auto"/>'
        '<w:ind w:left="720" w:hanging="360"/></w:pPr>'
        f'<w:r><w:rPr>{run_props(size=24, bold=False)}</w:rPr><w:t xml:space="preserve">• </w:t></w:r>'
        f'<w:r><w:rPr>{run_props(size=24, bold=False)}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
    )


def title(text):
    return paragraph(text, size=30, bold=True, align="center", before=120, after=180)


def heading(text):
    return paragraph(text, size=28, bold=True, align="left", before=180, after=120)


def subheading(text):
    return paragraph(text, size=24, bold=True, align="left", before=120, after=80)


def table(rows, widths=None):
    if not widths:
        widths = [2400] * len(rows[0])
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs = []
    for row_index, row in enumerate(rows):
        cells = []
        for cell in row:
            fill = ' w:fill="D9E2F3"' if row_index == 0 else ""
            cells.append(
                '<w:tc>'
                f'<w:tcPr><w:tcW w:w="0" w:type="auto"/><w:shd w:val="clear" w:color="auto"{fill}/></w:tcPr>'
                f'{paragraph(cell, size=22, bold=row_index == 0, align="left", after=60)}'
                '</w:tc>'
            )
        trs.append(f'<w:tr>{"".join(cells)}</w:tr>')
    return (
        '<w:tbl>'
        '<w:tblPr><w:tblW w:w="0" w:type="auto"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '</w:tblBorders></w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>'
        f'{"".join(trs)}'
        '</w:tbl>'
    )


def build_document():
    parts = []

    parts += [
        title("MINOR PROJECT PROGRESS REPORT"),
        paragraph("on", align="center", after=80),
        title("AI-Powered Student Performance Assessment and Analytics Dashboard"),
        paragraph("Submitted in partial fulfillment of the requirements for PBL-3 End Term Assessment", align="center", after=200),
        paragraph("Submitted by:", bold=True, align="center"),
        paragraph("Your Name", align="center"),
        paragraph("Registration Number: Your Registration Number", align="center"),
        paragraph("Under the Guidance of:", bold=True, align="center", before=120),
        paragraph("Project Guide Name", align="center"),
        paragraph("Department of Computer Science and Engineering", align="center", before=200),
        paragraph("School of Computer Science and Engineering", align="center"),
        paragraph("Manipal University Jaipur, Jaipur", align="center"),
        paragraph("Academic Session: 2024-2025", align="center", before=120),
        paragraph("Semester: VI", align="center"),
    ]

    parts += [
        paragraph(page_break=True),
        title("CERTIFICATE"),
        paragraph('This is to certify that the project entitled "AI-Powered Student Performance Assessment and Analytics Dashboard" is a bonafide work carried out as PBL-3 End Term Assessment in partial fulfillment for the award of the degree of Bachelor of Technology in Computer Science and Engineering, by Your Name bearing registration number Your Registration Number, during the academic semester VI of year 2024-2025.'),
        paragraph("Place: Manipal University Jaipur, Jaipur", before=120),
        paragraph("Name of the Project Guide: Project Guide Name"),
        paragraph("Signature of the Project Guide: ______________________", before=120),
    ]

    parts += [
        paragraph(page_break=True),
        title("ACKNOWLEDGEMENT"),
        paragraph('This project would not have been completed without the help, support, comments, advice, cooperation and coordination of various people. I acknowledge and express my deepest sense of gratitude to my internal supervisor Project Guide Name for constant support, guidance, and continuous engagement during the development of this project titled "AI-Powered Student Performance Assessment and Analytics Dashboard."'),
        paragraph("I owe my profound gratitude to Dr. Neha Chaudhary, Head, Department of CSE, for valuable guidance and for facilitating me during my work. I am also very grateful to all the faculty members and staff for their precious support and cooperation during the development of this project."),
        paragraph("Finally, I extend my heartfelt appreciation to my classmates for their help and encouragement."),
    ]

    parts += [
        paragraph(page_break=True),
        title("ABSTRACT"),
        paragraph("The AI-Powered Student Performance Assessment and Analytics Dashboard is a web-based academic analytics system designed to monitor, analyze, and visualize student performance data. The project focuses on collecting and representing a broad student dataset including demographic details, academic scores, attendance, school and department information, behavior score, extracurricular participation, socioeconomic status, parental education, internet access, and career goals."),
        paragraph("The system is developed using Flask, Python, Pandas, Plotly, HTML, CSS, and JavaScript. It offers an interactive dashboard with filtering options that allow users to analyze student records by school, department, grade level, region, gender, socioeconomic category, and internet access. The project also includes AI-inspired insight generation for identifying high-performing students, at-risk learners, and academic intervention needs."),
        paragraph("The project integrates major technical components such as data visualization, introductory LLM-style insight generation, Docker-based containerization, Kubernetes deployment support, and Tableau-ready data export, making it a strong capstone-level application. The system helps educational stakeholders make informed decisions regarding student performance, intervention, and planning."),
    ]

    toc_rows = [
        ["Section", "Title"],
        ["1", "Introduction"],
        ["2", "Design Description"],
        ["3", "Project Description"],
        ["4", "Input/Output Form Design"],
        ["5", "Testing and Tools Used"],
        ["6", "Implementation and Maintenance"],
        ["7", "Conclusion and Future Work"],
        ["8", "Outcome"],
        ["9", "Bibliography"],
    ]
    parts += [
        paragraph(page_break=True),
        title("TABLE OF CONTENTS"),
        table(toc_rows, widths=[1400, 7600]),
    ]

    parts += [
        paragraph(page_break=True),
        heading("1. INTRODUCTION"),
        subheading("1.1 Objective of the Project"),
        paragraph("The main objective of this project is to build an intelligent and interactive student performance dashboard that can:"),
        bullet("store and process student-related academic and contextual data."),
        bullet("visualize performance trends using charts and analytics."),
        bullet("identify students requiring academic support."),
        bullet("generate insight-based recommendations."),
        bullet("help in educational monitoring and decision-making."),
        subheading("1.2 Brief Description of the Project"),
        paragraph("This project is a web-based dashboard application that manages and analyzes student performance assessment data. The system uses a dataset of 100 unique students and includes a wide variety of fields such as academic marks, attendance, behavior, extracurricular participation, demographic information, school information, and support-related indicators."),
        paragraph("The dashboard provides real-time filtering of student data, spotlight view of an individual student, cohort-level performance comparison, support-risk identification, and academic analytics through interactive visualizations."),
        subheading("1.3 Technology Used"),
        table(
            [
                ["Component", "Technology Used"],
                ["Frontend", "HTML, CSS, JavaScript"],
                ["Backend", "Python Flask"],
                ["Data Handling", "Pandas"],
                ["Visualization", "Plotly"],
                ["Testing", "Pytest"],
                ["Containerization", "Docker, Docker Compose"],
                ["Deployment", "Kubernetes manifests"],
                ["Analytics Integration", "Tableau-ready export"],
            ],
            widths=[2800, 6200],
        ),
        subheading("1.3.1 Hardware Requirement"),
        table(
            [
                ["Hardware", "Specification"],
                ["Processor", "Intel Core i3 or above"],
                ["RAM", "Minimum 4 GB, recommended 8 GB"],
                ["Storage", "Minimum 500 MB free space"],
                ["Display", "1366 x 768 resolution or above"],
            ],
            widths=[2800, 6200],
        ),
        subheading("1.3.2 Software Requirement"),
        table(
            [
                ["Software", "Requirement"],
                ["Operating System", "Windows / Linux / macOS"],
                ["Python", "3.11 or above"],
                ["Libraries", "Flask, Pandas, Plotly, Gunicorn, Pytest"],
                ["Tools", "Docker Desktop, Kubernetes, VS Code"],
                ["Browser", "Chrome / Edge / Firefox"],
            ],
            widths=[2800, 6200],
        ),
        subheading("1.4 Organization Profile"),
        paragraph("This project is developed as an academic application under the Department of Computer Science and Engineering, Manipal University Jaipur. The work is intended for educational analysis and demonstration of student performance monitoring using modern software engineering and analytics tools."),
    ]

    parts += [
        paragraph(page_break=True),
        heading("2. DESIGN DESCRIPTION"),
        subheading("2.1 Flow Chart"),
        bullet("Start"),
        bullet("Load Student Dataset"),
        bullet("Process and Clean Data"),
        bullet("Compute Academic Averages and Indicators"),
        bullet("Generate Insights and Risk Flags"),
        bullet("Render Dashboard"),
        bullet("Apply Filters"),
        bullet("Update Charts and Student Spotlight"),
        bullet("Display Results"),
        bullet("End"),
        subheading("2.2 Data Flow Diagrams"),
        paragraph("Level 0 DFD: User interacts with the Student Performance Dashboard System, which reads the student dataset and produces reports and visualizations."),
        paragraph("Level 1 DFD: User applies filters and inputs, the Data Processing Module reads the dataset, and the Insight Generation Module and Visualization Module produce recommendations and charts for the user."),
        subheading("2.3 Entity Relationship Diagram"),
        paragraph("The current system uses a CSV-based student entity containing StudentID, Student, Gender, Age, GradeLevel, School, Department, Region, SocioeconomicStatus, ParentalEducation, StudyHoursPerWeek, Attendance, Math, Science, English, ComputerScience, Economics, BehaviorScore, ExtracurricularScore, InternetAccess, CareerGoal, and Average."),
    ]

    field_rows = [
        ["Field Name", "Description"],
        ["StudentID", "Unique student identifier"],
        ["Student", "Name of student"],
        ["Gender", "Gender of student"],
        ["Age", "Age of student"],
        ["GradeLevel", "Class or grade level"],
        ["School", "School name"],
        ["Department", "Department or stream"],
        ["Region", "Urban or Rural"],
        ["SocioeconomicStatus", "Student socioeconomic category"],
        ["ParentalEducation", "Parent education level"],
