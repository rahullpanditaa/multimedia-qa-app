"""
This service handles timestamp-aware semantic retrieval.
It finds transcript moments relevant to a query.
"""

from sqlalchemy.orm import Session

from app.models.transcript_segment import TranscriptSegment

from app.services.embedding_service import generate_embedding

def retrieve_relevant_timestamps(query: str, document_id: int, 
                                 db: Session, limit: int = 3):
    """
    Retrieve relevant transcript timestamps.
    """

    query_embedding = generate_embedding(query)

    # Semantic search
    results = (
        db.query(TranscriptSegment)

        # Restrict to selected media document
        .filter(
            TranscriptSegment.document_id
            == document_id
        )

        # Semantic similarity ordering
        .order_by(
            TranscriptSegment.embedding
            .cosine_distance(query_embedding)
        )

        .limit(limit)

        .all()
    )

    return results