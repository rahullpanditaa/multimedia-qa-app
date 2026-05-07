"""
This route implements the core RAG loop.

Flow:
1. receive user question
2. retrieve relevant chunks
3. build prompt context
4. send context to LLM
5. return grounded answer
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.retrieval_service import retrieve_similar_chunks
from app.services.llm_service import generate_response

from app.models.document import Document

# /chat path operations
router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """
    Request body for chat endpoint.
    """

    question: str

    # Document to search against
    document_id: int


@router.post("/")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Main RAG chat endpoint.
    """

    # validate doc exists
    document = db.query(Document).filter(Document.id == payload.document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )
    
    # Retrieve relevant chunks
    retrieved_chunks = retrieve_similar_chunks(
        query=payload.question,
        document_id=payload.document_id,
        db=db,
        limit=5,
    )

    # Build context to give to llm
    context = "\n\n".join(
        chunk.text
        for chunk in retrieved_chunks
    )

    # Build rag prompt
    prompt = f"""
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

If the answer is not contained in the context,
say you do not know.

Context:
{context}

Question:
{payload.question}

Answer:
"""

    # Generate llm response
    answer = generate_response(prompt)

    return {
        "question": payload.question,
        "answer": answer,
    }