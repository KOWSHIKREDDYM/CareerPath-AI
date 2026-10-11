from fastapi import Form
from backend.auth import hash_password, verify_password
from backend.database import get_connection, init_database

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pypdf import PdfReader

from backend.career_agent import career_advisor
from backend.skill_gap_agent import skill_gap_analyzer
from backend.learning_roadmap_agent import learning_roadmap_generator
from backend.agent_orchestrator import run_careerpath_workflow
from backend.career_coach_agent import career_coach

import io

app = FastAPI(
    title="CareerPath AI",
    description="Agentic AI Career Guidance Platform",
    version="1.0.0"
)

init_database()

@app.post("/api/auth/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    name = name.strip()
    email = email.strip().lower()

    if len(name) < 2:
        return {
            "success": False,
            "message": "Please enter a valid name."
        }

    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must be at least 6 characters."
        }

    connection = get_connection()
    cursor = connection.cursor()

    existing_user = cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        connection.close()
        return {
            "success": False,
            "message": "An account with this email already exists."
        }

    password_hash = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (name, email, password_hash)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return {
        "success": True,
        "message": "Account created successfully.",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }

@app.post("/api/auth/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    email = email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    user = cursor.execute(
        """
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    if not verify_password(password, user["password_hash"]):
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/resume/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Please upload a PDF resume."
        }

    file_content = await file.read()

    try:
        pdf = PdfReader(io.BytesIO(file_content))

        extracted_text = ""

        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        return {
            "success": True,
            "filename": file.filename,
            "pages": len(pdf.pages),
            "text": extracted_text[:10000]
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Could not analyze the PDF: {str(e)}"
        }

@app.post("/api/career/analyze")
async def analyze_career(data: dict):

    profile = data.get("profile", {})
    resume_text = data.get("resume_text", "")

    result = career_advisor(
        profile,
        resume_text
    )

    return {
        "success": True,
        "analysis": result
    }    

@app.post("/api/skill-gap/analyze")
async def analyze_skill_gap(data: dict):

    recommended_career = data.get(
        "recommended_career",
        ""
    )

    current_skills = data.get(
        "current_skills",
        []
    )

    result = skill_gap_analyzer(
        recommended_career,
        current_skills
    )

    return {
        "success": True,
        "analysis": result
    }

@app.post("/api/roadmap/generate")
async def generate_roadmap(data: dict):

    missing_skills = data.get(
        "missing_skills",
        []
    )

    result = learning_roadmap_generator(
        missing_skills
    )

    return {
        "success": True,
        "analysis": result
    }

@app.post("/api/careerpath/analyze")
async def analyze_careerpath(data: dict):

    profile = data.get("profile", {})
    resume_text = data.get("resume_text", "")

    result = run_careerpath_workflow(
        profile,
        resume_text
    )

    return {
        "success": True,
        "workflow": result
    }

@app.post("/api/career-coach")
async def career_coach_api(data: dict):
    question = data.get("question", "").strip()
    profile = data.get("profile", {})
    resume_text = data.get("resume_text", "")

    if not question:
        return {
            "success": False,
            "message": "Please enter a question."
        }

    result = career_coach(
        question=question,
        profile=profile,
        resume_text=resume_text
    )

    return result

# ============================================================
# INTERVIEW ANSWER EVALUATION
# ============================================================

from pydantic import BaseModel


class InterviewEvaluationRequest(BaseModel):
    career: str
    question: str
    answer: str


# ------------------------------------------------------------
# Interview evaluation knowledge
# ------------------------------------------------------------

INTERVIEW_RUBRICS = {

    "supervised and unsupervised": {
        "concepts": [
            "supervised learning",
            "unsupervised learning",
            "labeled data",
            "unlabeled data",
            "classification",
            "clustering"
        ],
        "model_answer": (
            "Supervised learning uses labeled data to learn a mapping "
            "between inputs and known outputs. Classification and regression "
            "are common supervised learning tasks. Unsupervised learning "
            "uses unlabeled data to discover patterns or structure, such as "
            "clustering."
        )
    },

    "mean median mode": {
        "concepts": [
            "mean",
            "median",
            "mode"
        ],
        "model_answer": (
            "Mean is the average of all values. Median is the middle value "
            "after sorting the data. Mode is the value that occurs most often. "
            "Median is often useful when the data contains extreme outliers."
        )
    },

    "pandas": {
        "concepts": [
            "pandas",
            "dataframe",
            "data manipulation",
            "data cleaning"
        ],
        "model_answer": (
            "Pandas is a Python library used for data manipulation and analysis. "
            "It provides structures such as DataFrames and supports operations "
            "such as filtering, cleaning, grouping and analyzing datasets."
        )
    },

    "overfitting": {
        "concepts": [
            "overfitting",
            "training data",
            "unseen data",
            "generalization"
        ],
        "model_answer": (
            "Overfitting occurs when a model learns the training data too closely, "
            "including noise, and therefore performs poorly on unseen data. "
            "It can be reduced using techniques such as regularization, "
            "cross-validation, simpler models or more training data."
        )
    },

    "data preprocessing": {
        "concepts": [
            "missing values",
            "outliers",
            "scaling",
            "encoding",
            "duplicates",
            "cleaning"
        ],
        "model_answer": (
            "Data preprocessing prepares raw data for machine learning. "
            "It can include handling missing values and duplicates, treating "
            "outliers, encoding categorical variables and scaling numerical "
            "features where necessary."
        )
    },

    "missing values": {
        "concepts": [
            "missing values",
            "delete",
            "imputation",
            "mean",
            "median",
            "mode"
        ],
        "model_answer": (
            "Missing values can be handled by removing affected rows or columns "
            "when appropriate, or by imputing values using techniques such as "
            "mean, median or mode imputation. The method should depend on the "
            "dataset and the reason values are missing."
        )
    },

    "precision recall f1": {
        "concepts": [
            "precision",
            "recall",
            "f1",
            "false positive",
            "false negative"
        ],
        "model_answer": (
            "Precision measures how many predicted positives are actually "
            "positive. Recall measures how many actual positives were found. "
            "F1-score is the harmonic mean of precision and recall and is useful "
            "when both are important."
        )
    },

    "cross-validation": {
        "concepts": [
            "cross-validation",
            "fold",
            "training",
            "validation",
            "generalization"
        ],
        "model_answer": (
            "Cross-validation divides the dataset into multiple folds and trains "
            "and validates the model across different train-validation splits. "
            "It provides a more reliable estimate of model generalization."
        )
    },

    "stack and queue": {
        "concepts": [
            "stack",
            "queue",
            "lifo",
            "fifo"
        ],
        "model_answer": (
            "A stack follows LIFO, meaning the last element inserted is the first "
            "one removed. A queue follows FIFO, meaning the first element inserted "
            "is the first one removed."
        )
    },

    "object-oriented programming": {
        "concepts": [
            "encapsulation",
            "inheritance",
            "polymorphism",
            "abstraction"
        ],
        "model_answer": (
            "Object-oriented programming organizes software around objects and "
            "classes. Its main concepts include encapsulation, inheritance, "
            "polymorphism and abstraction."
        )
    },

    "api": {
        "concepts": [
            "api",
            "application programming interface",
            "request",
            "response"
        ],
        "model_answer": (
            "An API is an interface that allows software applications to "
            "communicate with each other. A client sends a request to an API "
            "and the server processes it and returns a response."
        )
    },

    "machine learning": {
        "concepts": [
            "machine learning",
            "data",
            "patterns",
            "prediction",
            "model"
        ],
        "model_answer": (
            "Machine learning is a branch of artificial intelligence where "
            "models learn patterns from data and use those patterns to make "
            "predictions or decisions without being explicitly programmed "
            "with every rule."
        )
    },

    "classification and regression": {
        "concepts": [
            "classification",
            "regression",
            "categories",
            "continuous",
            "prediction"
        ],
        "model_answer": (
            "Classification predicts discrete categories, such as spam or "
            "not spam. Regression predicts continuous numerical values, "
            "such as house prices."
        )
    },

    "generative ai": {
        "concepts": [
            "generative ai",
            "generate",
            "text",
            "image",
            "code",
            "content"
        ],
        "model_answer": (
            "Generative AI refers to AI systems that generate new content "
            "such as text, images, audio or code based on learned patterns "
            "from training data."
        )
    },

    "large language model": {
        "concepts": [
            "llm",
            "large language model",
            "language",
            "text",
            "tokens",
            "generate"
        ],
        "model_answer": (
            "A large language model is an AI model trained on large amounts "
            "of text to understand and generate language. LLMs can perform "
            "tasks such as answering questions, summarization and code generation."
        )
    },

    "rag": {
        "concepts": [
            "rag",
            "retrieval",
            "augmented generation",
            "documents",
            "knowledge",
            "llm"
        ],
        "model_answer": (
            "Retrieval-Augmented Generation combines information retrieval "
            "with an LLM. Relevant information is retrieved from an external "
            "knowledge source and provided to the model so that the generated "
            "answer can be grounded in that information."
        )
    },

    "ai agent": {
        "concepts": [
            "agent",
            "goal",
            "reasoning",
            "tools",
            "actions"
        ],
        "model_answer": (
            "An AI agent is a system that works toward a goal by reasoning "
            "about a task and potentially using tools or taking actions. "
            "An agentic system can plan steps, use tools and respond based "
            "on the results."
        )
    },

    "html": {
        "concepts": [
            "html",
            "structure",
            "web page",
            "elements",
            "markup"
        ],
        "model_answer": (
            "HTML, or HyperText Markup Language, provides the structure of "
            "web pages using elements such as headings, paragraphs, links, "
            "images and forms."
        )
    },

    "css": {
        "concepts": [
            "css",
            "style",
            "layout",
            "design",
            "responsive"
        ],
        "model_answer": (
            "CSS is used to style and lay out HTML content. It controls "
            "properties such as colors, spacing, typography, positioning "
            "and responsive layouts."
        )
    },

    "javascript": {
        "concepts": [
            "javascript",
            "interactive",
            "dynamic",
            "browser",
            "web"
        ],
        "model_answer": (
            "JavaScript is a programming language commonly used to add "
            "interactivity and dynamic behavior to web applications. "
            "It can manipulate the DOM, respond to user events and "
            "communicate with backend APIs."
        )
    },

    "react": {
        "concepts": [
            "react",
            "component",
            "state",
            "props",
            "ui"
        ],
        "model_answer": (
            "React is a JavaScript library for building user interfaces "
            "using reusable components. Components can manage state and "
            "receive data through props."
        )
    },

    "node.js": {
        "concepts": [
            "node.js",
            "javascript",
            "runtime",
            "server",
            "backend"
        ],
        "model_answer": (
            "Node.js is a JavaScript runtime that allows JavaScript to run "
            "outside the browser. It is commonly used for backend services, "
            "APIs and server-side applications."
        )
    },

    "rest api": {
        "concepts": [
            "rest",
            "api",
            "http",
            "get",
            "post",
            "put",
            "delete",
            "request",
            "response"
        ],
        "model_answer": (
            "A REST API exposes resources through HTTP endpoints. Common "
            "HTTP methods include GET for retrieving data, POST for creating "
            "data, PUT or PATCH for updating data and DELETE for removing data."
        )
    }
}


# ------------------------------------------------------------
# Find the closest interview rubric
# ------------------------------------------------------------

def find_interview_rubric(question: str):

    question_lower = question.lower()

    for topic, rubric in INTERVIEW_RUBRICS.items():

        topic_words = topic.lower().split()

        if all(word in question_lower for word in topic_words):
            return rubric

    return None


# ------------------------------------------------------------
# Evaluate answer deterministically
# ------------------------------------------------------------

def evaluate_interview_answer_locally(
    question: str,
    answer: str
):

    answer_lower = answer.lower().strip()

    rubric = find_interview_rubric(question)

    if not rubric:

        # Generic fallback evaluation
        word_count = len(answer.split())

        if word_count < 10:
            score = 3
        elif word_count < 25:
            score = 5
        elif word_count < 50:
            score = 7
        else:
            score = 8

        return {
            "score": score,
            "strengths": [
                "You attempted to answer the interview question.",
                "Your answer provides some explanation."
            ],
            "weaknesses": [
                "The answer could contain more technical details.",
                "A concrete example would make the explanation stronger."
            ],
            "improvement": [
                "Explain the key concept clearly.",
                "Add a practical example where appropriate."
            ],
            "model_answer": (
                "A strong interview answer should clearly define the "
                "concept, explain how it works and provide a practical "
                "example when appropriate."
            )
        }

    matched = []
    missing = []

    for concept in rubric["concepts"]:

        if concept.lower() in answer_lower:
            matched.append(concept)
        else:
            missing.append(concept)

    total = len(rubric["concepts"])

    coverage = len(matched) / total if total else 0

    # Base score from concept coverage
    score = round(coverage * 10)

    # Minimum score for a meaningful answer
    if len(answer.split()) >= 10 and score < 4:
        score = 4

    if len(answer.split()) >= 25 and score < 5:
        score += 1

    score = min(score, 10)

    strengths = []

    if matched:
        strengths.append(
            "Correctly covers: " +
            ", ".join(matched[:4]) + "."
        )

    if len(answer.split()) >= 20:
        strengths.append(
            "Provides a reasonably clear technical explanation."
        )
    else:
        strengths.append(
            "The answer is concise and focused."
        )

    weaknesses = []

    if missing:
        weaknesses.append(
            "Could also mention: " +
            ", ".join(missing[:3]) + "."
        )

    if len(answer.split()) < 15:
        weaknesses.append(
            "The explanation is quite brief."
        )

    if not weaknesses:
        weaknesses.append(
            "The answer is strong, but a practical example could make it even better."
        )

    improvement = []

    if missing:
        improvement.append(
            "Add the missing technical concepts to make the explanation more complete."
        )

    improvement.append(
        "Use a simple real-world example when explaining the concept in an interview."
    )

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvement": improvement,
        "model_answer": rubric["model_answer"]
    }


# ============================================================
# API ENDPOINT
# ============================================================

@app.post("/api/interview-evaluate")
async def evaluate_interview_answer(
    request: InterviewEvaluationRequest
):

    try:

        answer = request.answer.strip()

        if not answer:

            return {
                "success": False,
                "message": "Please provide an answer before evaluating."
            }

        evaluation = evaluate_interview_answer_locally(
            request.question,
            answer
        )

        formatted_evaluation = f"""
Score: {evaluation["score"]}/10

Strengths:
{chr(10).join("- " + item for item in evaluation["strengths"])}

Weaknesses:
{chr(10).join("- " + item for item in evaluation["weaknesses"])}

Improvement:
{chr(10).join("- " + item for item in evaluation["improvement"])}


Model Answer:
{evaluation["model_answer"]}
"""

        return {
            "success": True,
            "career": request.career,
            "question": request.question,
            "evaluation": formatted_evaluation.strip()
        }

    except Exception as e:

        print(
            "Interview evaluation error:",
            str(e)
        )

        return {
            "success": False,
            "message": "Interview evaluation failed.",
            "error": str(e)
        }