"""
This route handles document summarization.

Flow:
1. retrieve chunks belonging to a document
2. combine chunk text
3. send summarization prompt to local LLM
4 return generated summary
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.document import Document
from app.models.chunk import Chunk

from app.services.llm_service import generate_response

from app.services.auth_dependency import get_current_user
from app.services.redis_service import redis_client


# api router for /summary path operations
router = APIRouter(prefix="/summary", tags=["summary"])

# path parameter - doc id
@router.post("/{document_id}")
def summarize_document(document_id: int, db: Session = Depends(get_db),
                       current_user = Depends(get_current_user)):
    """
    Generate summary for a document.
    """

    # Verify document exists
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )
    
    # Check cache for doc summary
    cache_key = f"summary:{document_id}"
    cached_summary = redis_client.get(cache_key)
    if cached_summary:
        return {
            "document_id": document_id,
            "filename": document.filename,
            "summary": cached_summary}

    # Retrieve document chunks
    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_index)
        .all()
    )

    # Combine chunk text into one document string
    document_text = "\n\n".join(
        chunk.text
        for chunk in chunks
    )

    # Build prompt
    prompt = f"""
You are a helpful AI assistant.

Generate a concise but informative summary
of the following document.

Document:
{document_text}

Summary:
"""

    summary = generate_response(prompt)

    # store summary in redis for 24 hrs
    redis_client.setex(cache_key, 86400, summary)

    return {
        "document_id": document_id,
        "filename": document.filename,
        "summary": summary,
    }