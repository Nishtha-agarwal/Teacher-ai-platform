from services.llm import ask_json


def generate_tkp(chunks, classification=None):

    content = "\n\n".join(chunks)

    classification = classification or {}

    prompt = f"""
You are an expert educational content designer creating a
Teacher Knowledge Package (TKP) from a source textbook/document.

Your job is to transform the supplied document into structured
teaching material WITHOUT inventing facts.

========================
SOURCE DOCUMENT
========================

{content}

========================
DOCUMENT CLASSIFICATION
========================

{classification}

========================
IMPORTANT GROUNDING RULES
========================

1. Use ONLY information supported by the source document.

2. DO NOT invent facts, formulas, definitions, examples,
   experiments, numerical values, or scientific claims.

3. If a fact is unclear or missing from the source, do not guess it.

4. Preserve scientific and mathematical formulas exactly when
   possible.

5. NEVER reconstruct a corrupted formula from memory.

6. If the source contains a formula that cannot be reliably
   extracted, describe the concept without inventing a formula.

7. Do not confuse similar concepts.

8. Examples must be based on examples, problems, or concepts
   actually present in the source.

9. Misconceptions should be realistic and relevant to the
   concepts actually taught in the source.

10. Activities must be appropriate for classroom teaching and
    should be based on the source material.

11. Assessment questions must test concepts that actually appear
    in the document.

12. Do not introduce knowledge from outside the document.

========================
DIFFICULTY RULE
========================

Choose EXACTLY ONE difficulty level.

Allowed values:

"Beginner"
"Intermediate"
"Advanced"

NEVER return:

"Beginner | Intermediate | Advanced"

========================
GRADE RULE
========================

Use the classification information when available.

If the document is clearly an NCERT Class 12 textbook/chapter,
return:

"12"

If grade cannot be determined from the source, return:

"Unknown"

========================
OUTPUT FORMAT
========================

Return ONLY valid JSON.

Use exactly this structure:

{{
  "title": "string",

  "summary": "string",

  "learning_objectives": [
    "string",
    "string",
    "string"
  ],

  "key_concepts": [
    "string",
    "string",
    "string"
  ],

  "prerequisites": [
    "string",
    "string"
  ],

  "examples": [
    "string",
    "string"
  ],

  "misconceptions": [
    "string",
    "string"
  ],

  "activities": [
    "string",
    "string"
  ],

  "assessment": [
    "string",
    "string"
  ],

  "difficulty_level": "Beginner",

  "estimated_teaching_time": "string"
}}

========================
FIELD REQUIREMENTS
========================

title:
- Use the actual chapter/topic title from the document.
- Do not create a generic title if the actual title is available.

summary:
- Give a concise summary of the actual document.
- Do not introduce outside information.

learning_objectives:
- Write measurable objectives.
- Start objectives with verbs such as:
  identify, explain, calculate, compare, analyze, derive,
  demonstrate, classify, solve.
- Every objective must be supported by the document.

key_concepts:
- Extract important concepts directly from the document.
- Prefer terminology used by the source.

prerequisites:
- Include concepts that students need before learning this material.
- Only include prerequisites supported by the document context.

examples:
- Include examples/problems/applications found in the document.
- Do not invent numerical examples.

misconceptions:
- Include likely misconceptions related to the concepts.
- Do not state an unsupported misconception as a scientific fact.

activities:
- Create classroom activities based on the actual content.
- Do not require equipment or experiments unless the document
  supports them.

assessment:
- Create assessment items that test the learning objectives.
- Keep them grounded in the source.

difficulty_level:
- Return exactly ONE of:
  "Beginner"
  "Intermediate"
  "Advanced"

estimated_teaching_time:
- Estimate realistically based on the amount and complexity
  of the material.
- Example:
  "2-3 periods of 45 minutes"

========================
FINAL VALIDATION
========================

Before returning the response:

1. Make sure the response is valid JSON.
2. Make sure every required field exists.
3. Make sure difficulty_level contains exactly ONE value.
4. Make sure there are no Markdown code fences.
5. Make sure there are no comments.
6. Make sure formulas are not invented.
7. Make sure every factual claim is supported by the document.

Return ONLY the JSON object.
"""

    return ask_json(prompt)