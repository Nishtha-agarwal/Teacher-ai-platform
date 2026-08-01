from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.upload import router as upload_router
from backend.api.process import router as process_router

app = FastAPI(
    title="Teacher AI Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(upload_router)
app.include_router(process_router)


@app.get("/")
def root():
    return {
        "message": "Teacher AI Platform API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
