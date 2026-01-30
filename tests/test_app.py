from app import create_app, load_student_data


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


def test_insights_api_returns_json():
    app = create_app()
    client = app.test_client()
