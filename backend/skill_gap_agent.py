def skill_gap_analyzer(recommended_career, current_skills):
    """
    Skill Gap Agent

    Compares the student's current skills with the
    skills required for the recommended career.
    """

    career_requirements = {

        "AI Engineer": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Generative AI",
            "LLM",
            "RAG",
            "Agentic AI",
            "Model Deployment",
            "MLOps"
        ],

        "Machine Learning Engineer": [
            "Python",
            "Machine Learning",
            "Statistics",
            "Deep Learning",
            "Scikit-learn",
            "TensorFlow",
            "Model Deployment",
            "MLOps"
        ],

        "Data Scientist": [
            "Python",
            "SQL",
            "Statistics",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "Data Visualization"
        ],

        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "SQL",
            "MongoDB",
            "REST APIs"
        ],

        "Software Developer": [
            "Python",
            "Java",
            "Data Structures",
            "Algorithms",
            "SQL",
            "Git",
            "REST APIs"
        ]
    }

    required_skills = career_requirements.get(
        recommended_career,
        []
    )

    # Normalize current skills
    normalized_current = [
        skill.lower().strip()
        for skill in current_skills
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in normalized_current:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total = len(required_skills)

    if total > 0:
        readiness = round(
            (len(matched_skills) / total) * 100
        )
    else:
        readiness = 0

    return {
        "career": recommended_career,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "readiness_percentage": readiness
    }