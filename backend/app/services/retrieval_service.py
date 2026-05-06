"""
This service performs semantic retrieval using pgvector and SQLAlchemy ORM.

Flow:
1. embed user query
2. compare against stored chunk embeddings
3. return most semantically similar chunks
"""

# from sqlalchemy import text
from app.models.chunk import Chunk
from sqlalchemy.orm import Session

from app.services.embedding_service import generate_embedding


def retrieve_similar_chunks(query: str, document_id: int,
                            db: Session, 
                            limit: int = 5):
    """
    Retrieve chunks semantically similar to user query.
    """

    # Generate embedding for user query
    query_embedding = generate_embedding(query)

    # Vector similarity search
    results = (
        db.query(Chunk).filter(Chunk.document_id == document_id)
        .order_by(
            Chunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(limit)
        .all()
    )

    return results