from backend.services.llm import ask_json


def classify_document(text):

    # ---------------------------------------------------------
    # Limit input size for classification.
    # We use enough content to understand the chapter.
    # ---------------------------------------------------------

    content = text[:20000]

    prompt = f"""
You are an expert educational document classifier and curriculum planner.

Analyze the educational document below.

==================================================
DOCUMENT
==================================================

{content}

==================================================
TASK
==================================================

Classify the document and estimate how many classroom
teaching periods are reasonably required to teach the
chapter completely.

The number of periods must depend on:

- Amount of content
- Number of major concepts
- Concept complexity
- Number of formulas
- Derivations
- Examples
- Problems/exercises
- Activities
- Conceptual difficulty
- Overall chapter depth

Do NOT automatically return 3 periods.

A short/simple chapter may require 2-3 periods.

A medium chapter may require 4-7 periods.

A large/complex chapter may require 8-12 periods.

A very large chapter may require more than 12 periods
if the source clearly supports that amount.

Do not inflate the number unnecessarily.

The goal is a realistic classroom teaching plan.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON using EXACTLY this structure:

{{
  "subject": "string",

  "grade": "string",

  "difficulty": "Beginner",

  "topic": "string",

  "chapter": "string",

  "category": "string",

  "teaching_periods": 3,

  "period_duration_minutes": 45,

  "period_reason": "string"
}}

==================================================
FIELD RULES
==================================================

subject:

Identify the actual academic subject.

Examples:

Physics
Chemistry
Mathematics
Biology
Computer Science

--------------------------------------------------

grade:

Identify the class/grade from the document.

If clearly NCERT Class 12:

"12"

If Class 11:

"11"

If the grade cannot be determined:

"Unknown"

--------------------------------------------------

difficulty:

Return EXACTLY ONE:

"Beginner"
"Intermediate"
"Advanced"

Never return multiple values.

--------------------------------------------------

topic:

Identify the main topic of the document.

Use terminology from the source.

--------------------------------------------------

chapter:

Identify the chapter number/name if available.

Use the actual chapter information from the source.

--------------------------------------------------

category:

Return the academic category/subject.

--------------------------------------------------

teaching_periods:

This is VERY IMPORTANT.

Return ONE integer.

This integer represents the total number of
45-minute classroom periods required to teach
the chapter.

The number must be based on the actual document.

Use the following general guidance:

1-3 periods:
Very short/simple material.

4-6 periods:
Moderate amount of material.

7-10 periods:
Large chapter with multiple concepts.

Do NOT always return 3.
Do NOT return a range.
Correct:
"teaching_periods": 8

Incorrect:

"teaching_periods": "8-10"

Incorrect:

"teaching_periods": "3-5"

--------------------------------------------------

period_duration_minutes:

Always return:

45

--------------------------------------------------

period_reason:

Briefly explain why the selected number of periods
is appropriate.

Mention actual characteristics of the document.

For example:

"Large chapter containing multiple major concepts,
derivations, examples and exercises."

Do not invent details that are not present.

==================================================
IMPORTANT CONSISTENCY RULE
==================================================

The value of "teaching_periods" will be passed directly
to the Teacher Knowledge Package generator.

Therefore:

Choose the number carefully.

Do not change it later.

The TKP generator MUST use exactly this number.

==================================================
GROUNDING RULES
==================================================

1. Use ONLY information supported by the document.

2. Do not invent chapter information.

3. Do not invent formulas.

4. Do not invent topics.

5. Do not use outside academic information.

6. Base the period estimate on the actual amount
   and complexity of the supplied document.

7. Return ONLY valid JSON.

8. Do not use Markdown.

9. Do not include explanations outside JSON.

==================================================
FINAL VALIDATION
==================================================

Before returning the response verify:

- subject exists
- grade exists
- difficulty is exactly one value
- topic exists
- chapter exists
- category exists
- teaching_periods is an integer
- teaching_periods is greater than 0
- period_duration_minutes is exactly 45
- period_reason exists

Return ONLY the JSON object.
"""

    result = ask_json(prompt)

    # ---------------------------------------------------------
    # PROGRAMMATIC VALIDATION
    # ---------------------------------------------------------

    if not isinstance(result, dict):
        raise RuntimeError(
            "Classifier returned invalid JSON."
        )

    # ---------------------------------------------------------
    # Validate teaching_periods
    # ---------------------------------------------------------

    period_count = result.get("teaching_periods")

    try:
        period_count = int(period_count)
    except (TypeError, ValueError):
        raise RuntimeError(
            "Classifier returned an invalid teaching_periods value."
        )

    if period_count < 1:
        raise RuntimeError(
            "teaching_periods must be greater than 0."
        )

    # Prevent accidental extreme values.
    if period_count > 20:
        period_count = 20

    result["teaching_periods"] = period_count

    # ---------------------------------------------------------
    # Period duration is fixed.
    # ---------------------------------------------------------

    result["period_duration_minutes"] = 45

    return result

