"""
This route connects the entire ingestion pipeline together.

Flow:
uploaded PDF
1. save file locally
2. create document row
3. extract text
4. chunk text
5. store chunks in database
"""

import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.document import Document
from app.models.chunk import Chunk

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text

from app.services.embedding_service import generate_embedding

# FastAPI router
router = APIRouter(prefix="/upload", tags=["upload"],)

# Directory where uploaded PDFs are stored
UPLOAD_DIRECTORY = "uploads"


@router.post("/pdf")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and process a PDF.
    """

    # Validate file type - basic validation.
    # Prevents non-PDF uploads.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    # Generate unique filename - prevents collisions between uploaded files.
    unique_filename = f"{uuid4()}_{file.filename}"

    # Full path where file will be saved
    filepath = os.path.join(
        UPLOAD_DIRECTORY,
        unique_filename,
    )

    # Save uploaded PDF locally
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create Document row
    document = Document(
        filename=file.filename,
        filepath=filepath,
        mime_type=file.content_type,
    )

    db.add(document)

    # Persist document row
    db.commit()

    db.refresh(document)

    # Extract text from pdf
    extracted_text = extract_text_from_pdf(filepath)

    # Chunking of extracted text
    chunks = chunk_text(extracted_text)

    # Store chunks in db
    for index, chunk in enumerate(chunks):

        # generate semantic embedding vector
        embedding = generate_embedding(chunk)

        chunk_row = Chunk(
            text=chunk,
            chunk_index=index,
            document_id=document.id,

            # store embedding vector
            embedding=embedding
        )

        db.add(chunk_row)

    db.commit()

    # Return a response
    return {
        "message": "PDF uploaded successfully",
        "document_id": document.id,
        "chunks_created": len(chunks),
    }