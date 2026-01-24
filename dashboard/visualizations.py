import plotly.express as px
from plotly.io import to_html

SUBJECT_COLUMNS = ["Math", "Science", "English", "ComputerScience", "Economics"]


def create_subject_chart(df):
    fig = px.bar(
        df,
        x="Student",
        y=SUBJECT_COLUMNS,
        barmode="group",
        title="Multi-Domain Subject Score Comparison",
        color_discrete_sequence=["#00d1ff", "#2df1b8", "#ffd166", "#ff6b6b", "#a78bfa"],
    )
    fig.update_layout(template="plotly_white", legend_title_text="Subject", xaxis_title="Student")
    return to_html(fig, full_html=False, include_plotlyjs=False)

