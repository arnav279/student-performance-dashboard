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
        ["StudyHoursPerWeek", "Weekly study hours"],
        ["Attendance", "Attendance percentage"],
        ["Math / Science / English / ComputerScience / Economics", "Assessment scores"],
        ["BehaviorScore", "Behavioral performance score"],
        ["ExtracurricularScore", "Participation/activity score"],
        ["InternetAccess", "Internet access status"],
        ["CareerGoal", "Student career aspiration"],
        ["Average", "Calculated overall academic average"],
    ]

    parts += [
        paragraph(page_break=True),
        heading("3. PROJECT DESCRIPTION"),
        subheading("3.1 Database"),
        paragraph("This project currently uses a CSV file-based dataset instead of a traditional relational database. The main dataset file is dataset/students.csv. Data is loaded using Pandas and processed dynamically inside the Flask application."),
        subheading("3.2 Table Description"),
        table(field_rows, widths=[3600, 5400]),
        subheading("3.3 File/Database Design"),
        bullet("app.py - Main Flask application"),
        bullet("llm_assistant.py - AI-style insight generation logic"),
        bullet("dashboard/visualizations.py - Plotly chart generation functions"),
        bullet("templates/index.html - Dashboard frontend template"),
        bullet("dataset/students.csv - Main student dataset"),
        bullet("tests/test_app.py - Unit tests"),
        bullet("Dockerfile - Containerization setup"),
        bullet("docker-compose.yml - Docker compose configuration"),
        bullet("kubernetes/ - Deployment manifests"),
    ]

    parts += [
        paragraph(page_break=True),
        heading("4. INPUT/OUTPUT FORM DESIGN"),
        paragraph("Input controls include student search, school filter, department filter, grade filter, region filter, gender filter, socioeconomic filter, internet access filter, attendance threshold slider, support-risk toggle, and sorting dropdown."),
        paragraph("Output is displayed in the form of KPI metric cards, student spotlight panel, advisor brief and intervention recommendations, cohort explorer student list, intervention matrix chart, subject balance chart, server-rendered Plotly visualizations, and cohort directory table."),
    ]

    parts += [
        paragraph(page_break=True),
        heading("5. TESTING AND TOOLS USED"),
        paragraph("Testing covers the following application checks:"),
        bullet("successful loading of dataset"),
        bullet("generation of average column"),
        bullet("uniqueness of student names"),
        bullet("correct Urban/Rural region setup"),
        bullet("rendering of dashboard home page"),
        bullet("API response validation"),
        bullet("Tableau export route validation"),
        paragraph("Tools used in the project include:"),
        bullet("Python"),
        bullet("Flask"),
        bullet("Pandas"),
        bullet("Plotly"),
        bullet("Pytest"),
        bullet("Docker and Docker Compose"),
        bullet("Kubernetes"),
        bullet("VS Code"),
        bullet("Git/GitHub"),
    ]

    parts += [
        paragraph(page_break=True),
        heading("6. IMPLEMENTATION AND MAINTENANCE"),
        paragraph("The implementation of the project follows a modular structure. Backend logic is handled using Flask routes, data processing is done through Pandas, charts are built using Plotly, and the frontend is created using HTML, CSS, and JavaScript. Dynamic filtering is implemented on the client side for interactivity."),
        paragraph("For maintenance, the dataset can be updated by replacing the CSV file, the system supports containerized deployment using Docker, Kubernetes manifests allow future scalable deployment, and test files help ensure correctness after code updates."),
    ]

    parts += [
        paragraph(page_break=True),
        heading("7. CONCLUSION AND FUTURE WORK"),
        paragraph("The project successfully demonstrates a complete student performance analytics system that combines data management, visualization, filtering, and intelligent insight generation. It provides a rich and interactive dashboard for understanding academic trends, attendance behavior, learner support needs, and student segmentation."),
        paragraph("Future enhancements may include:"),
        bullet("integration with a relational database such as MySQL or PostgreSQL"),
        bullet("login and role-based access control"),
        bullet("downloadable PDF report generation"),
        bullet("historical trend analysis across semesters"),
        bullet("real LLM/API integration for advanced recommendations"),
        bullet("teacher/admin dashboards"),
        bullet("predictive analytics using machine learning"),
        bullet("live deployment on cloud platforms"),
    ]

    parts += [
        paragraph(page_break=True),
        heading("8. OUTCOME"),
        paragraph("The project has reached a functional stage with a fully working dashboard, expanded dataset, multi-factor filtering, interactive charts, and deployment-ready configuration."),
        paragraph("The work demonstrates progress toward a capstone-level educational analytics system with strong visualization and insight-generation capabilities."),
        paragraph("Further outcomes may include deployment, publication as a technical paper, or extension into a full-scale academic monitoring platform."),
    ]

    parts += [
        paragraph(page_break=True),
        heading("9. BIBLIOGRAPHY"),
        bullet("[1] Grus, J. (2019). Data Science from Scratch. O'Reilly Media, Sebastopol, Calif."),
        bullet("[2] McKinney, W. (2022). Python for Data Analysis. O'Reilly Media, Sebastopol, Calif."),
        bullet("[3] Ramalho, L. (2022). Fluent Python. O'Reilly Media, Sebastopol, Calif."),
        bullet("[4] Plotly Technologies Inc. (2024). Plotly Python Graphing Library. https://plotly.com/python/"),
        bullet("[5] Flask Documentation. (2024). Flask Web Development Framework. https://flask.palletsprojects.com/"),
        bullet("[6] Pandas Documentation. (2024). Pandas User Guide. https://pandas.pydata.org/"),
        bullet("[7] Docker Documentation. (2024). Docker Overview. https://docs.docker.com/"),
        bullet("[8] Kubernetes Documentation. (2024). Kubernetes Concepts. https://kubernetes.io/docs/home/"),
    ]

    body = "".join(parts)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="708" w:footer="708" w:gutter="0"/>'
        '</w:sectPr></w:body></w:document>'
    )


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>
"""


CORE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Minor Project Progress Report Styled</dc:title>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
</cp:coreProperties>
"""


WORD_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""


def main():
    with ZipFile(OUTPUT_PATH, "w", ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", CONTENT_TYPES)
        docx.writestr("_rels/.rels", RELS)
        docx.writestr("docProps/app.xml", APP_XML)
        docx.writestr("docProps/core.xml", CORE_XML)
        docx.writestr("word/document.xml", build_document())
        docx.writestr("word/_rels/document.xml.rels", WORD_RELS)
    print(OUTPUT_PATH.resolve())


if __name__ == "__main__":
    main()
