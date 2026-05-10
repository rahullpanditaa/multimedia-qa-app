"""
Tests for timestamp endpoint.
"""

from app.models.document import Document

from app.models.transcript_segment import TranscriptSegment

def test_timestamps_missing_document(client):
    response = client.post(
        "/timestamps/",
        json={
            "question":
                "Where is fear discussed?",

            "document_id": 999,
        }
    )

    assert response.status_code in [200, 404]

# test timestamp retrieval
def test_timestamp_retrieval(client, db_session):
    document = Document(
        filename="song.mp3",
        filepath="uploads/song.mp3",
        mime_type="audio/mpeg",
        file_type="media",
        user_id=1        
    )

    db_session.add(document)

    db_session.commit()

    db_session.refresh(document)

    # Create transcript segment
    segment = TranscriptSegment(

        text=(
            "The singer talks about fear "
            "and loneliness."
        ),

        start_time=10,

        end_time=20,

        document_id=document.id,

        # dummy embedding vector
        embedding=[0.1] * 768,
    )

    db_session.add(segment)

    db_session.commit()

    response = client.post(
        "/timestamps/",
        json={
            "question":
                "Where does the singer discuss fear?",

            "document_id":
                document.id,
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "timestamps" in data
    assert len(data["timestamps"]) > 0