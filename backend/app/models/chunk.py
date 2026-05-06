from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


# Model for storing individual chunks of extracted document text
# Docs -> chunks -> vectors
class Chunk(Base):
    __tablename__ = "chunks"

    # primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # actual chunk text
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # position/order of the chunk inside the document
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

    # foreign key chunk -> parent document
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE")
    )

    # relationship back to the document model
    document = relationship("Document", back_populates="chunks")