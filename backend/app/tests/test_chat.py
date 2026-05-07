"""
Tests for chat endpoint.
"""

from app.tests.conftest import client

def test_chat_missing_document(client):
    response = client.post(
        "/chat/",
        json={
            "question":
                "What is this?",

            "document_id": 999,
        }
    )

    # Expected failure codes
    assert response.status_code in [
        404,
        500,
    ]