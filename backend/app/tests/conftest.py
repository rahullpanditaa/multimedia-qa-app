"""
Shared pytest fixtures.

This file configures:
1. test database
2. FastAPI test client
3. dependency overrides
4. authenticated test client
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app

from app.db.base import Base
from app.db.session import get_db

from app.models.user import User
from app.services.auth_service import hash_password

# Test database
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/qa_rag_test"

# Engine
engine = create_engine(TEST_DATABASE_URL)

# Session factory
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create all tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db_session():
    """
    Provide a clean database session for each test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    """
    Authenticated FastAPI test client.

    Creates a test user, logs in, and attaches the JWT token
    to all subsequent requests.
    """

    # Create test user
    user = User(
        username="testuser",
        hashed_password=hash_password("testpassword")
    )

    db_session.add(user)
    db_session.commit()

    # Create client
    test_client = TestClient(app)

    # Log in
    response = test_client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]

    # Attach token to all future requests
    test_client.headers.update(
        {
            "Authorization":
                f"Bearer {token}"
        }
    )

    return test_client