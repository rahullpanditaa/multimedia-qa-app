from app.api.routes.document import router as document_router
from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router
from app.api.routes.summary import router as summary_router

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(document_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(summary_router)