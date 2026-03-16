import plotly.express as px
from plotly.io import to_html


def create_subject_chart(df):
    fig = px.bar(
        df,
        x="Student",
        y=["Math", "Science", "English"],
        barmode="group",
        title="Subject Score Comparison",
        color_discrete_sequence=["#114b5f", "#1a936f", "#f4d35e"],
    )
    fig.update_layout(template="plotly_white", legend_title_text="Subject")
    return to_html(fig, full_html=False, include_plotlyjs=False)


def create_attendance_chart(df):
    fig = px.line(
        df,
        x="Student",
        y="Attendance",
        markers=True,
        title="Attendance Trend",
    )
    fig.update_traces(line_color="#c44536", marker_color="#772e25")
    fig.update_layout(template="plotly_white", yaxis_range=[0, 100])
    return to_html(fig, full_html=False, include_plotlyjs=False)
