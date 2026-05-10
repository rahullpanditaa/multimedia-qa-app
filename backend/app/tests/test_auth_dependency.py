from fastapi.testclient import TestClient
from app.main import app

def test_invalid_token_returns_401():
    client = TestClient(app)
    response = client.get(
        "/documents/",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401