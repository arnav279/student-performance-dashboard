from app import create_app, load_student_data


def test_load_student_data_creates_average_column():
    df = load_student_data()

    assert "Average" in df.columns
    assert len(df) >= 5


def test_home_page_renders_dashboard():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"AI-Powered Student Performance Analysis and Visualization System" in response.data
    assert b"Top Performer" in response.data


def test_insights_api_returns_json():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/insights")
    payload = response.get_json()

    assert response.status_code == 200
    assert "students" in payload
    assert "insights" in payload
    assert payload["insights"]["top_student"]["student"] == "C"
