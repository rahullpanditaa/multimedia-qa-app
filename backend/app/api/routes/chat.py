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

from fastapi.responses import StreamingResponse

from app.core.config import settings

import requests
import json

from app.services.auth_dependency import get_current_user

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
def chat(payload: ChatRequest, db: Session = Depends(get_db),
         current_user = Depends(get_current_user)):
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

# streaming chat edpoint
@router.post("/stream")
def stream_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    document = (
        db.query(Document)
        .filter(Document.id == payload.document_id).first())
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    chunks = retrieve_similar_chunks(
        query=payload.question,
        document_id=payload.document_id,
        db=db,
    )

    context = "\n\n".join(
        chunk.text
        for chunk in chunks
    )

    prompt = f"""
Answer the user's question
using ONLY the provided context.

Context:
{context}

Question:
{payload.question}
"""

    def generate():

        response = requests.post(

            f"{settings.ollama_url}/api/generate",

            json={

                "model":
                    "mistral:latest",

                "prompt":
                    prompt,

                "stream":
                    True,
            },

            stream=True,
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get(
                    "response",
                    "",
                )

                yield token


    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )