import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Student Performance Dashboard")
st.subheader("Created by Arnav Juneja")

data = {
    "Student": ["A", "B", "C", "D"],
    "Math": [85, 78, 92, 60],
    "Science": [88, 74, 95, 65],
}

df = pd.DataFrame(data)

st.write("Student Data")
st.dataframe(df)

fig = px.bar(df, x="Student", y="Math", title="Math Scores")
st.plotly_chart(fig)
