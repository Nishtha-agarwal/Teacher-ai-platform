from backend.services.llm import ask_json


def classify_document(text):

    # Limit classification input so the prompt does not become huge.
    content = text[:15000]

    prompt = f"""
You are an educational document classifier.

Analyze the following educational document.

DOCUMENT:
{content}

Return ONLY valid JSON using exactly this structure:

{{
  "subject": "string",
  "grade": "string",
  "difficulty": "Beginner",
  "topic": "string",
  "chapter": "string",
  "category": "string"
}}

RULES:

1. subject:
   Identify the actual academic subject.
   Examples:
   Physics, Chemistry, Mathematics, Biology, Computer Science.

2. grade:
   Identify the class/grade from the document.

   If this is clearly an NCERT Class 12 document,
   return exactly:
   "12"

   If it is Class 11:
   return:
   "11"

   If the grade cannot be determined:
   return:
   "Unknown"

3. difficulty:
   Return EXACTLY ONE of:

   "Beginner"
   "Intermediate"
   "Advanced"

   NEVER return:
   "Beginner | Intermediate | Advanced"

4. topic:
   Identify the main topic of the document.

5. chapter:
   Identify the chapter number/name if available.

6. category:
   Return the academic category/subject.

7. Do not invent information.

8. Base the classification only on the document.

9. Return ONLY JSON.
"""

    return ask_json(prompt)
