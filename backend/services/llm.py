import json
import re
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:3b"


def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,
        },
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Run 'ollama serve' first."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"Ollama API error: {e}"
        )


def clean_json_text(text: str) -> str:
    """
    Remove common formatting mistakes from LLM output.
    """

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    # Find JSON object if model added extra text
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


def ask_json(prompt: str):

    json_prompt = f"""
You are an educational AI system.

{prompt}

STRICT OUTPUT REQUIREMENTS:

Return ONLY one valid JSON object.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations.
Do NOT add comments.
Do NOT add text before the JSON.
Do NOT add text after the JSON.

All JSON keys must use double quotes.

All string values must use double quotes.

If a string contains a double quote, escape it as \\\".

Do not use trailing commas.

The result must be valid JSON that can be parsed by:

json.loads()

Return exactly one JSON object.
"""

    raw = ask_llm(json_prompt)

    print("\n========== OLLAMA RAW OUTPUT ==========")
    print(raw)
    print("=======================================\n")

    cleaned = clean_json_text(raw)

    # Attempt 1
    try:
        result = json.loads(cleaned)

        print("✓ JSON parsed successfully")

        return result

    except json.JSONDecodeError as error:

        print("JSON parsing failed:")
        print(error)

    # Attempt 2: ask Ollama to repair the JSON
    repair_prompt = f"""
You are a JSON repair system.

The following output is supposed to be JSON but is invalid.

Repair it.

IMPORTANT:

- Return ONLY valid JSON.
- Do not use Markdown.
- Do not explain anything.
- Do not change the meaning.
- Do not remove valid information.
- Fix missing commas.
- Fix missing quotation marks.
- Escape quotes inside strings.
- Remove trailing commas.

INVALID JSON:

{cleaned}
"""

    repaired_raw = ask_llm(repair_prompt)

    print("\n========== REPAIRED OUTPUT ==========")
    print(repaired_raw)
    print("=====================================\n")

    repaired = clean_json_text(repaired_raw)

    # Attempt 3
    try:

        result = json.loads(repaired)

        print("✓ Repaired JSON parsed successfully")

        return result

    except json.JSONDecodeError as error:

        print("\n========== FINAL JSON ERROR ==========")
        print(error)
        print("\nOriginal output:")
        print(cleaned)
        print("\nRepaired output:")
        print(repaired)
        print("======================================")

        raise RuntimeError(
            f"Ollama returned invalid JSON: {error}"
        )