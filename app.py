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
