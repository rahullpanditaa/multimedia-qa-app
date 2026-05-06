from app.db.base import Base
from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Table for uploaded docs
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # original uploaded filename
    filename: Mapped[str] = mapped_column(String, nullable=False)

    # actual saved location on disk
    filepath: Mapped[str] = mapped_column(String, nullable=False)

    # MIME type of uploaded file
    # eg - application/pdf
    mime_type: Mapped[str] = mapped_column(String, nullable=False)

    # Type of uploaded file, eg pdf, audio, video
    file_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="pdf"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # Relationship - one doc can have many chunks
    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )