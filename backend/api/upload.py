# backend/api/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".md"
}


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload educational documents.
    Supported:
    - PDF
    - DOCX
    - PPTX
    - TXT
    - Markdown
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    unique_name = f"{uuid.uuid4()}{extension}"
    save_path = UPLOAD_DIR / unique_name

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "saved_as": unique_name,
            "path": str(save_path)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )