from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template

from dashboard.visualizations import create_attendance_chart, create_subject_chart
from llm_assistant import generate_insights


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "students.csv"


def load_student_data() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    subject_columns = ["Math", "Science", "English"]
    df["Average"] = df[subject_columns].mean(axis=1).round(2)
    return df


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        df = load_student_data()
        insights = generate_insights(df)
        subject_chart = create_subject_chart(df)
        attendance_chart = create_attendance_chart(df)

        return render_template(
            "index.html",
            students=df.to_dict(orient="records"),
            insights=insights,
            subject_chart=subject_chart,
            attendance_chart=attendance_chart,
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

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
