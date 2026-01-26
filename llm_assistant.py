SUBJECT_COLUMNS = ["Math", "Science", "English", "ComputerScience", "Economics"]


def generate_insights(df):
    top_student = df.loc[df["Average"].idxmax()]
    support_students = df[df["Average"] < 70]
    attendance_risk = df[df["Attendance"] < 80]
    class_average = float(df["Average"].mean())
    attendance_average = float(df["Attendance"].mean())
    strongest_subject = (
        df[SUBJECT_COLUMNS].mean().astype(float).idxmax()
    )
    weakest_subject = (
        df[SUBJECT_COLUMNS].mean().astype(float).idxmin()
    )

    overview = (
        f"The class average is {class_average:.1f} with overall attendance at "
        f"{attendance_average:.1f}% across {df['School'].nunique()} schools and "
        f"{df['Region'].nunique()} regions. {top_student['Student']} is leading with "
        f"an average of {top_student['Average']:.1f}."
    )

    recommendations = []
    for _, row in support_students.iterrows():
        weakest_subject_for_student = (
            row[SUBJECT_COLUMNS].astype(float).idxmin()
        )
        recommendations.append(
            {
                "student": row["Student"],
                "average": float(row["Average"]),
                "action": (
                    f"Focus on {weakest_subject_for_student} remediation, reinforce "
                    f"{row['Department']} learning goals, and schedule weekly mentoring."
                ),
            }
        )

    attendance_alerts = []
    for _, row in attendance_risk.iterrows():
        attendance_alerts.append(
            {
                "student": row["Student"],
                "attendance": int(row["Attendance"]),
                "action": (
                    f"Schedule a guardian follow-up and attendance review for the "
                    f"{row['Region']} region cohort."
                ),
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "student": "Classwide",
                "average": class_average,
                "action": "Maintain momentum with advanced practice and peer mentoring.",
            }
        )

    if not attendance_alerts:
        attendance_alerts.append(
            {
                "student": "Classwide",
                "attendance": int(attendance_average),
                "action": "Attendance is stable across the cohort.",
            }
        )
