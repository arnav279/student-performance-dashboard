from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app, load_student_data
from llm_assistant import _default_llm_status


def test_load_student_data_creates_average_column():
    df = load_student_data()

    assert "Average" in df.columns
    assert len(df) >= 100
    assert "Department" in df.columns
    assert "Region" in df.columns
    assert "ComputerScience" in df.columns
    assert df["Student"].is_unique
    assert set(df["Region"].unique()) == {"Urban", "Rural"}


def test_home_page_renders_dashboard():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"AI-Powered Student Performance Analysis and Visualization System" in response.data
    assert b"Top performer" in response.data
    assert b"Academic Profile" in response.data
    assert b"Geography and Demographics" in response.data
    assert b"Cohort Directory" in response.data
    assert b"Ask AI Assistant" in response.data


def test_insights_api_returns_json():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/insights")
    payload = response.get_json()

    assert response.status_code == 200
    assert "students" in payload
    assert "insights" in payload
    assert payload["insights"]["top_student"]["student"]
    assert payload["insights"]["llm_status"]["mode"] in {"live", "fallback"}
    assert payload["students"][0]["Department"]


def test_summary_api_exposes_lab_features_and_metrics():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/summary")
    payload = response.get_json()

    assert response.status_code == 200
    assert len(payload["metrics"]) == 7
    assert len(payload["dataset_profile"]) == 4
    assert len(payload["lab_features"]) == 6
    assert payload["lab_features"][4]["title"] == "Intro to LLM"
    assert len(payload["subject_columns"]) == 5
    assert payload["tableau"]["data_endpoint"] == "/api/tableau/student-performance.csv"


def test_tableau_export_returns_csv():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/tableau/student-performance.csv")

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"SupportFlag" in response.data
    assert b"AttendanceRisk" in response.data


def test_assistant_api_returns_answer():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/api/assistant",
        json={"question": "Who is the top student?", "student": None},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert "answer" in payload
    assert payload["llm_status"]["mode"] in {"live", "fallback"}


def test_assistant_api_validates_question():
    app = create_app()
    client = app.test_client()

    response = client.post("/api/assistant", json={"question": "   "})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Question is required."


def test_ollama_mode_is_considered_live_without_api_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_MODEL", "llama3.2")
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    status = _default_llm_status()

    assert status["enabled"] is True
    assert status["mode"] == "live"
    assert status["provider"] == "ollama"
