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

    # Store transcript segments
    for segment in segments:
        segment_row = TranscriptSegment(
            text=segment["text"],
            start_time=segment["start"],
            end_time=segment["end"],
            document_id=document.id,
        )

        db.add(segment_row)

    db.commit()

    return {
        "message": "Media uploaded and transcribed",
        "document_id": document.id,
        "segments_created": len(segments),
    }