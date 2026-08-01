from backend.services.llm import ask_json

def generate_activities(
    knowledge,
    teaching_plan
):

    prompt = f"""
Create classroom activities based on the educational content.

KNOWLEDGE:
{knowledge}

TEACHING PLAN:
{teaching_plan}

Return ONLY valid JSON:

{{
    "activities": [
        {{
            "name": "string",
            "type": "demonstration | experiment | discussion | role_play | group_work",
            "duration": "string",
            "instructions": [
                "string"
            ],
            "materials": [
                "string"
            ],
            "success_criteria": [
                "string"
            ]
        }}
    ]
}}

Create activities that are:

- age appropriate
- classroom feasible
- directly related to the topic
- interactive
- measurable
"""
    
    return ask_json(prompt)
