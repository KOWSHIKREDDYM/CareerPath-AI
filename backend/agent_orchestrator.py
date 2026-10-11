from backend.career_agent import career_advisor
from backend.skill_gap_agent import skill_gap_analyzer
from backend.learning_roadmap_agent import learning_roadmap_generator
from backend.project_recommendation_agent import project_recommendation_agent


def run_careerpath_workflow(profile, resume_text):
    """
    CareerPath AI Agent Orchestrator

    Runs the complete career guidance workflow:
    1. Career Advisor
    2. Skill Gap Analyzer
    3. Learning Roadmap Generator
    4. Project Recommendation Agent
    """

    # --------------------------------------------------
    # Agent 1: Career Advisor
    # --------------------------------------------------

    career_result = career_advisor(
        profile,
        resume_text
    )

    recommended_career = career_result[
        "recommended_career"
    ]

    matched_skills = career_result[
        "matched_skills"
    ]


    # --------------------------------------------------
    # Agent 2: Skill Gap Analyzer
    # --------------------------------------------------

    skill_gap_result = skill_gap_analyzer(
        recommended_career,
        matched_skills
    )

    missing_skills = skill_gap_result[
        "missing_skills"
    ]


    # --------------------------------------------------
    # Agent 3: Learning Roadmap
    # --------------------------------------------------

    roadmap_result = learning_roadmap_generator(
        missing_skills
    )

    
    # --------------------------------------------------
    # Agent 4: Project Recommendation
    # --------------------------------------------------

    project_result = project_recommendation_agent(
        recommended_career,
        missing_skills
    )


    # --------------------------------------------------
    # Final Agentic Workflow Result
    # --------------------------------------------------

    return {
        "career_analysis": career_result,

        "skill_gap_analysis": skill_gap_result,

        "learning_roadmap": roadmap_result,

        "project_recommendations": project_result
    }