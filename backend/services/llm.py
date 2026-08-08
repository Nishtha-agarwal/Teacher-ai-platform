import os
import time
import json
import re

from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

GEMINI_MAX_RETRIES = int(
    os.getenv("GEMINI_MAX_RETRIES", "3")
)


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():
    """
    Create and return Gemini client.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# ASK GEMINI
# ============================================================

def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini with controlled retry handling.

    429:
        Quota/rate limit exceeded.
        Do not retry.

    503:
        Temporary Gemini overload.
        Retry with exponential backoff.

    Timeout:
        Retry with exponential backoff.

    Returns:
        Gemini response as a string.
    """

    try:
        from google.genai import types

        client = get_gemini_client()

        for attempt in range(GEMINI_MAX_RETRIES):

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

                error_text = str(error)

                print(
                    f"[GEMINI] Error: {error_text}"
                )

                # ==================================================
                # 429 - QUOTA / RATE LIMIT
                # ==================================================

                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                    or "quota" in error_text.lower()
                    or "rate limit" in error_text.lower()
                ):

                    print(
                        "[GEMINI] Quota/rate limit exceeded."
                    )

                    raise RuntimeError(
                        "Gemini API quota/rate limit exceeded. "
                        "Please wait for the quota to reset "
                        "or check your Gemini API usage."
                    )

                # ==================================================
                # 503 - TEMPORARY UNAVAILABLE
                # ==================================================

                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "high demand" in error_text.lower()
                ):

                    if attempt < GEMINI_MAX_RETRIES - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"[GEMINI] Temporary failure. "
                            f"Retrying in {wait_time}s..."
                        )

                        time.sleep(wait_time)

                        continue

                    raise RuntimeError(
                        "Gemini is temporarily unavailable. "
                        "Please try again later."
                    )

                # ==================================================
                # TIMEOUT
                # ==================================================

                if (
                    "timeout" in error_text.lower()
                    or "timed out" in error_text.lower()
                ):

                    if attempt < GEMINI_MAX_RETRIES - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"[GEMINI] Timeout. "
                            f"Retrying in {wait_time}s..."
                        )

                        time.sleep(wait_time)

                        continue

                    raise RuntimeError(
                        "Gemini request timed out."
                    )

                # ==================================================
                # MODEL NOT FOUND
                # ==================================================

                if (
                    "404" in error_text
                    or "NOT_FOUND" in error_text
                    or "model not found" in error_text.lower()
                ):

                    raise RuntimeError(
                        f"Gemini model '{GEMINI_MODEL}' "
                        "was not found. Check GEMINI_MODEL."
                    )

                # ==================================================
                # OTHER ERROR
                # ==================================================

                raise RuntimeError(
                    f"Gemini API error: {error}"
                )

    except ImportError:

        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install google-genai"
        )


# ============================================================
# CLEAN GEMINI JSON
# ============================================================

def _clean_json_response(text: str) -> str:
    """
    Clean common Gemini JSON formatting problems.
    """

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    text = text.strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    return text


# ============================================================
# EXTRACT FIRST COMPLETE JSON OBJECT / ARRAY
# ============================================================

def _extract_json(text: str):
    """
    Extract the first complete JSON object or array.

    This protects against Gemini returning something like:

        {
            "subject": "Physics"
        }

        {
            "extra": "text"
        }

    or:

        Here is the JSON:

        {
            ...
        }

        Hope this helps.
    """

    text = _clean_json_response(text)

    # --------------------------------------------------------
    # First attempt: normal JSON parsing
    # --------------------------------------------------------

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Find first JSON object or array
    # --------------------------------------------------------

    start_positions = []

    object_start = text.find("{")
    array_start = text.find("[")

    if object_start != -1:
        start_positions.append(object_start)

    if array_start != -1:
        start_positions.append(array_start)

    if not start_positions:
        raise RuntimeError(
            "Gemini response does not contain valid JSON."
        )

    start = min(start_positions)

    opening = text[start]

    if opening == "{":
        closing = "}"
    else:
        closing = "]"

    # --------------------------------------------------------
    # Track nested objects/arrays
    # --------------------------------------------------------

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(text)):

        char = text[index]

        # Handle escaped characters inside strings
        if escape:
            escape = False
            continue

        if char == "\\" and in_string:
            escape = True
            continue

        # Toggle string state
        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        # Opening brackets
        if char == "{" or char == "[":
            depth += 1

        # Closing brackets
        elif char == "}" or char == "]":
            depth -= 1

            if depth == 0:

                candidate = text[
                    start:index + 1
                ].strip()

                try:
                    return json.loads(candidate)

                except json.JSONDecodeError as error:

                    raise RuntimeError(
                        "Gemini returned malformed JSON."
                    ) from error

    raise RuntimeError(
        "Could not find a complete JSON object in "
        "Gemini response."
    )


# ============================================================
# ASK JSON
# ============================================================

def ask_json(prompt: str):
    """
    Ask Gemini and return a Python dictionary/list.

    This function is compatible with:

        from backend.services.llm import ask_json
    """

    result = ask_gemini(prompt)

    parsed = _extract_json(result)

    print(
        "[GEMINI] JSON parsed successfully."
    )

    return parsed
