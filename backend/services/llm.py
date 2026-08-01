
import json
import os
import re

import requests


# ============================================================
# Configuration
# ============================================================

# Supported providers:
#   ollama
#   gemini
#
# Automatic behavior:
#   - If LLM_PROVIDER is explicitly set, use that provider.
#   - Otherwise, try Ollama first.
#   - If Ollama is unavailable and GEMINI_API_KEY exists,
#     automatically fall back to Gemini.

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").lower().strip()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# Gemini client
# ============================================================

_gemini_client = None


def get_gemini_client():
    """
    Lazily create the Gemini client.

    This prevents the application from failing during startup
    when Gemini is not being used locally.
    """

    global _gemini_client

    if _gemini_client is not None:
        return _gemini_client

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    try:
        from google import genai

        _gemini_client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        return _gemini_client

    except ImportError:
        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install google-genai"
        )


# ============================================================
# Ollama
# ============================================================

def ask_ollama(prompt: str) -> str:
    """
    Send a prompt to local Ollama.
    """

    payload = {
        "model": OLLAMA_MODEL,
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

        result = data.get("response")

        if not result:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return result

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Cannot connect to Ollama."
        )

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.HTTPError as error:

        raise RuntimeError(
            f"Ollama API error: {error}"
        )

    except requests.exceptions.RequestException as error:

        raise RuntimeError(
            f"Ollama request failed: {error}"
        )


# ============================================================
# Gemini
# ============================================================

def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini.
    """

    try:

        from google.genai import types

        client = get_gemini_client()

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )

        result = response.text

        if not result:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return result

    except Exception as error:

        raise RuntimeError(
            f"Gemini API error: {error}"
        )


# ============================================================
# Main LLM function
# ============================================================

def ask_llm(prompt: str) -> str:
    """
    Generate text using the configured LLM provider.

    Behavior:

    1. LLM_PROVIDER=ollama
       -> Ollama only

    2. LLM_PROVIDER=gemini
       -> Gemini only

    3. No LLM_PROVIDER:
       -> Try Ollama first
       -> Fall back to Gemini if Ollama is unavailable
    """

    # --------------------------------------------------------
    # Explicit Ollama
    # --------------------------------------------------------

    if LLM_PROVIDER == "ollama":

        print(
            f"[LLM] Using Ollama: {OLLAMA_MODEL}"
        )

        return ask_ollama(prompt)

    # --------------------------------------------------------
    # Explicit Gemini
    # --------------------------------------------------------

    if LLM_PROVIDER == "gemini":

        print(
            f"[LLM] Using Gemini: {GEMINI_MODEL}"
        )

        return ask_gemini(prompt)

    # --------------------------------------------------------
    # Automatic mode
    # --------------------------------------------------------

    print("[LLM] Automatic provider selection")

    # Try Ollama first
    try:

        print(
            f"[LLM] Trying Ollama: {OLLAMA_MODEL}"
        )

        return ask_ollama(prompt)

    except RuntimeError as ollama_error:

        print(
            f"[LLM] Ollama unavailable: {ollama_error}"
        )

    # Try Gemini fallback
    if GEMINI_API_KEY:

        print(
            f"[LLM] Falling back to Gemini: {GEMINI_MODEL}"
        )

        return ask_gemini(prompt)

    # Nothing available
    raise RuntimeError(
        "No LLM provider is available. "
        "Start Ollama or configure GEMINI_API_KEY."
    )


# ============================================================
# JSON cleaning
# ============================================================

def clean_json_text(text: str) -> str:
    """
    Remove common formatting mistakes from LLM output.
    """

    text = text.strip()

    # Remove markdown JSON fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove generic markdown fences
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

        text = text[
            start:end + 1
        ]

    return text.strip()


# ============================================================
# JSON generation
# ============================================================

def ask_json(prompt: str):
    """
    Generate and parse a JSON object.

    Uses the selected LLM provider and performs a second
    LLM call to repair malformed JSON if necessary.
    """

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

    # --------------------------------------------------------
    # First generation
    # --------------------------------------------------------

    raw = ask_llm(json_prompt)

    print(
        "\n========== LLM RAW OUTPUT =========="
    )
    print(raw)
    print(
        "====================================\n"
    )

    cleaned = clean_json_text(raw)

    # --------------------------------------------------------
    # Attempt 1: Direct JSON parsing
    # --------------------------------------------------------

    try:

        result = json.loads(cleaned)

        print(
            "✓ JSON parsed successfully"
        )

        return result

    except json.JSONDecodeError as error:

        print(
            "JSON parsing failed:"
        )

        print(error)

    # --------------------------------------------------------
    # Attempt 2: Ask the same LLM to repair JSON
    # --------------------------------------------------------

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

    repaired_raw = ask_llm(
        repair_prompt
    )

    print(
        "\n========== REPAIRED OUTPUT =========="
    )

    print(repaired_raw)

    print(
        "=====================================\n"
    )

    repaired = clean_json_text(
        repaired_raw
    )

    # --------------------------------------------------------
    # Attempt 3: Parse repaired JSON
    # --------------------------------------------------------

    try:

        result = json.loads(repaired)

        print(
            "✓ Repaired JSON parsed successfully"
        )

        return result

    except json.JSONDecodeError as error:

        print(
            "\n========== FINAL JSON ERROR =========="
        )

        print(error)

        print(
            "\nOriginal output:"
        )

        print(cleaned)

        print(
            "\nRepaired output:"
        )

        print(repaired)

        print(
            "======================================"
        )

        raise RuntimeError(
            f"LLM returned invalid JSON: {error}"
        )

