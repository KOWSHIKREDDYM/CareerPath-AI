from transformers import pipeline

# ============================================================

# CareerPath AI - Structured Career Knowledge

# ============================================================

CAREER_SKILLS = {

    "Data Scientist": [

        "Python",

        "SQL",

        "Statistics",

        "Pandas",

        "NumPy",

        "Machine Learning",

        "Data Visualization"

    ],

    "Software Developer": [

        "Python",

        "Java",

        "Data Structures",

        "Algorithms",

        "SQL",

        "Git",

        "REST APIs"

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

    "Full Stack Developer": [

        "HTML",

        "CSS",

        "JavaScript",

        "React",

        "Node.js",

        "SQL",

        "MongoDB",

        "REST APIs"

    ]

}

# ============================================================

# Load Local AI Model

# ============================================================

# Load the language model only when an open-ended Career Coach question needs it.
# This avoids loading model weights during application startup.
career_coach_model = None


def get_career_coach_model():
    """Create and cache the local text-generation pipeline on first use."""
    global career_coach_model

    if career_coach_model is None:
        career_coach_model = pipeline(
            "text-generation",
            model="HuggingFaceTB/SmolLM2-135M-Instruct",
            device="cpu"
        )

    return career_coach_model

# ============================================================

# Career Detection

# ============================================================

def resolve_career(question, target_career):

    """

    Resolve the student's target career using both:

    1. The saved profile target career

    2. The current question

    This prevents the AI model from being used for questions

    that can be answered directly from CareerPath knowledge.

    """

    question_lower = (question or "").lower()

    target_lower = (target_career or "").lower()

    career_aliases = {

        "Data Scientist": [

            "data scientist",

            "data science"

        ],

        "Software Developer": [

            "software developer",

            "software development",

            "software engineer",

            "software engineering"

        ],

        "Machine Learning Engineer": [

            "machine learning engineer",

            "ml engineer"

        ],

        "AI Engineer": [

            "ai engineer",

            "artificial intelligence engineer"

        ],

        "Full Stack Developer": [

            "full stack developer",

            "full-stack developer",

            "fullstack developer"

        ]

    }

    # --------------------------------------------------------

    # First check the student's saved target career.

    # --------------------------------------------------------

    for career, aliases in career_aliases.items():

        for alias in aliases:

            if alias in target_lower:

                return career

    # --------------------------------------------------------

    # If the profile does not identify the career,

    # check the current question.

    # --------------------------------------------------------

    for career, aliases in career_aliases.items():

        for alias in aliases:

            if alias in question_lower:

                return career

    return target_career


def get_career_skills(target_career):

    return CAREER_SKILLS.get(target_career, [])

# ============================================================

# Question Detection

# ============================================================

def is_skill_question(question):

    """

    Detect questions asking what skills are required.

    """

    text = question.lower()

    keywords = [

        "what skills",

        "which skills",

        "skills should i learn",

        "skills do i need",

        "skills required",

        "skills needed",

        "what should i learn",

        "what do i need to learn",

        "what technologies should i learn",

        "what technology should i learn"

    ]

    return any(keyword in text for keyword in keywords)

def is_skill_gap_question(question):

    """

    Detect questions asking about missing skills.

    """

    text = question.lower()

    keywords = [

        "skill gap",

        "skills am i missing",

        "skills i am missing",

        "what am i missing",

        "missing skills",

        "what skills do i lack",

        "what should i improve"

    ]

    return any(keyword in text for keyword in keywords)

# ============================================================

# Fast Career Skill Answer

# ============================================================

def create_skill_answer(target_career):

    """

    Generate a fast, deterministic answer using CareerPath's

    structured career requirements.

    """

    skills = get_career_skills(target_career)

    if not skills:

        return None

    lines = [

        f"To prepare for a {target_career} career, focus on these skills:"

    ]

    for index, skill in enumerate(skills, start=1):

        lines.append(f"{index}. {skill}")

    lines.append("")

    lines.append(

        "Recommended approach: learn the fundamentals first, "

        "then build projects that combine these skills."

    )

    return "\n".join(lines)

# ============================================================

# Fast Skill Gap Answer

# ============================================================

def create_skill_gap_answer(target_career, resume_text):

    """

    Compare the student's resume text with CareerPath's

    predefined requirements.

    """

    required_skills = get_career_skills(target_career)

    if not required_skills:

        return None

    resume_lower = (resume_text or "").lower()

    matched = []

    missing = []

    for skill in required_skills:

        skill_lower = skill.lower()

        if skill_lower in resume_lower:

            matched.append(skill)

        else:

            missing.append(skill)

    total = len(required_skills)

    if total:

        readiness = round((len(matched) / total) * 100)

    else:

        readiness = 0

    answer = [

        f"Your CareerPath skill-gap summary for {target_career}:",

        "",

        f"Career readiness based on the available resume text: {readiness}%",

        ""

    ]

    if matched:

        answer.append("Skills already found in your resume:")

        for skill in matched:

            answer.append(f"• {skill}")

        answer.append("")

    if missing:

        answer.append("Skills to focus on next:")

        for skill in missing:

            answer.append(f"• {skill}")

        answer.append("")

    answer.append(

        "Use the missing skills as the starting point for your learning roadmap."

    )

    return "\n".join(answer)

# ============================================================

# AI Career Coach

# ============================================================

def career_coach(question, profile=None, resume_text=""):

    """

    Hybrid AI Career Coach.

    Structured career questions use CareerPath's knowledge

    directly for speed and accuracy.

    Open-ended questions use SmolLM2 for AI-generated guidance.

    """

    profile = profile or {}

    name = profile.get("name", "Student")

    branch = profile.get("branch", "Engineering")

    year = profile.get("year", "")

    original_target_career = profile.get("target_career", "")

    # --------------------------------------------------------

    # Resolve career from profile OR question.

    # --------------------------------------------------------

    target_career = resolve_career(

        question,

        original_target_career

    )

    # Keep resume context reasonably small.

    resume_context = (

        resume_text[:4000]

        if resume_text

        else "No resume information available."

    )

    try:

        # ====================================================

        # ROUTE 1: Career Skill Question

        # ====================================================

        if is_skill_question(question):

            answer = create_skill_answer(target_career)

            if answer:

                return {

                    "success": True,

                    "agent": "CareerPath Skill Knowledge Agent",

                    "question": question,

                    "answer": answer,

                    "context": {

                        "name": name,

                        "branch": branch,

                        "year": year,

                        "target_career": target_career,

                        "required_skills": get_career_skills(

                            target_career

                        )

                    }

                }

        # ====================================================

        # ROUTE 2: Skill Gap Question

        # ====================================================

        if is_skill_gap_question(question):

            answer = create_skill_gap_answer(

                target_career,

                resume_text

            )

            if answer:

                return {

                    "success": True,

                    "agent": "CareerPath Skill Gap Agent",

                    "question": question,

                    "answer": answer,

                    "context": {

                        "name": name,

                        "branch": branch,

                        "year": year,

                        "target_career": target_career,

                        "required_skills": get_career_skills(

                            target_career

                        )

                    }

                }

        # ====================================================

        # ROUTE 3: Open-ended AI Career Coach

        # ====================================================

        required_skills = get_career_skills(

            target_career

        )

        if required_skills:

            required_skills_text = ", ".join(

                required_skills

            )

        else:

            required_skills_text = (

                "No predefined career requirements available."

            )

        system_prompt = """

You are CareerPath AI, an AI career coach for engineering students.

Give short, practical and personalized career guidance.

You can help with:

- career planning

- learning plans

- projects

- resumes

- internships

- placements

- interviews

- career decisions

- study strategies

Rules:

1. Answer the student's actual question directly.

2. Do not repeat the question.

3. Do not start with "Based on the information provided".

4. Do not write "Student:".

5. Give practical actions the student can take.

6. Use the student's profile when relevant.

7. Use the resume only when relevant.

8. Keep the answer concise.

9. Prefer 3 to 5 useful points.

10. Do not invent facts about the student.

"""

        user_prompt = f"""

Student profile:

Name: {name}

Branch: {branch}

Year: {year}

Target career: {target_career}

CareerPath requirements for this career:

{required_skills_text}

Resume information:

{resume_context}

Student question:

{question}

Give a concise and practical answer.

"""

        messages = [

            {

                "role": "system",

                "content": system_prompt

            },

            {

                "role": "user",

                "content": user_prompt

            }

        ]

        # ----------------------------------------------------

        # Generate AI response.

        # ----------------------------------------------------

        result = get_career_coach_model()(
            messages,

            max_new_tokens=80,

            do_sample=False

        )

        generated = result[0]["generated_text"]

        if isinstance(generated, list):

            answer = generated[-1]["content"]

        else:

            answer = str(generated)

        return {

            "success": True,

            "agent": "AI Career Coach",

            "question": question,

            "answer": answer.strip(),

            "context": {

                "name": name,

                "branch": branch,

                "year": year,

                "target_career": target_career,

                "required_skills": required_skills

            }

        }

    except Exception as error:

        return {

            "success": False,

            "message": "The AI Career Coach could not generate a response.",

            "error": str(error)

        }
