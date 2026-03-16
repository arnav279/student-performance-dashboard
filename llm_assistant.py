def generate_insights(df):
    top_student = df.loc[df["Average"].idxmax()]
    support_students = df[df["Average"] < 70]
    attendance_risk = df[df["Attendance"] < 80]

    overview = (
        f"The class average is {df['Average'].mean():.1f}. "
        f"{top_student['Student']} is leading with an average of {top_student['Average']:.1f}."
    )

    recommendations = []
    for _, row in support_students.iterrows():
        weakest_subject = (
            row[["Math", "Science", "English"]].astype(float).idxmin()
        )
        recommendations.append(
            {
                "student": row["Student"],
                "average": float(row["Average"]),
                "action": f"Focus on {weakest_subject} remediation and weekly mentoring.",
            }
        )

    attendance_alerts = []
    for _, row in attendance_risk.iterrows():
        attendance_alerts.append(
            {
                "student": row["Student"],
                "attendance": int(row["Attendance"]),
                "action": "Schedule a guardian follow-up and attendance review.",
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "student": "Classwide",
                "average": float(df["Average"].mean()),
                "action": "Maintain momentum with advanced practice and peer mentoring.",
            }
        )

    if not attendance_alerts:
        attendance_alerts.append(
            {
                "student": "Classwide",
                "attendance": int(df["Attendance"].mean()),
                "action": "Attendance is stable across the cohort.",
            }
        )

    return {
        "overview": overview,
        "top_student": {
            "student": top_student["Student"],
            "average": float(top_student["Average"]),
        },
        "recommendations": recommendations,
        "attendance_alerts": attendance_alerts,
    }
