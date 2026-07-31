# api/health.py

from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/")
async def root():
    return {"message": "Teacher AI Platform is running!"}

@router.get("/health")
async def health():
    return {"status": "healthy"}