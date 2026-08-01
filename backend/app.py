from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.upload import router as upload_router
from backend.api.process import router as process_router

app = FastAPI(title="Teacher AI Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://teacher-ai-platform-2.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(process_router)

@app.get("/health")
def health():
    return {"status": "ok"}
