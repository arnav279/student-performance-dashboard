# Student Performance Dashboard

Flask-based capstone project for student performance analysis, visualization, lightweight LLM-style insights, Docker packaging, and CI validation.

## Features

- Student score and attendance dashboard
- Automated insight generation for support planning
- Plotly visualizations for subject comparison and attendance
- JSON API endpoint for dashboard insights
- Docker and Docker Compose support
- GitHub Actions CI running the test suite

## Project Structure

```text
student-performance-dashboard
|-- app.py
|-- llm_assistant.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- README.md
|-- dataset/
|   `-- students.csv
|-- dashboard/
|   `-- visualizations.py
|-- templates/
|   `-- index.html
|-- tests/
|   `-- test_app.py
`-- .github/
    `-- workflows/
        `-- ci.yml
```

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

## Docker

```bash
docker build -t student-dashboard .
docker run -p 5000:5000 student-dashboard
```

Or:

```bash
docker compose up --build
```

## Testing

```bash
pytest
```
