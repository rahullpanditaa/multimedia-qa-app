"""
This service performs semantic retrieval.

Flow:
1. embed user query
2. compare against stored chunk embeddings
3. return most semantically similar chunks
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import generate_embedding


def retrieve_similar_chunks(query: str, db: Session, 
                            limit: int = 5):
    """
    Retrieve chunks semantically similar to user query.
    """

    # Generate embedding for user query
    query_embedding = generate_embedding(query)

    # pgvector cosine similarity search
    # <=> -> cosine distance operator
    # Smaller distance = more similar
    sql = text(
        '''
        SELECT *
        FROM chunks
        ORDER BY embedding <=> :embedding
        LIMIT :limit
        '''
    )

    results = db.execute(
        sql,
        {
            "embedding": query_embedding,
            "limit": limit,
        },
    )

    return results.fetchall()