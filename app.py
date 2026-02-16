import streamlit as st
import pandas as pd
import plotly.express as px

st.title("AI-Powered Student Performance Analysis and Visualization System")

# Load dataset
df = pd.read_csv("data/student_data.csv")

# Show dataset
st.subheader("Student Dataset")
st.dataframe(df)

# Calculate average
df["Average"] = df[["Math", "Science", "English"]].mean(axis=1)

# Show averages
st.subheader("Average Scores")
st.dataframe(df[["Student", "Average"]])

# Visualization
st.subheader("Score Comparison")
fig = px.bar(df, x="Student", y=["Math", "Science", "English"],
             barmode="group")
st.plotly_chart(fig)

# AI Insight
st.subheader("AI Insights")

low_students = df[df["Average"] < 70]

if len(low_students) > 0:
    st.write("Students needing improvement:")
    st.dataframe(low_students[["Student", "Average"]])
else:
    st.write("All students performing well")

