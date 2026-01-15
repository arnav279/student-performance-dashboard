import plotly.express as px
from plotly.io import to_html

SUBJECT_COLUMNS = ["Math", "Science", "English", "ComputerScience", "Economics"]


def create_subject_chart(df):
    fig = px.bar(
