def analyze_job_description(
    job_title: str,
    company_name: str,
    status: str,
    job_description: str,
):
    description = job_description.lower()

    score = 40
    strengths = []
    missing_skills = []
    interview_topics = []
    suggested_next_actions = []

    skill_keywords = {
        "python": "Python",
        "fastapi": "FastAPI",
        "postgresql": "PostgreSQL",
        "sql": "SQL",
        "docker": "Docker",
        "rest api": "REST API",
        "api": "API development",
        "jwt": "JWT authentication",
        "authentication": "Authentication",
        "sqlalchemy": "SQLAlchemy",
        "testing": "Testing",
        "pytest": "Pytest",
        "deployment": "Deployment",
        "cloud": "Cloud deployment",
        "git": "Git/GitHub",
        "ci/cd": "CI/CD",
        "github actions": "GitHub Actions",
    }

    matched_skills = []

    for keyword, skill_name in skill_keywords.items():
        if keyword in description:
            matched_skills.append(skill_name)
            score += 5

    score = min(score, 95)

    if matched_skills:
        strengths.append(
            "This job matches your backend skills in "
            + ", ".join(matched_skills[:5])
            + "."
        )
    else:
        strengths.append("This job has general software engineering overlap.")

    expected_skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
        "Testing",
        "Cloud deployment",
        "CI/CD",
    ]

    for skill in expected_skills:
        if skill not in matched_skills:
            missing_skills.append(skill)

    interview_topics = matched_skills[:6]

    if not interview_topics:
        interview_topics = [
            "Backend API design",
            "Database basics",
            "Authentication",
            "Problem solving",
        ]

    suggested_next_actions.append("Prepare to explain your Job Tracker API project clearly.")
    suggested_next_actions.append("Review the main technologies mentioned in the job description.")
    suggested_next_actions.append(
        "Prepare examples about authentication, database design, testing, Docker, and deployment."
    )

    application_note = (
        f"{job_title} at {company_name} looks like a {score}/100 match. "
        f"Current application status: {status}. "
        f"The strongest overlap is around "
        f"{', '.join(matched_skills[:4]) if matched_skills else 'general backend development'}. "
        "Before applying or interviewing, focus on the missing skills and prepare project-based explanations."
    )

    return {
        "match_score": score,
        "strengths": strengths,
        "missing_skills": missing_skills,
        "interview_topics": interview_topics,
        "suggested_next_actions": suggested_next_actions,
        "application_note": application_note,
    }