from app.api.routes.document import router as document_router
from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router
from app.api.routes.summary import router as summary_router
from app.api.routes.media import router as media_router
from app.api.routes.timestamps import router as timestamps_router


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# static file serving - uploaded media files can be accessed via url 
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS config
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
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