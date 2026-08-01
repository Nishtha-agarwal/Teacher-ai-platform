from backend.services.llm import ask_json


def generate_teaching_plan(knowledge, classification):

    prompt = f"""
Create a teaching plan for this educational topic.

CLASSIFICATION:
{classification}

KNOWLEDGE:
{knowledge}

Create a practical classroom teaching plan.

Return ONLY valid JSON with this structure:

{{
    "total_periods": 3,
    "periods": [
        {{
            "period": 1,
            "duration": "45-60 minutes",
            "topic": "string",
            "objectives": ["string"],
            "sequence": [
                "string"
            ]
        }}
    ]
}}

Requirements:

- Each period should be 40-60 minutes.
- Sequence concepts logically.
- Start with prerequisite concepts.
- Move from basic concepts to applications.
- Include a clear objective for every period.
"""

    return ask_json(prompt)
