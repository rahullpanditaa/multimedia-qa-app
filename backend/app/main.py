from app.api.routes.document import router as document_router
from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router
from app.api.routes.summary import router as summary_router
from app.api.routes.media import router as media_router
from app.api.routes.timestamps import router as timestamps_router
from app.api.routes.auth import router as auth_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from pathlib import Path

app = FastAPI()

Path("uploads").mkdir(parents=True, exist_ok=True)

# static file serving - uploaded media files can be accessed via url 
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS config
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(document_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(summary_router)
app.include_router(media_router)
app.include_router(timestamps_router)
app.include_router(auth_router)