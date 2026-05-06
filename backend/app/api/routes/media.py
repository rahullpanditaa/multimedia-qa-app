"""
This route is for media upload and transcription.
"""

import os
import shutil
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.document import Document
from app.models.transcript_segment import TranscriptSegment
from app.services.transcription_service import transcribe_media

from app.models.chunk import Chunk
from app.services.embedding_service import generate_embedding
from app.services.chunking_service import chunk_text

from app.services.transcript_window_service import create_transcript_windows

# API route for all /media path operations
router = APIRouter(prefix="/media", tags=["media"])

UPLOAD_DIRECTORY = "uploads"

@router.post("/upload")
def upload_media(file: UploadFile = File(...), 
                 db: Session = Depends(get_db)):

    # Save file
    unique_filename = f"{uuid4()}_{file.filename}"

    filepath = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create Document
    document = Document(
        filename=file.filename,
        filepath=filepath,
        mime_type=file.content_type,
        file_type="media",
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    segments = transcribe_media(filepath)

    # Create transcript windows
    windows = create_transcript_windows(segments=segments)

    # Build transcript text
    # Join all segments into one text block
    transcript_text = " ".join([segment["text"] for segment in segments])

    # chunk transcript
    chunks = chunk_text(transcript_text)

    # Store transcript segments
    for segment in segments:
        embedding = generate_embedding(segment["text"])

        segment_row = TranscriptSegment(
            text=segment["text"],
            start_time=segment["start"],
            end_time=segment["end"],
            embedding=embedding,
            document_id=document.id,
        )
        db.add(segment_row)
    
    # store window embeddings
    for index, window in enumerate(windows):
        embedding = generate_embedding(window["text"])

        chunk_row = Chunk(
            text=window["text"],
            chunk_index=index,
            document_id=document.id,
            embedding=embedding)
        db.add(chunk_row)

    db.commit()

    return {
        "message": "Media uploaded and transcribed",
        "document_id": document.id,
        "segments_created": len(segments),
    }