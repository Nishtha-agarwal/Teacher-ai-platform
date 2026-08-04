def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini with controlled retry handling.

    429:
        Quota/rate limit exceeded.
        Do not blindly retry.

    503:
        Temporary Gemini overload.
        Retry with exponential backoff.

    Timeout:
        Retry with exponential backoff.
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
                        response_mime_type="application/json"
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
