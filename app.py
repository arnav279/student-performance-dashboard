import os
from pathlib import Path

import pandas as pd
from flask import Flask, Response, jsonify, render_template

from dashboard.visualizations import (
    create_attendance_chart,
    create_performance_scatter,
    create_subject_chart,
)
from llm_assistant import generate_insights


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "students.csv"
SUBJECT_COLUMNS = ["Math", "Science", "English", "ComputerScience", "Economics"]


def load_student_data() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    df["Average"] = df[SUBJECT_COLUMNS].mean(axis=1).round(2)
    return df


def build_summary_metrics(df: pd.DataFrame) -> list[dict]:
    return [
        {
            "label": "Students",
            "value": int(len(df)),
            "description": "Records included in the capstone dataset.",
        },
        {
            "label": "Schools",
            "value": int(df["School"].nunique()),
            "description": "Institutions represented across the learning network.",
        },
        {
            "label": "Regions",
            "value": int(df["Region"].nunique()),
            "description": "Geographic zones covered in the student dataset.",
        },
        {
            "label": "Domains",
            "value": len(SUBJECT_COLUMNS),
            "description": "Academic subject areas used for student assessment.",
        },
        {
            "label": "Cohort Average",
            "value": f"{df['Average'].mean():.1f}",
            "description": "Combined performance across five assessment domains.",
        },
        {
            "label": "Attendance",
            "value": f"{df['Attendance'].mean():.1f}%",
            "description": "Average attendance rate across the cohort.",
        },
        {
            "label": "Needs Support",
            "value": int((df["Average"] < 70).sum()),
            "description": "Students flagged for additional academic intervention.",
        },
    ]


def build_dataset_profile(df: pd.DataFrame) -> list[dict]:
    return [
        {
            "title": "Academic Profile",
            "detail": "Math, Science, English, Computer Science, and Economics scores per learner.",
        },
        {
            "title": "Demographic Coverage",
            "detail": f"{df['Gender'].nunique()} genders, ages {int(df['Age'].min())}-{int(df['Age'].max())}, and {df['GradeLevel'].nunique()} grade levels.",
        },
        {
            "title": "Institutional Context",
            "detail": f"{df['School'].nunique()} schools, {df['Department'].nunique()} departments, and {df['Region'].nunique()} regions represented.",
        },
        {
            "title": "Learner Support Signals",
            "detail": "Attendance, study hours, behavior, extracurricular participation, internet access, and parental education.",
        },
    ]


def get_lab_features() -> list[dict]:
    return [
        {
            "lab": "Lab 1",
            "title": "Python data loading",
            "detail": "Reads CSV data with Pandas and prepares clean derived metrics.",
        },
        {
            "lab": "Lab 2",
            "title": "Data preprocessing",
            "detail": "Computes multi-subject averages and profile indicators across academic and contextual fields.",
        },
        {
            "lab": "Lab 3",
            "title": "Web application",
            "detail": "Serves the dashboard and APIs using Flask routes.",
        },
        {
            "lab": "Lab 4",
            "title": "Data visualization",
            "detail": "Renders interactive Plotly charts and exposes Tableau-ready analytics data.",
        },
        {
            "lab": "Lab 5",
            "title": "Intro to LLM",
            "detail": "Transforms dataset patterns into natural-language academic insights.",
        },
        {
            "lab": "Lab 6",
            "title": "Containerization and DevOps",
            "detail": "Packages the app with Docker, Compose, CI, and Kubernetes manifests.",
        },
    ]


def create_app() -> Flask:
    app = Flask(__name__)
    tableau_embed_url = os.environ.get("TABLEAU_EMBED_URL", "").strip()

    @app.route("/")
    def index():
        df = load_student_data()
        insights = generate_insights(df)
        subject_chart = create_subject_chart(df)
        attendance_chart = create_attendance_chart(df)
        performance_scatter = create_performance_scatter(df)

        return render_template(
            "index.html",
            students=df.to_dict(orient="records"),
            insights=insights,
            metrics=build_summary_metrics(df),
            dataset_profile=build_dataset_profile(df),
            lab_features=get_lab_features(),
            subject_columns=SUBJECT_COLUMNS,
            department_options=sorted(df["Department"].unique().tolist()),
            gender_options=sorted(df["Gender"].unique().tolist()),
            grade_options=sorted(df["GradeLevel"].astype(str).unique().tolist()),
            school_options=sorted(df["School"].unique().tolist()),
            region_options=sorted(df["Region"].unique().tolist()),
            socioeconomic_options=sorted(df["SocioeconomicStatus"].unique().tolist()),
            internet_options=sorted(df["InternetAccess"].unique().tolist()),
            tableau={
                "enabled": True,
                "data_endpoint": "/api/tableau/student-performance.csv",
                "embed_url": tableau_embed_url,
            },
            subject_chart=subject_chart,
            attendance_chart=attendance_chart,
            performance_scatter=performance_scatter,
        )

    @app.route("/api/insights")
    def api_insights():
        df = load_student_data()
        return jsonify(
            {
                "students": df.to_dict(orient="records"),
                "insights": generate_insights(df),
            }
        )

    @app.route("/api/summary")
    def api_summary():
        df = load_student_data()
        return jsonify(
            {
                "metrics": build_summary_metrics(df),
                "dataset_profile": build_dataset_profile(df),
                "lab_features": get_lab_features(),
                "subject_columns": SUBJECT_COLUMNS,
                "tableau": {
                    "enabled": True,
                    "data_endpoint": "/api/tableau/student-performance.csv",
                    "embed_url": tableau_embed_url,
                },
            }
        )

    @app.route("/api/tableau/student-performance.csv")
    def api_tableau_data():
        df = load_student_data().copy()
        df["SupportFlag"] = df["Average"].apply(lambda value: "Yes" if value < 70 else "No")
        df["AttendanceRisk"] = df["Attendance"].apply(
            lambda value: "Yes" if value < 80 else "No"
        )
        csv_payload = df.to_csv(index=False)
        return Response(
            csv_payload,
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=student-performance-tableau.csv"
            },
        )

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
