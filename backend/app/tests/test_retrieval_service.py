"""
Tests for retrieval service.
"""

from app.models.chunk import Chunk
from app.models.document import Document
from app.services.retrieval_service import retrieve_similar_chunks

from app.models.user import User
from app.services.auth_service import hash_password

def test_empty_retrieval(db_session):
    chunks = retrieve_similar_chunks(
        query="What is AI?",
        document_id=999,
        db=db_session,
    )
    assert chunks == []

def test_chunk_retrieval(db_session):
    # Create a user first
    user = User(
        username="testuser",
        hashed_password=hash_password("testpassword"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create document owned by that user
    document = Document(
        filename="test.pdf",
        filepath="uploads/test.pdf",
        mime_type="application/pdf",
        file_type="pdf",
        user_id=user.id,
    )

    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    # Create chunk
    chunk = Chunk(
        text="Artificial intelligence is transforming software.",
        chunk_index=0,
        embedding=[0.1] * 768,
        document_id=document.id,
    )

    db_session.add(chunk)
    db_session.commit()

    # Retrieve chunks
    results = retrieve_similar_chunks(
        query="What is artificial intelligence?",
        document_id=document.id,
        db=db_session,
    )

    assert len(results) > 0