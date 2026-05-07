"""
Tests for summary endpoint.
"""

from app.models.document import Document

# test with invalid doc
def test_summary_missing_document(client):
    response = client.post(
        "/summary/999"
    )
    assert response.status_code == 404

# test with valid doc
def test_summary_valid_document(client, db_session):
    document = Document(
        filename="test.pdf",
        filepath="uploads/test.pdf",
        mime_type="application/pdf",
        file_type="pdf",
    )

    db_session.add(document)

    db_session.commit()

    db_session.refresh(document)

    # call summary endpoint
    response = client.post(
        f"/summary/{document.id}"
    )

    assert response.status_code == 200
    assert "summary" in response.json()