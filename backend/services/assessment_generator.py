from services.llm import ask_json


def generate_assessment(
    knowledge,
    teaching_plan
):

    prompt = f"""
Create an assessment for this educational topic.

KNOWLEDGE:
{knowledge}

TEACHING PLAN:
{teaching_plan}

Return ONLY valid JSON:

{{
    "mcqs": [
        {{
            "question": "string",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "answer": "A",
            "explanation": "string"
        }}
    ],

    "short_answer": [
        {{
            "question": "string",
            "answer": "string"
        }}
    ],

    "long_answer": [
        {{
            "question": "string",
            "answer": "string"
        }}
    ],

    "numerical": [
        {{
            "question": "string",
            "answer": "string",
            "solution": "string"
        }}
    ],

    "rubric": [
        {{
            "criterion": "string",
            "description": "string"
        }}
    ]
}}

Requirements:

- Include multiple question types.
- Questions must test the learning objectives.
- Include answer keys.
- Include explanations where useful.
- Numerical problems should include solutions.
- Avoid questions requiring information not present in the document.
"""
    
    return ask_json(prompt)