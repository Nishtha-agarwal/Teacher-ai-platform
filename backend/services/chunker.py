# backend/services/chunker.py

import re


def clean_text(text):

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


def chunk_text(
    text,
    max_words=400,
    overlap_words=50
):

    text = clean_text(text)

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    chunks = []

    current_words = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        words = paragraph.split()

        if (
            len(current_words)
            + len(words)
            <= max_words
        ):

            current_words.extend(words)

        else:

            if current_words:
                chunks.append(
                    " ".join(current_words)
                )

            overlap = current_words[
                -overlap_words:
            ]

            if len(words) > max_words:

                for i in range(
                    0,
                    len(words),
                    max_words - overlap_words
                ):

                    chunk = words[
                        i:i + max_words
                    ]

                    if chunk:
                        chunks.append(
                            " ".join(chunk)
                        )

                current_words = []

            else:

                current_words = (
                    overlap + words
                )

    if current_words:

        chunks.append(
            " ".join(current_words)
        )

    return chunks