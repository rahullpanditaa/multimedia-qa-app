"""
Stores timestamped transcript segments.

These timestamps enable:
- topic timestamp extraction
- media playback jumping
- synchronized QA
"""

from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from pgvector.sqlalchemy import Vector

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Transcript text for this segment
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Segment start timestamp in seconds
    start_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Segment end timestamp in seconds
    end_time: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    
    # Semantic embedding for transcript segment
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=True)

    # Parent document
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    document = relationship(
        "Document",
        back_populates="transcript_segments",
    )