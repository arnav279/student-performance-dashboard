import json
import os
from typing import Any
from urllib import error, request


SUBJECT_COLUMNS = ["Math", "Science", "English", "ComputerScience", "Economics"]


def _provider_name() -> str:
    return os.environ.get("LLM_PROVIDER", "openai-compatible").strip().lower()


def _provider_configured(provider: str) -> bool:
    model = os.environ.get("LLM_MODEL", "").strip()
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    if provider == "ollama":
        return bool(model)
    return bool(api_key and model)


def _base_metrics(df) -> dict[str, Any]:
    top_student = df.loc[df["Average"].idxmax()]
    support_students = df[df["Average"] < 70]
    attendance_risk = df[df["Attendance"] < 80]
    class_average = float(df["Average"].mean())
    attendance_average = float(df["Attendance"].mean())
    strongest_subject = df[SUBJECT_COLUMNS].mean().astype(float).idxmax()
    weakest_subject = df[SUBJECT_COLUMNS].mean().astype(float).idxmin()

    return {
        "top_student": top_student,
        "support_students": support_students,
        "attendance_risk": attendance_risk,
        "class_average": class_average,
        "attendance_average": attendance_average,
        "strongest_subject": strongest_subject,
        "weakest_subject": weakest_subject,
    }


def _default_llm_status() -> dict[str, Any]:
    provider = _provider_name()
    configured = _provider_configured(provider)
    return {
        "enabled": configured,
        "provider": provider,
        "model": os.environ.get("LLM_MODEL", ""),
        "mode": "live" if configured else "fallback",
    }


def _student_snapshot(row) -> dict[str, Any]:
    return {
        "student": row["Student"],
        "school": row["School"],
        "region": row["Region"],
        "department": row["Department"],
        "grade_level": int(row["GradeLevel"]),
        "attendance": float(row["Attendance"]),
        "average": float(row["Average"]),
        "best_subject": row[SUBJECT_COLUMNS].astype(float).idxmax(),
        "weakest_subject": row[SUBJECT_COLUMNS].astype(float).idxmin(),
        "study_hours": float(row["StudyHoursPerWeek"]),
        "behavior_score": float(row["BehaviorScore"]),
        "career_goal": row["CareerGoal"],
    }


def _build_prompt_context(df, student_name: str | None = None) -> str:
    metrics = _base_metrics(df)
    top_students = (
        df.nlargest(3, "Average")[["Student", "Average", "Attendance"]]
        .to_dict(orient="records")
    )
    support_students = [
        _student_snapshot(row)
        for _, row in metrics["support_students"].nsmallest(5, "Average").iterrows()
    ]
    attendance_risk = [
        _student_snapshot(row)
        for _, row in metrics["attendance_risk"].nsmallest(5, "Attendance").iterrows()
    ]

    context = {
        "cohort_size": int(len(df)),
        "schools": sorted(df["School"].unique().tolist()),
        "regions": sorted(df["Region"].unique().tolist()),
        "class_average": round(metrics["class_average"], 2),
        "attendance_average": round(metrics["attendance_average"], 2),
        "strongest_subject": metrics["strongest_subject"],
        "weakest_subject": metrics["weakest_subject"],
        "top_students": top_students,
        "support_students": support_students,
        "attendance_risk": attendance_risk,
    }

    if student_name:
        row = df[df["Student"] == student_name]
        if not row.empty:
            context["selected_student"] = _student_snapshot(row.iloc[0])

    return json.dumps(context, indent=2)


def _fallback_summary(df) -> str:
    metrics = _base_metrics(df)
    top_student = metrics["top_student"]
    support_count = int(len(metrics["support_students"]))
    attendance_risk_count = int(len(metrics["attendance_risk"]))

    return (
        f"The cohort average is {metrics['class_average']:.1f}, with attendance averaging "
        f"{metrics['attendance_average']:.1f}%. {top_student['Student']} is the strongest "
        f"overall learner at {top_student['Average']:.1f}. {metrics['strongest_subject']} is "
        f"the strongest subject across the cohort, while {metrics['weakest_subject']} needs the "
        f"most reinforcement. {support_count} students need academic support and "
        f"{attendance_risk_count} require attendance follow-up."
    )


def _fallback_answer(df, question: str, student_name: str | None = None) -> str:
    metrics = _base_metrics(df)
    lowered = question.lower()

    if student_name:
        row = df[df["Student"] == student_name]
        if not row.empty:
            student = row.iloc[0]
            best = student[SUBJECT_COLUMNS].astype(float).idxmax()
            weakest = student[SUBJECT_COLUMNS].astype(float).idxmin()
            return (
                f"{student['Student']} has an average of {student['Average']:.1f} and attendance "
                f"of {student['Attendance']:.0f}%. Their strongest subject is {best} and the main "
                f"support area is {weakest}. A sensible next step is targeted practice in {weakest} "
                f"plus weekly progress review aligned with the {student['Department']} department."
            )

    if "top" in lowered or "best" in lowered:
        top_student = metrics["top_student"]
        return (
            f"The top student is {top_student['Student']} with an average score of "
            f"{top_student['Average']:.1f} and attendance of {top_student['Attendance']:.0f}%."
        )

    if "attendance" in lowered:
        return (
            f"Average attendance is {metrics['attendance_average']:.1f}%. "
            f"{len(metrics['attendance_risk'])} students are below the 80% attendance threshold."
        )

    if "subject" in lowered:
        return (
            f"{metrics['strongest_subject']} is the strongest subject across the cohort, while "
            f"{metrics['weakest_subject']} is the weakest and should be prioritized for support."
        )

    return (
        f"The cohort is performing at an average of {metrics['class_average']:.1f} with "
        f"{metrics['attendance_average']:.1f}% attendance. The main academic focus should be "
        f"{metrics['weakest_subject']}, especially for students currently below the 70 average mark."
    )


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    provider = _provider_name()
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    model = os.environ.get("LLM_MODEL", "").strip()
    default_base_url = (
        "http://localhost:11434" if provider == "ollama" else "https://api.openai.com/v1"
    )
    base_url = os.environ.get("LLM_API_BASE_URL", default_base_url).rstrip("/")

    if provider == "ollama":
        if not model:
            raise RuntimeError("LLM_MODEL must be set for Ollama responses.")

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.3},
        }

        req = request.Request(
            f"{base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
    else:
        if not api_key or not model:
            raise RuntimeError(
                "LLM_API_KEY and LLM_MODEL must be set for live LLM responses."
            )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }

        req = request.Request(
            f"{base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

    try:
        with request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"LLM request failed with HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"LLM request failed: {exc.reason}") from exc

    if provider == "ollama":
        return result["message"]["content"].strip()

    return result["choices"][0]["message"]["content"].strip()


def generate_insights(df) -> dict[str, Any]:
    metrics = _base_metrics(df)
    top_student = metrics["top_student"]

    overview = (
        f"The class average is {metrics['class_average']:.1f} with overall attendance at "
        f"{metrics['attendance_average']:.1f}% across {df['School'].nunique()} schools and "
        f"{df['Region'].nunique()} regions. {top_student['Student']} is leading with "
        f"an average of {top_student['Average']:.1f}."
    )

    recommendations = []
    for _, row in metrics["support_students"].iterrows():
        weakest_subject_for_student = row[SUBJECT_COLUMNS].astype(float).idxmin()
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
    for _, row in metrics["attendance_risk"].iterrows():
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
                "average": metrics["class_average"],
                "action": "Maintain momentum with advanced practice and peer mentoring.",
            }
        )

    if not attendance_alerts:
        attendance_alerts.append(
            {
                "student": "Classwide",
                "attendance": int(metrics["attendance_average"]),
                "action": "Attendance is stable across the cohort.",
            }
        )

    llm_status = _default_llm_status()
    llm_summary = _fallback_summary(df)

    if llm_status["enabled"]:
        try:
            llm_summary = _call_llm(
                system_prompt=(
                    "You are an academic analytics assistant. Summarize student cohort data in 3 "
                    "short sentences for a dashboard. Be concrete, action-oriented, and do not "
                    "invent data beyond the provided context."
                ),
                user_prompt=f"Summarize this cohort:\n{_build_prompt_context(df)}",
            )
        except RuntimeError as exc:
            llm_status["mode"] = "fallback"
            llm_status["error"] = str(exc)

    return {
        "overview": overview,
        "top_student": {
            "student": top_student["Student"],
            "average": float(top_student["Average"]),
        },
        "class_snapshot": {
            "class_average": metrics["class_average"],
            "attendance_average": metrics["attendance_average"],
            "strongest_subject": metrics["strongest_subject"],
            "weakest_subject": metrics["weakest_subject"],
        },
        "llm_summary": llm_summary,
        "llm_workflow": [
            "Load student performance and attendance data.",
            "Build a compact cohort context with performance and support signals.",
            "Send the context to either an OpenAI-compatible API or a local Ollama model when configured.",
            "Fall back to deterministic summaries if no live LLM configuration is available.",
        ],
        "llm_status": llm_status,
        "recommendations": recommendations,
        "attendance_alerts": attendance_alerts,
    }


def answer_question(df, question: str, student_name: str | None = None) -> dict[str, Any]:
    clean_question = question.strip()
    if not clean_question:
        raise ValueError("Question cannot be empty.")

    llm_status = _default_llm_status()
    answer = _fallback_answer(df, clean_question, student_name=student_name)

    if llm_status["enabled"]:
        try:
            answer = _call_llm(
                system_prompt=(
                    "You are an academic analytics assistant for a student performance dashboard. "
                    "Answer using only the provided dataset context. Keep the answer under 120 words "
                    "and include at least one concrete numeric detail."
                ),
                user_prompt=(
                    f"Question: {clean_question}\n"
                    f"Selected student: {student_name or 'None'}\n"
                    f"Context:\n{_build_prompt_context(df, student_name=student_name)}"
                ),
            )
        except RuntimeError as exc:
            llm_status["mode"] = "fallback"
            llm_status["error"] = str(exc)

    return {
        "answer": answer,
        "question": clean_question,
        "student": student_name,
        "llm_status": llm_status,
    }
