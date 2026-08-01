from backend.services.llm import ask_json


def generate_classroom_content(
    knowledge,
    teaching_plan,
    classification
):

    prompt = f"""
Generate classroom teaching content.

CLASSIFICATION:
{classification}

KNOWLEDGE:
{knowledge}

TEACHING PLAN:
{teaching_plan}

Return ONLY valid JSON:

{{
    "entry_ticket": [
        "string"
    ],

    "teacher_script": [
        "string"
    ],

    "board_notes": [
        "string"
    ],

    "exit_ticket": [
        "string"
    ],

    "homework": [
        "string"
    ],

    "mentor_moment": [
        "string"
    ]
}}

Requirements:

- Entry ticket should activate prior knowledge.
- Teacher script should contain useful teaching prompts.
- Board notes should contain concise points a teacher can write.
- Exit ticket should check understanding.
- Homework should reinforce the lesson.
- Mentor moment should connect the topic to real-world applications.
"""
    
    return ask_json(prompt)
