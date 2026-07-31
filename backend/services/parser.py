from pathlib import Path

from pypdf import PdfReader
import docx


def extract_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx(path):

    document = docx.Document(path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def extract_txt(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def extract_text(path):

    extension = Path(path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(path)

    elif extension == ".docx":
        return extract_docx(path)

    elif extension in [".txt", ".md"]:
        return extract_txt(path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )