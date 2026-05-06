from app.api.routes.document import router as document_router
from app.api.routes.upload import router as upload_router

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(document_router)
app.include_router(upload_router)