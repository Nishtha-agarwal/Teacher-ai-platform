from backend.services.llm import ask_json


def extract_knowledge(text: str, classification: dict):

    prompt = f"""
You are an expert educational knowledge extractor.

SUBJECT:
{classification.get("subject")}

GRADE:
{classification.get("grade")}

TOPIC:
{classification.get("topic")}

DOCUMENT:
{text[:16000]}

Extract structured educational knowledge.

Return JSON:

{{
    "summary": "",
    "learning_objectives":  [
        "Calculate capacitance using the appropriate capacitance equations",
        "Understand electric potential and potential difference",
        "Explain the factors affecting the capacitance of a capacitor"
    ],
    "key_concepts": [],
    "keywords": [],
    "definitions": [],
    "formulas": [],
    "examples": [],
    "applications": [],
    "misconceptions": []
}}
"""

    return ask_json(prompt)
