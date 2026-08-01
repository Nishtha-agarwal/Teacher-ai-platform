from backend.services.llm import ask_json


def generate_tkp(chunks, classification=None):

    content = "\n\n".join(chunks)

    classification = classification or {}

    # ---------------------------------------------------------
    # GET PERIOD COUNT FROM CLASSIFICATION
    # ---------------------------------------------------------
    # The classifier should decide the appropriate number.
    # If unavailable, default to 3.
    # ---------------------------------------------------------

    period_count = classification.get("teaching_periods")

    if period_count is None:
        period_count = classification.get("estimated_periods")

    if period_count is None:
        period_count = classification.get("period_count")

    # Convert to integer safely
    try:
        period_count = int(period_count)
    except (TypeError, ValueError):
        period_count = 3

    # Prevent unreasonable values
    period_count = max(1, min(period_count, 20))

    prompt = f"""
You are an expert educational content designer creating a
Teacher Knowledge Package (TKP) from a source textbook/document.

Your job is to transform the supplied document into structured
teaching material WITHOUT inventing facts.

==================================================
SOURCE DOCUMENT
==================================================

{content}

==================================================
DOCUMENT CLASSIFICATION
==================================================

{classification}

==================================================
TEACHING PERIOD RULE — CRITICAL
==================================================

The document classification has determined that this chapter
should be taught in EXACTLY {period_count} teaching periods.

You MUST generate exactly {period_count} teaching periods.

The number of teaching periods MUST remain consistent
throughout the entire Teacher Knowledge Package.

DO NOT independently calculate a different number.

DO NOT change the number because the document is long or short.

DO NOT generate fewer periods.

DO NOT generate additional periods.

The final "teaching_periods" array MUST contain exactly
{period_count} objects.

Period numbers MUST be:

1, 2, 3, ... {period_count}

==================================================
PERIOD DISTRIBUTION
==================================================

Distribute the actual chapter content across exactly
{period_count} periods.

The distribution should be based on:

- chapter length
- number of concepts
- concept complexity
- derivations
- examples
- activities
- exercises
- assessment content

Do NOT invent content to fill periods.

If one period contains more concepts than another, that is
acceptable.

Every period must contain only source-supported material.

==================================================
GROUNDING RULES
==================================================

1. Use ONLY information supported by the source document.

2. DO NOT invent facts, formulas, definitions, examples,
   experiments, numerical values, or scientific claims.

3. If a fact is unclear or missing from the source,
   do not guess it.

4. Preserve scientific and mathematical formulas exactly
   when possible.

5. NEVER reconstruct a corrupted formula from memory.

6. If a formula cannot be reliably extracted, describe
   the concept without inventing the formula.

7. Do not confuse similar concepts.

8. Examples must be based on examples, problems, or concepts
   actually present in the source.

9. Misconceptions must relate to concepts actually taught
   in the source.

10. Activities must be appropriate for classroom teaching
    and based on the source.

11. Assessment questions must test concepts appearing
    in the document.

12. Do not introduce knowledge from outside the document.

==================================================
DIFFICULTY RULE
==================================================

Choose EXACTLY ONE:

"Beginner"
"Intermediate"
"Advanced"

==================================================
GRADE RULE
==================================================

Use the classification information when available.

If the document is clearly an NCERT Class 12 textbook/chapter,
return:

"12"

If grade cannot be determined:

"Unknown"

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
  "title": "string",

  "summary": "string",

  "learning_objectives": [
    "string"
  ],

  "key_concepts": [
    "string"
  ],

  "prerequisites": [
    "string"
  ],

  "examples": [
    "string"
  ],

  "misconceptions": [
    "string"
  ],

  "activities": [
    "string"
  ],

  "assessment": [
    "string"
  ],

  "difficulty_level": "Beginner",

  "estimated_teaching_time": "{period_count} periods of 45 minutes",

  "teaching_periods": [
    {{
      "period": 1,
      "title": "string",
      "topics": [
        "string"
      ],
      "objectives": [
        "string"
      ],
      "activities": [
        "string"
      ],
      "assessment": [
        "string"
      ]
    }}
  ]
}}

IMPORTANT:

The example above shows the structure of ONE period.

You MUST repeat the period object until there are exactly
{period_count} periods.

==================================================
FIELD REQUIREMENTS
==================================================

title:
- Use the actual chapter/topic title from the document.

summary:
- Summarize only the source document.

learning_objectives:
- Write measurable objectives.
- Use verbs such as:
  identify, explain, calculate, compare, analyze,
  derive, demonstrate, classify, solve.

key_concepts:
- Extract important concepts directly from the document.

prerequisites:
- Include only prerequisites supported by the document context.

examples:
- Use examples/problems/applications actually found in the source.

misconceptions:
- Include realistic misconceptions related to source concepts.

activities:
- Create activities based on the actual document.

assessment:
- Create assessment questions based on the learning objectives.

difficulty_level:
- Return exactly one difficulty level.

estimated_teaching_time:
- Return exactly:

"{period_count} periods of 45 minutes"

teaching_periods:
- MUST contain exactly {period_count} objects.
- First object MUST have period = 1.
- Last object MUST have period = {period_count}.
- Period numbers must be sequential.
- No missing periods.
- No duplicate periods.
- No additional periods.

==================================================
FINAL VALIDATION
==================================================

Before returning JSON, verify:

1. Valid JSON.
2. All required fields exist.
3. difficulty_level contains exactly one value.
4. teaching_periods exists.
5. teaching_periods contains exactly {period_count} objects.
6. Period numbers are sequential from 1 to {period_count}.
7. estimated_teaching_time says exactly:
   "{period_count} periods of 45 minutes".
8. No additional periods exist.
9. No invented facts.
10. No Markdown.
11. No comments.

Return ONLY the JSON object.
"""

    result = ask_json(prompt)

    # ---------------------------------------------------------
    # PROGRAMMATIC VALIDATION
    # ---------------------------------------------------------

    if not isinstance(result, dict):
        raise RuntimeError(
            "TKP generator returned invalid JSON."
        )

    periods = result.get("teaching_periods")

    if not isinstance(periods, list):
        raise RuntimeError(
            "TKP does not contain teaching_periods."
        )

    # IMPORTANT:
    # The number must match the classifier's number.
    if len(periods) != period_count:
        raise RuntimeError(
            f"Period count mismatch. "
            f"Expected {period_count}, "
            f"but Gemini returned {len(periods)}."
        )

    expected_numbers = list(range(1, period_count + 1))

    actual_numbers = [
        period.get("period")
        for period in periods
    ]

    if actual_numbers != expected_numbers:
        raise RuntimeError(
            f"Invalid period numbering. "
            f"Expected {expected_numbers}, "
            f"got {actual_numbers}."
        )

    # Force consistent teaching time
    result["estimated_teaching_time"] = (
        f"{period_count} periods of 45 minutes"
    )

    return result

