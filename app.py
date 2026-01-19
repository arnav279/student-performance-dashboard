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
