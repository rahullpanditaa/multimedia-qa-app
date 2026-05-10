
def test_stream_chat_missing_document(client):
    response = client.post(
        "/chat/stream",
        json={
            "question": "What is this?",
            "document_id": 999,
        },
    )

    assert response.status_code == 404