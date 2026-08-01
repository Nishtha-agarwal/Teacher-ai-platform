from backend.services.llm import ask_json


def analyze_learning_gaps(
    knowledge,
    assessment
):

    prompt = f"""
Analyze potential learning gaps for students studying this topic.

KNOWLEDGE:
{knowledge}

ASSESSMENT:
{assessment}

Return ONLY valid JSON:

{{
    "diagnostic_questions": [
        "string"
    ],

    "common_gaps": [
        {{
            "concept": "string",
            "gap": "string",
            "indicator": "string"
        }}
    ],

    "remediation": [
        {{
            "gap": "string",
            "strategy": "string",
            "activity": "string"
        }}
    ]
}}

Identify:

- likely misconceptions
- prerequisite gaps
- difficult concepts
- diagnostic questions
- remediation strategies
"""
    
    return ask_json(prompt)
