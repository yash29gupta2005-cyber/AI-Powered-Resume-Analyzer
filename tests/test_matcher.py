
from backend.skill_extractor import extract_skills, compare_skills
from backend.matcher import calculate_match_score


resume = """
I know C++, Python, SQL, MySQL, HTML, CSS,
JavaScript, Node.js, and Data Structures.
"""

job_description = """
Looking for a developer skilled in Python, SQL,
JavaScript, React, Node.js, and Machine Learning.
"""

print("Resume Skills:")
print(extract_skills(resume))

print("\nSkill Comparison:")

result = compare_skills(resume, job_description)

print("Required Skills:", result["required_skills"])
print("Matched Skills:", result["matched_skills"])
print("Missing Skills:", result["missing_skills"])

print("\nML Matching:")

score = calculate_match_score(resume, job_description)

print("Resume-Job Similarity Score:", str(score) + "%")

print("\n========== ALIAS TEST ==========")

test_text = """
I have experience in REST APIs,
OOP, Object Oriented Programming,
Problem-solving and RESTful API development.
"""

print("Detected Skills:", extract_skills(test_text))



