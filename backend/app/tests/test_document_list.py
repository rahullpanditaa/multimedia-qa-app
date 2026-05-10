from app.models.document import Document
from app.models.user import User


def test_get_documents_returns_created_document(client, db_session):
    # Get auth user created by fixture
    user = db_session.query(User).filter(User.username == "testuser").first()

    # Create a document for that user
    document = Document(
        filename="example.pdf",
        filepath="uploads/example.pdf",
        mime_type="application/pdf",
        file_type="pdf",
        user_id=user.id,
    )

    db_session.add(document)
    db_session.commit()

    # Call existing endpoint
    response = client.get("/documents/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["filename"] == "example.pdf"