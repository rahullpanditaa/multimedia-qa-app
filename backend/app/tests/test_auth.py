from fastapi.testclient import TestClient
from app.main import app

def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "password": "newpassword",
        },
    )
    assert response.status_code == 200

def test_login():
    client = TestClient(app)

    # Register
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "password": "password123",
        },
    )

    # Login
    response = client.post(
        "/auth/login",
        json={
            "username": "loginuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()