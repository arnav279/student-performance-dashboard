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


def create_attendance_chart(df):
    fig = px.line(
        df,
        x="Student",
        y="Attendance",
        markers=True,
        title="Attendance Trend Across the Cohort",
    )
    fig.update_traces(line_color="#ff6b6b", marker_color="#00d1ff")
    fig.update_layout(template="plotly_white", yaxis_range=[0, 100])
    return to_html(fig, full_html=False, include_plotlyjs=False)


def create_performance_scatter(df):
    fig = px.scatter(
        df,
        x="Attendance",
        y="Average",
        text="Student",
        color="Average",
        size="ComputerScience",
        title="Attendance vs Average Score",
        color_continuous_scale=["#ff6b6b", "#ffd166", "#2df1b8"],
    )
    fig.update_traces(textposition="top center")
