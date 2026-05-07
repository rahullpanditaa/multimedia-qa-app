"""
Tests for retrieval service.
"""

from app.models.chunk import Chunk
from app.models.document import Document
from app.services.retrieval_service import retrieve_similar_chunks

def test_empty_retrieval(db_session):
    chunks = retrieve_similar_chunks(
        query="What is AI?",
        document_id=999,
        db=db_session,
    )
    assert chunks == []

def test_chunk_retrieval(db_session):
    document = Document(
        filename="test.pdf",
        filepath="uploads/test.pdf",
        mime_type="application/pdf",
        file_type="pdf"        
    )

    db_session.add(document)

    db_session.commit()

    db_session.refresh(document)

    chunk = Chunk(
        text="Artificial intelligence is transforming software.",
        chunk_index=0,
        embedding= [0.1] * 768,
        document_id=document.id,
    )

    db_session.add(chunk)

    db_session.commit()

    results = retrieve_similar_chunks(
        query= "What is artificial intelligence?",
        document_id=document.id,
        db=db_session,
    )
    assert len(results) > 0