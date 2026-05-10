from unittest.mock import patch

from app.models.document import Document
from app.models.user import User

@patch("app.api.routes.summary.generate_response")
@patch("app.api.routes.summary.redis_client")
def test_summary_generation(mock_redis, mock_generate_response, client, db_session):
    # Simulate cache miss
    mock_redis.get.return_value = None

    # Simulate LLM summary response
    mock_generate_response.return_value = "This is a test summary."

    # Get authenticated user
    user = db_session.query(User).filter(User.username == "testuser").first()

    # Create document
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

    # get summary
    response = client.post(f"/summary/{document.id}")

    assert response.status_code == 200
    assert response.json()["summary"] == "This is a test summary."