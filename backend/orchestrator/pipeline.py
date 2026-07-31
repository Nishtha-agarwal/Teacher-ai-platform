from services.parser import parse_document
from services.chunker import chunk_text

def run_pipeline(path):
    text = parse_document(path)
    chunks = chunk_text(text)

    return {
        "text_length": len(text),
        "chunks": len(chunks)
    }