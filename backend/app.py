from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your routers
from api.upload import router as upload_router
from api.process import router as process_router

app.include_router(upload_router)
app.include_router(process_router)


@app.get("/health")
def health():
    return {"status": "ok"}
