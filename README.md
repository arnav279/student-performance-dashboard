# Student Performance Dashboard

## Live Website

The project is deployed online and can be accessed here:

[https://student-performance-dashboard-ett-lab.onrender.com/](https://student-performance-dashboard-ett-lab.onrender.com/)

## 1. Project Title

**AI-Powered Student Performance Assessment and Analytics Dashboard**

## 2. Project Overview

The Student Performance Dashboard is a feature-rich academic analytics system developed to study, visualize, and interpret student performance data in a meaningful way. The project is designed as an interactive dashboard rather than a static marks display. Its purpose is to help users explore student performance from multiple perspectives, such as academics, attendance, demographics, institutional context, and learner support indicators.

This project focuses on turning student records into understandable insights. Instead of limiting the analysis to subject-wise marks only, the dashboard represents a broader student profile that includes grade level, school, department, region, socioeconomic status, internet access, behavior, extracurricular participation, and career goals. This makes the system more realistic and more aligned with modern educational analytics use cases.

The dashboard provides a complete view of student assessment through interactive filtering, comparison charts, spotlight-based review, support-risk identification, and recommendation-oriented summaries. It is intended to demonstrate how data visualization and analytical thinking can be applied to educational data in a practical and presentation-ready form.

## 3. Purpose of the Project

The project is built to solve a simple but important problem: student data is often available, but it is not always easy to interpret quickly or use for decision-making. A spreadsheet or raw dataset may contain useful values, but it does not immediately communicate which students are doing well, which learners may need support, what patterns exist across schools or regions, or how performance differs across subject areas.

This dashboard addresses that gap by offering:

- a centralized and interactive performance analysis view
- a visual method for comparing academic outcomes
- student-level and cohort-level performance understanding
- support identification for low-performing or low-attendance learners
- a richer educational context for data-driven review

## 4. Problem Statement

Educational institutions and academic stakeholders often need a system that can do more than simply store marks. They need a platform that can:

- analyze academic performance across multiple dimensions
- identify students who may require intervention
- compare groups of learners based on contextual factors
- visualize patterns in student progress and attendance
- support academic planning using interpretable insights

Traditional tabular data alone is not sufficient for this purpose. Therefore, this project presents a dashboard-based student assessment system that combines data representation, filtering, analytics, and visualization in one interface.

## 5. Objectives

The major objectives of the project are:

- to create an interactive dashboard for student performance assessment
- to represent student data across academic, demographic, and behavioral dimensions
- to visualize student trends using modern chart-based techniques
- to identify support-risk learners using academic and attendance criteria
- to generate readable insight summaries for intervention planning
- to provide a strong capstone-style demonstration project for academic evaluation

## 6. Scope of the Project

The scope of the project includes:

- analysis of academic scores across five major subjects
- attendance-based performance monitoring
- student segmentation using multiple filters
- individual student spotlight review
- support recommendations and risk awareness
- cohort comparison and summary visualization
- export-ready data representation for external reporting tools

The project is suitable for:

- educational analytics demonstrations
- minor project and capstone presentations
- dashboard design showcases
- academic data visualization use cases
- early-stage student monitoring systems

## 7. Key Features

### 7.1 Interactive Cohort Explorer

The cohort explorer is one of the main components of the dashboard. It allows users to filter and narrow down the student population dynamically. This helps in studying specific learner groups rather than only the full dataset.

The explorer currently supports filtering by:

- student name
- school
- department
- grade level
- region
- gender
- socioeconomic status
- internet access
- attendance threshold
- support-risk category
- sorting preference

This feature makes the dashboard highly interactive and useful for detailed student segmentation.

### 7.1.1 LLM Assistant Integration

The dashboard now includes a real LLM integration layer instead of only static insight text. The assistant can answer questions about the selected student or the full cohort from the dashboard itself.

The integration supports:

- OpenAI-compatible chat completion APIs
- local Ollama models
- configurable model, API key, and base URL through environment variables
- graceful fallback summaries and answers when no live LLM is configured
- a dedicated `/api/assistant` endpoint for frontend or external use

### 7.2 Student Spotlight Panel

The student spotlight panel provides a focused view of an individual learner. When a student is selected, the dashboard updates to show:

- average score
- attendance status
- strongest subject
- weakest subject
- student narrative summary
- intervention recommendation
- attendance outlook
- support priority level

This feature helps transform raw student values into a meaningful learner profile.

### 7.3 Multi-Subject Academic Analysis

The dashboard analyzes student performance across the following five assessment domains:

- Mathematics
- Science
- English
- Computer Science
- Economics

Using multiple subject areas makes the project more realistic and more useful than a three-subject classroom demo. It also supports better subject comparison and broader academic evaluation.

### 7.4 Rich Student Data Representation

The project goes beyond marks and attendance to represent broader student context. Each student record includes fields such as:

- Student ID
- student name
- gender
- age
- grade level
- school
- department
- region
- socioeconomic status
- parental education
- study hours per week
- attendance
- behavior score
- extracurricular score
- internet access
- career goal
- subject scores
- overall average

This richer dataset helps make the project look and function like a more mature educational analytics system.

### 7.5 Performance and Risk Visualization

The dashboard includes visualizations that support both overview and detailed analysis. These charts help users understand:

- how subject scores compare across learners
- how attendance relates to academic performance
- how a filtered cohort performs across subjects
- which students fall into possible intervention zones

These visual components make the dashboard suitable for both presentation and analysis.

### 7.6 Academic Support Recommendations

The system includes recommendation-style insight generation that identifies:

- students with low academic averages
- students with low attendance
- subject areas where intervention is needed
- learners who should be prioritized for support

This gives the project an intelligence-oriented dimension and improves its usefulness as a decision-support tool.

## 8. Dataset Description

The project uses a dataset of **100 unique students**. The dataset has been expanded specifically to make the project stronger in scope, realism, and analytical value.

### 8.1 Dataset Characteristics

- 100 student records
- all student names are unique
- Urban and Rural regional categories
- multiple schools represented
- multiple departments represented
- multiple grade levels represented
- multiple socioeconomic categories represented
- multiple learner-support indicators represented

### 8.2 Main Data Groups

The dataset can be broadly divided into the following groups:

#### Academic Fields

- Math
- Science
- English
- ComputerScience
- Economics
- Average

#### Student Identity and Demographics

- StudentID
- Student
- Gender
- Age
- GradeLevel

#### Institutional Context

- School
- Department
- Region

#### Support and Contextual Indicators

- SocioeconomicStatus
- ParentalEducation
- StudyHoursPerWeek
- Attendance
- BehaviorScore
- ExtracurricularScore
- InternetAccess
- CareerGoal

This broad data representation helps the project support meaningful filtering and interpretation instead of only displaying basic marks.

## 9. Functional Modules

### 9.1 Dashboard Landing View

The dashboard opens with a project overview area that introduces the system and provides immediate context around the current cohort. It presents important summary information in a visually engaging way and gives users access to the main exploration areas.

### 9.2 Metrics Section

The dashboard provides key metric cards to summarize the dataset and the current analytical view. These metrics help users quickly understand the scale and quality of the student cohort.

Examples of information represented include:

- number of students
- number of schools
- number of regions
- number of academic domains
- cohort average
- attendance average
- number of students requiring support

### 9.3 Filtering and Segmentation

The filtering panel is designed to help users narrow the data based on educational context, learner characteristics, and support signals. This module allows the dashboard to act like a mini analytics studio rather than a static page.

### 9.4 Student Spotlight and Intervention View

This module updates dynamically based on selected students and shows deeper insight into their academic condition. It helps demonstrate how the system can support individual student assessment.

### 9.5 Visualization Studio

This section contains chart-based representations of cohort performance. It helps users identify patterns and compare filtered student groups more effectively than by reading raw table data.

### 9.6 Cohort Directory

The directory view provides a structured table of the active filtered cohort. It acts as a bridge between visual analysis and record-level review.

## 10. Dashboard Design and User Experience

The dashboard has been designed to look polished, modern, and presentation-ready. It uses a high-contrast colorful theme so that important sections remain visually separated and easy to understand.

The visual design emphasizes:

- strong section separation
- readable contrast
- colorful accents for chart and panel differentiation
- clean spacing and information hierarchy
- professional presentation suitable for academic demonstration

The filter menu is designed separately to improve clarity and usability. The project aims to look like a thoughtfully developed analytics product rather than a basic student marks page.

## 11. Visual Analytics in the Project

The project includes multiple chart-based analytics components to make performance interpretation easier.

These include:

- subject comparison visualization
- attendance-related performance analysis
- performance versus attendance relationship view
- filtered cohort subject balance view
- individual student subject signature

These chart-driven views help reveal patterns that would be difficult to detect from tables alone.

## 12. Insight and Decision Support Value

One of the strengths of the project is that it does not stop at data display. It attempts to explain what the data suggests.

The system supports educational review by helping users answer questions such as:

- which students are performing strongly overall
- which students may need intervention
- which subject area is weakest for a student
- how attendance affects performance
- which cohort segment should be studied more closely
- what contextual factors may be relevant in understanding student outcomes

This makes the project suitable for academic analytics, reporting, and educational planning demonstrations.

## 13. API and Structured Output Features

The project also provides structured output for analytics and reporting support.

Available outputs include:

- insight-oriented API responses
- summary-oriented API responses
- LLM assistant question-answer responses
- Tableau-ready CSV export

## 14. LLM Configuration

### 14.1 OpenAI-Compatible Providers

To enable live cloud LLM responses, set these environment variables before running the app:

- `LLM_API_KEY` for your provider API key
- `LLM_MODEL` for the chat model name
- `LLM_API_BASE_URL` optionally, if you are using a non-default OpenAI-compatible endpoint

### 14.2 Local Ollama

To run the dashboard against a local Ollama model, first install Ollama, pull a model, and then set:

- `LLM_PROVIDER=ollama`
- `LLM_MODEL=llama3.2` or another local model name you have pulled
- `LLM_API_BASE_URL=http://localhost:11434` optionally, if your Ollama server is not using the default local address

For Ollama, no API key is required. The app uses Ollama's native `/api/chat` endpoint.

Example PowerShell setup:

```powershell
$env:LLM_PROVIDER="ollama"
$env:LLM_MODEL="llama3.2"
ollama serve
ollama pull llama3.2
python app.py
```

If no live provider is configured, the dashboard still works and automatically uses its built-in fallback response engine.

This improves the scope of the project and makes it useful beyond the frontend dashboard alone.

## 15. CI/CD Setup

The repository now includes a GitHub Actions pipeline in `.github/workflows/ci.yml` with two stages:

- CI: installs dependencies and runs `pytest -q` on pushes and pull requests
- CD: triggers a Render deployment automatically after CI passes on the `main` branch

To enable automatic deployment from GitHub to Render:

1. Open your Render web service dashboard.
2. Copy the service deploy hook URL.
3. In GitHub, go to `Settings > Secrets and variables > Actions`.
4. Add a repository secret named `RENDER_DEPLOY_HOOK_URL`.

If the secret is not set, the workflow still completes CI successfully and skips deployment instead of failing.

## 16. Why This Project Is Strong as a Minor/Capstone Project

This project is strong for academic submission because it combines multiple meaningful components:

- data representation
- visual analytics
- filtering and interactivity
- broader dataset design
- student support interpretation
- presentation-quality dashboard design
- reportable educational outcomes

It shows both technical effort and analytical thinking. It also demonstrates how software can be used to convert raw educational data into an understandable and useful decision-support system.

## 17. Expected Use Cases

The dashboard can be useful in scenarios such as:

- reviewing class-wide student performance
- identifying academic risk groups
- comparing Urban and Rural student groups
- analyzing departmental performance
- understanding attendance-related academic issues
- preparing student analytics presentations
- demonstrating educational dashboard concepts in academic evaluation

## 18. Outcome of the Project

The project delivers a complete interactive student analytics dashboard that combines:

- broad student-data coverage
- performance assessment
- filtering and segmentation
- visual comparison
- student-level review
- support insight generation

It successfully presents student performance as a multi-dimensional educational analytics problem rather than a simple marks sheet.

## 19. Future Enhancement Possibilities

The project can be extended further in many directions, including:

- database integration using MySQL or PostgreSQL
- user login and role-based access control
- teacher and administrator panels
- downloadable report generation
- semester-wise historical tracking
- machine learning based prediction
- advanced recommendation generation
- cloud deployment for live access
- direct institutional integration

These future directions show that the project has good scope for development beyond the current version.

## 20. Final Summary

The Student Performance Dashboard is a comprehensive and presentation-oriented educational analytics project that explains student performance through data, interactivity, and visualization. It demonstrates strong project depth through a rich dataset, polished dashboard design, multi-factor filtering, learner-level analysis, and readable support insights.

Overall, the project is not only useful as a technical implementation, but also as a strong academic project report subject because it clearly shows purpose, scope, data richness, analysis quality, and future potential.
