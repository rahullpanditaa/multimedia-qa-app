"""
Timestamp retrieval endpoint.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.timestamp_service import retrieve_relevant_timestamps

from app.services.auth_dependency import get_current_user

# API router for /timestamps path operations
router = APIRouter(prefix="/timestamps", tags=["timestamps"])

class TimestampRequest(BaseModel):
    question: str
    document_id: int


@router.post("/")
def get_timestamps(payload: TimestampRequest,
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_user)):

    results = retrieve_relevant_timestamps(
        query=payload.question,
        document_id=payload.document_id,
        db=db
    )

    return {
        "question": payload.question,

        "timestamps": [
            {
                "text": segment.text,

                "start_time": segment.start_time,
                "end_time": segment.end_time,
            }
            for segment in results
        ]
    }