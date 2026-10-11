def career_advisor(profile, resume_text):
    """
    Career Advisor Agent

    Analyzes student profile + resume text
    and generates a career recommendation.
    """

    text = resume_text.lower()

    careers = {
        "Machine Learning Engineer": [
            "python",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "artificial intelligence"
        ],

        "Data Scientist": [
            "python",
            "sql",
            "machine learning",
            "statistics",
            "pandas",
            "numpy",
            "data analysis"
        ],

        "Full Stack Developer": [
            "html",
            "css",
            "javascript",
            "react",
            "node",
            "mongodb",
            "fastapi",
            "django"
        ],

        "AI Engineer": [
            "python",
            "artificial intelligence",
            "generative ai",
            "llm",
            "rag",
            "agentic ai",
            "machine learning"
        ],

        "Software Developer": [
            "python",
            "java",
            "javascript",
            "sql",
            "git",
            "github"
        ]
    }

    scores = {}

    for career, skills in careers.items():

        score = 0

        for skill in skills:
            if skill in text:
                score += 1

        scores[career] = score

    recommended_career = max(
        scores,
        key=scores.get
    )

    matched_skills = []

    for skill in careers[recommended_career]:

        if skill in text:
            matched_skills.append(skill)

    missing_skills = []

    for skill in careers[recommended_career]:

        if skill not in text:
            missing_skills.append(skill)

    return {
        "recommended_career": recommended_career,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "career_score": scores[recommended_career],
        "all_scores": scores
    }