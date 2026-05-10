from fastapi.testclient import TestClient
from app.main import app


def test_documents_requires_auth():
    client = TestClient(app)
    response = client.get("/documents/")

    assert response.status_code == 401