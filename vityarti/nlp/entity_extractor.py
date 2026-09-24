"""
Module: nlp.entity_extractor
Purpose: Recognizes academic entities (Course Codes, Semesters, Faculty names, Dates/Topics).
"""
import re
from typing import Dict, Any, List


# Known course synonyms and codes
KNOWN_COURSES = {
    "cs101": "CS101 - Introduction to Programming (Python)",
    "python": "CS101 - Introduction to Programming (Python)",
    "cs201": "CS201 - Data Structures and Algorithms",
    "dsa": "CS201 - Data Structures and Algorithms",
    "data structures": "CS201 - Data Structures and Algorithms",
    "cs301": "CS301 - Artificial Intelligence & Machine Learning",
    "ai": "CS301 - Artificial Intelligence & Machine Learning",
    "ml": "CS301 - Artificial Intelligence & Machine Learning",
    "machine learning": "CS301 - Artificial Intelligence & Machine Learning",
    "cs302": "CS302 - Full Stack Web Development",
    "web development": "CS302 - Full Stack Web Development",
    "web dev": "CS302 - Full Stack Web Development",
    "mat101": "MAT101 - Discrete Mathematics & Linear Algebra",
    "maths": "MAT101 - Discrete Mathematics & Linear Algebra",
    "math": "MAT101 - Discrete Mathematics & Linear Algebra"
}

# Known faculty aliases
KNOWN_FACULTY = {
    "sharma": "Dr. R. K. Sharma (Head of Department - CSE)",
    "verma": "Prof. Ananya Verma (AI & Data Science Lead)",
    "patel": "Dr. Sunil Patel (Systems & Web Technologies)",
    "gupta": "Prof. Priya Gupta (Mathematics & Cryptography)"
}


class EntityExtractor:
    """Extracts structured academic entities from conversational text."""

    def __init__(self):
        # Regex patterns for standard academic tokens
        self.course_code_regex = re.compile(r"\b([a-zA-Z]{2,4}\s?[0-9]{3,4})\b", re.IGNORECASE)
        self.semester_regex = re.compile(r"\b(sem(?:ester)?\s*[1-8]|(?:1st|2nd|3rd|[4-8]th)\s*sem(?:ester)?)\b", re.IGNORECASE)
        self.exam_type_regex = re.compile(r"\b(mid\s*term|cat\s*[12]|fat|final\s*exam|quiz|end\s*sem(?:ester)?)\b", re.IGNORECASE)

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract all identifiable academic entities from the text.
        Returns a dictionary of found entities.
        """
        entities: Dict[str, Any] = {
            "course": None,
            "course_code": None,
            "semester": None,
            "exam_type": None,
            "faculty": None
        }

        lowered = text.lower()

        # 1. Extract course code via regex
        code_match = self.course_code_regex.search(text)
        if code_match:
            code = code_match.group(1).replace(" ", "").upper()
            entities["course_code"] = code

        # 2. Extract course alias / title
        for alias, full_title in KNOWN_COURSES.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", lowered):
                entities["course"] = full_title
                if not entities["course_code"]:
                    entities["course_code"] = full_title.split()[0]
                break

        # 3. Extract semester
        sem_match = self.semester_regex.search(text)
        if sem_match:
            entities["semester"] = sem_match.group(1).strip()

        # 4. Extract exam type
        exam_match = self.exam_type_regex.search(text)
        if exam_match:
            entities["exam_type"] = exam_match.group(1).strip()

        # 5. Extract faculty reference
        for name_key, full_prof in KNOWN_FACULTY.items():
            if name_key in lowered:
                entities["faculty"] = full_prof
                break

        return {k: v for k, v in entities.items() if v is not None}
