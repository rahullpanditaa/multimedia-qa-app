from app.api.routes.document import router as document_router
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(document_router)