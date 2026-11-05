
import re


SKILLS = [
    "C++",
    "C",
    "Java",
    "Python",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Express.js",
    "FastAPI",
    "Flask",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Git",
    "GitHub",
    "REST API",
    "Data Structures",
    "Algorithms",
    "Object-Oriented Programming",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Docker",
    "Linux",
    "AWS",
    "Azure",
    "Communication",
    "Problem Solving"
]


# Alternative names and variations for skills
SKILL_ALIASES = {
    "REST API": [
        "REST APIs",
        "RESTful API",
        "RESTful APIs",
        "REST API development"
    ],
    "Object-Oriented Programming": [
        "OOP",
        "Object Oriented Programming",
        "Object-Oriented Programming"
    ],
    "Data Structures": [
        "Data Structure"
    ],
    "Algorithms": [
        "Algorithm"
    ],
    "Problem Solving": [
        "Problem-solving",
        "Problem solving skills"
    ]
}


def extract_skills(text):
    """
    Identify known skills and their alternative names.
    Returns a list of unique skill names.
    """
    found_skills = []
    text_lower = text.lower()

    for skill in SKILLS:

        # Special handling for C and C++
        if skill == "C":
            patterns = [r"(?<!\w)c(?![\w+])"]

        elif skill == "C++":
            patterns = [r"(?<!\w)c\+\+(?!\w)"]

        else:
            patterns = [
                r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
            ]

        # Add patterns for alternative skill names
        for alias in SKILL_ALIASES.get(skill, []):
            patterns.append(
                r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
            )

        # Check whether any pattern matches
        if any(re.search(pattern, text_lower) for pattern in patterns):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_text, job_description):
    """
    Compare resume skills with job description skills.
    """
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in resume_skills
    ]

    return {
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
