def learning_roadmap_generator(missing_skills):
    """
    Learning Roadmap Agent

    Converts identified skill gaps into an ordered
    learning roadmap.
    """

    learning_paths = {
        "Python": {
            "order": 1,
            "description": "Strengthen Python programming and problem-solving.",
            "duration": "1-2 weeks"
        },

        "Machine Learning": {
            "order": 2,
            "description": "Learn supervised learning, unsupervised learning and model evaluation.",
            "duration": "2-3 weeks"
        },

        "Deep Learning": {
            "order": 3,
            "description": "Learn neural networks, CNNs, RNNs and transformer fundamentals.",
            "duration": "2-3 weeks"
        },

        "Generative AI": {
            "order": 4,
            "description": "Learn LLM concepts, prompt engineering and generative AI applications.",
            "duration": "1-2 weeks"
        },

        "LLM": {
            "order": 5,
            "description": "Learn large language model concepts, embeddings and model integration.",
            "duration": "1-2 weeks"
        },

        "RAG": {
            "order": 6,
            "description": "Learn retrieval augmented generation, vector databases and document retrieval.",
            "duration": "1-2 weeks"
        },

        "Agentic AI": {
            "order": 7,
            "description": "Learn AI agents, tool usage, planning and multi-agent workflows.",
            "duration": "1-2 weeks"
        },

        "Model Deployment": {
            "order": 8,
            "description": "Learn how to deploy machine learning and AI applications using APIs and cloud services.",
            "duration": "1-2 weeks"
        },

        "MLOps": {
            "order": 9,
            "description": "Learn model versioning, monitoring, CI/CD and production ML workflows.",
            "duration": "2-3 weeks"
        },

        "Statistics": {
            "order": 2,
            "description": "Strengthen probability, statistics and data analysis fundamentals.",
            "duration": "1-2 weeks"
        },

        "SQL": {
            "order": 3,
            "description": "Learn SQL queries, joins, aggregation and database design.",
            "duration": "1-2 weeks"
        },

        "Data Visualization": {
            "order": 4,
            "description": "Learn how to communicate data using charts and visualization tools.",
            "duration": "1 week"
        },

        "HTML": {
            "order": 1,
            "description": "Learn HTML structure and semantic web development.",
            "duration": "3-5 days"
        },

        "CSS": {
            "order": 2,
            "description": "Learn responsive layouts, styling and modern CSS.",
            "duration": "1 week"
        },

        "JavaScript": {
            "order": 3,
            "description": "Learn JavaScript fundamentals and browser programming.",
            "duration": "1-2 weeks"
        },

        "React": {
            "order": 4,
            "description": "Learn component-based frontend development with React.",
            "duration": "1-2 weeks"
        },

        "Git": {
            "order": 1,
            "description": "Learn Git version control and collaborative development workflows.",
            "duration": "3-5 days"
        },

        "Data Structures": {
            "order": 2,
            "description": "Learn arrays, linked lists, stacks, queues, trees and graphs.",
            "duration": "2-3 weeks"
        },

        "Algorithms": {
            "order": 3,
            "description": "Learn searching, sorting, recursion, graph algorithms and optimization.",
            "duration": "2-3 weeks"
        }
    }

    roadmap = []

    for skill in missing_skills:

        path = learning_paths.get(skill)

        if path:

            roadmap.append({
                "skill": skill,
                "order": path["order"],
                "description": path["description"],
                "duration": path["duration"]
            })

        else:

            roadmap.append({
                "skill": skill,
                "order": 99,
                "description": f"Develop practical knowledge of {skill}.",
                "duration": "1-2 weeks"
            })

    roadmap.sort(key=lambda item: item["order"])

    # Add learning steps
    for index, item in enumerate(roadmap, start=1):
        item["step"] = index

    return {
        "total_skills": len(roadmap),
        "roadmap": roadmap
    }