import json
import os
import re
import time
import requests

# ============================================================
# Configuration
# ============================================================

# Supported providers:
#   ollama
#   gemini
#
# Automatic mode:
#   Local machine:
#       Ollama -> preferred
#
#   Render:
#       Ollama unavailable -> Gemini
#
# You can also explicitly set:
#
#   LLM_PROVIDER=ollama
#   LLM_PROVIDER=gemini
#
# ============================================================

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    ""
).lower().strip()


# ============================================================
# Ollama Configuration
# ============================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


# ============================================================
# Gemini Configuration
# ============================================================

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# Number of retries for temporary Gemini failures
GEMINI_MAX_RETRIES = int(
    os.getenv(
        "GEMINI_MAX_RETRIES",
        "3"
    )
)


# ============================================================
# Gemini Client
# ============================================================

_gemini_client = None


def get_gemini_client():
    """
    Lazily create the Gemini client.

    This prevents the application from failing during startup
    when Gemini is not being used.
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
            "temperature": 0.1
        }
    }

    try:

        print(
            f"[OLLAMA] Model: {OLLAMA_MODEL}"
        )

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        result = data.get(
            "response"
        )

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

    Automatically retries temporary 503 errors.

    429 errors are reported clearly because they may indicate
    that the Gemini free-tier quota has been exhausted.
    """

    try:

        from google.genai import types

        client = get_gemini_client()

        for attempt in range(
            GEMINI_MAX_RETRIES
        ):

            try:

                print(
                    f"[GEMINI] Model: {GEMINI_MODEL}"
                )

                print(
                    f"[GEMINI] Attempt "
                    f"{attempt + 1}/"
                    f"{GEMINI_MAX_RETRIES}"
                )

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )

                result = response.text

                if not result:

                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                print(
                    "[GEMINI] Response received successfully."
                )

                return result

            except Exception as error:

                error_text = str(
                    error
                )

                # ------------------------------------------------
                # 429 - Quota / rate limit
                # ------------------------------------------------

                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED"
                    in error_text
                ):

                    raise RuntimeError(
                        "Gemini API quota/rate limit exceeded. "
                        "Please wait for the quota to reset "
                        "or check your Gemini API usage."
                    )

                # ------------------------------------------------
                # 503 - Temporary model overload
                # ------------------------------------------------

                if (
                    "503" in error_text
                    or "UNAVAILABLE"
                    in error_text
                    or "high demand"
                    in error_text.lower()
                ):

                    if attempt < GEMINI_MAX_RETRIES - 1:

                        wait_time = 5 * (
                            attempt + 1
                        )

                        print(
                            "[GEMINI] Model temporarily "
                            "unavailable."
                        )

                        print(
                            f"[GEMINI] Retrying in "
                            f"{wait_time} seconds..."
                        )

                        time.sleep(
                            wait_time
                        )

                        continue

                    raise RuntimeError(
                        "Gemini is temporarily unavailable "
                        "because the model is experiencing "
                        "high demand. Please try again later."
                    )

                # ------------------------------------------------
                # Timeout / temporary failure
                # ------------------------------------------------

                if (
                    "timeout" in error_text.lower()
                    or "timed out"
                    in error_text.lower()
                ):

                    if attempt < GEMINI_MAX_RETRIES - 1:

                        wait_time = 5 * (
                            attempt + 1
                        )

                        print(
                            f"[GEMINI] Timeout. "
                            f"Retrying in "
                            f"{wait_time}s..."
                        )

                        time.sleep(
                            wait_time
                        )

                        continue

                    raise RuntimeError(
                        "Gemini request timed out."
                    )

                # ------------------------------------------------
                # Other Gemini error
                # ------------------------------------------------

                raise RuntimeError(
                    f"Gemini API error: {error}"
                )

    except ImportError:

        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install google-genai"
        )


# ============================================================
# Main LLM Function
# ============================================================

def ask_llm(prompt: str) -> str:
    """
    Generate text using the configured LLM provider.

    Behavior:

    LLM_PROVIDER=ollama
        -> Ollama only

    LLM_PROVIDER=gemini
        -> Gemini only

    No LLM_PROVIDER
        -> Try Ollama first
        -> If Ollama unavailable, use Gemini
    """

    # ========================================================
    # Explicit Ollama
    # ========================================================

    if LLM_PROVIDER == "ollama":

        print(
            "[LLM] Provider explicitly set to Ollama."
        )

        return ask_ollama(
            prompt
        )


    # ========================================================
    # Explicit Gemini
    # ========================================================

    if LLM_PROVIDER == "gemini":

        print(
            "[LLM] Provider explicitly set to Gemini."
        )

        return ask_gemini(
            prompt
        )


    # ========================================================
    # Automatic Mode
    # ========================================================

    print(
        "[LLM] Automatic provider selection."
    )


    # ========================================================
    # Try Ollama First
    # ========================================================

    try:

        print(
            f"[LLM] Trying Ollama: "
            f"{OLLAMA_MODEL}"
        )

        return ask_ollama(
            prompt
        )

    except RuntimeError as ollama_error:

        print(
            f"[LLM] Ollama unavailable: "
            f"{ollama_error}"
        )


    # ========================================================
    # Gemini Fallback
    # ========================================================

    if GEMINI_API_KEY:

        print(
            f"[LLM] Falling back to Gemini: "
            f"{GEMINI_MODEL}"
        )

        return ask_gemini(
            prompt
        )


    # ========================================================
    # No Provider
    # ========================================================

    raise RuntimeError(
        "No LLM provider is available. "
        "Start Ollama or configure GEMINI_API_KEY."
    )


# ============================================================
# JSON Cleaning
# ============================================================

def clean_json_text(text: str) -> str:
    """
    Clean common formatting problems from LLM output.
    """

    if not text:

        raise RuntimeError(
            "LLM returned empty output."
        )

    text = text.strip()


    # --------------------------------------------------------
    # Remove ```json
    # --------------------------------------------------------

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )


    # --------------------------------------------------------
    # Remove ```
    # --------------------------------------------------------

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()


    # --------------------------------------------------------
    # Extract JSON object
    # --------------------------------------------------------

    start = text.find(
        "{"
    )

    end = text.rfind(
        "}"
    )

    if (
        start != -1
        and end != -1
        and end > start
    ):

        text = text[
            start:end + 1
        ]


    return text.strip()


# ============================================================
# JSON Generation
# ============================================================

def ask_json(prompt: str):
    """
    Generate a JSON object using the configured LLM.

    First attempt:
        Generate JSON.

    Second attempt:
        Only if the first response cannot be parsed,
        ask the LLM to repair it.

    This keeps the normal pipeline at ONE LLM request.
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

If a string contains a double quote,
escape it as \\\".

Do not use trailing commas.

The result must be valid JSON that can be parsed using:

json.loads()

Return exactly ONE JSON object.
"""


    # ========================================================
    # First Generation
    # ========================================================

    raw = ask_llm(
        json_prompt
    )


    print(
        "\n========== LLM RAW OUTPUT =========="
    )

    print(
        raw
    )

    print(
        "====================================\n"
    )


    # ========================================================
    # Clean
    # ========================================================

    cleaned = clean_json_text(
        raw
    )


    # ========================================================
    # Attempt 1 - Direct Parse
    # ========================================================

    try:

        result = json.loads(
            cleaned
        )

        print(
            "✓ JSON parsed successfully."
        )

        return result

    except json.JSONDecodeError as error:

        print(
            "JSON parsing failed:"
        )

        print(
            error
        )


    # ========================================================
    # Attempt 2 - JSON Repair
    # ========================================================

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


    print(
        "[LLM] Requesting JSON repair..."
    )


    repaired_raw = ask_llm(
        repair_prompt
    )


    print(
        "\n========== REPAIRED OUTPUT =========="
    )

    print(
        repaired_raw
    )

    print(
        "=====================================\n"
    )


    repaired = clean_json_text(
        repaired_raw
    )


    # ========================================================
    # Attempt 3 - Parse Repaired JSON
    # ========================================================

    try:

        result = json.loads(
            repaired
        )

        print(
            "✓ Repaired JSON parsed successfully."
        )

        return result

    except json.JSONDecodeError as error:

        print(
            "\n========== FINAL JSON ERROR =========="
        )

        print(
            error
        )

        print(
            "\nOriginal output:"
        )

        print(
            cleaned
        )

        print(
            "\nRepaired output:"
        )

        print(
            repaired
        )

        print(
            "======================================"
        )

        raise RuntimeError(
            f"LLM returned invalid JSON: {error}"
        )
