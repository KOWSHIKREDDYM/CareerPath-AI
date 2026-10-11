def project_recommendation_agent(recommended_career, missing_skills):
    """
    Project Recommendation Agent

    Recommends practical projects based on the
    student's recommended career and skill gaps.
    """

    projects = {

        "AI Engineer": [
            {
                "title": "RAG-Based College Assistant",
                "description": "Build an AI assistant that answers questions from college documents using RAG.",
                "skills": ["LLM", "RAG", "Python"],
                "level": "Intermediate"
            },
            {
                "title": "AI Resume Analyzer",
                "description": "Build an AI system that extracts resume information and identifies career skill gaps.",
                "skills": ["Python", "Generative AI", "NLP"],
                "level": "Intermediate"
            },
            {
                "title": "Multi-Agent Career Advisor",
                "description": "Build a multi-agent system that analyzes careers, skills and learning paths.",
                "skills": ["Agentic AI", "Python", "LLM"],
                "level": "Advanced"
            },
            {
                "title": "AI Model Deployment Platform",
                "description": "Deploy an AI model through a FastAPI service with monitoring.",
                "skills": ["Model Deployment", "Python", "MLOps"],
                "level": "Advanced"
            }
        ],

        "Machine Learning Engineer": [
            {
                "title": "Student Performance Predictor",
                "description": "Build a machine learning model that predicts student academic performance.",
                "skills": ["Python", "Machine Learning", "Statistics"],
                "level": "Beginner"
            },
            {
                "title": "ML Model Deployment API",
                "description": "Train a machine learning model and deploy it through FastAPI.",
                "skills": ["Machine Learning", "Python", "Model Deployment"],
                "level": "Intermediate"
            },
            {
                "title": "ML Monitoring System",
                "description": "Create a system that monitors deployed machine learning models.",
                "skills": ["MLOps", "Model Deployment", "Machine Learning"],
                "level": "Advanced"
            }
        ],

        "Data Scientist": [
            {
                "title": "Student Data Analytics Dashboard",
                "description": "Analyze student data and create an interactive analytics dashboard.",
                "skills": ["Python", "SQL", "Data Visualization"],
                "level": "Beginner"
            },
            {
                "title": "Customer Churn Prediction",
                "description": "Build a machine learning model to predict customer churn.",
                "skills": ["Python", "Machine Learning", "Statistics"],
                "level": "Intermediate"
            },
            {
                "title": "Business Intelligence Analytics",
                "description": "Build a data analytics pipeline using SQL and visualization.",
                "skills": ["SQL", "Data Visualization", "Python"],
                "level": "Intermediate"
            }
        ],

        "Full Stack Developer": [
            {
                "title": "Student Management System",
                "description": "Build a full-stack application for managing student records.",
                "skills": ["HTML", "CSS", "JavaScript", "SQL"],
                "level": "Beginner"
            },
            {
                "title": "College Event Platform",
                "description": "Build a web application for creating and managing college events.",
                "skills": ["JavaScript", "React", "REST APIs"],
                "level": "Intermediate"
            },
            {
                "title": "E-Commerce Application",
                "description": "Build a complete e-commerce platform with frontend and backend.",
                "skills": ["React", "Node.js", "MongoDB"],
                "level": "Advanced"
            }
        ],

        "Software Developer": [
            {
                "title": "Library Management System",
                "description": "Build a software system for managing books, students and transactions.",
                "skills": ["Python", "SQL", "Git"],
                "level": "Beginner"
            },
            {
                "title": "Task Management API",
                "description": "Create a REST API for managing tasks and users.",
                "skills": ["Python", "REST APIs", "SQL"],
                "level": "Intermediate"
            },
            {
                "title": "Collaborative Coding Platform",
                "description": "Build a platform where students can collaborate on coding projects.",
                "skills": ["JavaScript", "REST APIs", "Git"],
                "level": "Advanced"
            }
        ]
    }

    career_projects = projects.get(
        recommended_career,
        []
    )

    # Normalize missing skills
    normalized_missing = [
        skill.lower().strip()
        for skill in missing_skills
    ]

    recommendations = []

    for project in career_projects:

        matching_skills = []

        for skill in project["skills"]:

            if skill.lower() in normalized_missing:
                matching_skills.append(skill)

        recommendations.append({
            "title": project["title"],
            "description": project["description"],
            "skills": project["skills"],
            "matching_skill_gaps": matching_skills,
            "level": project["level"]
        })

    # Projects that address more skill gaps come first
    recommendations.sort(
        key=lambda project: len(
            project["matching_skill_gaps"]
        ),
        reverse=True
    )

    return {
        "career": recommended_career,
        "recommended_projects": recommendations[:3]
    }