"""
Shared pytest fixtures.

This file configures:
- test database
- FastAPI test client
- dependency overrides
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app

from app.db.base import Base
from app.db.session import get_db

# Test db 
TEST_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5433/qa_rag_test"
)

# SQLite engine for testing
engine = create_engine(
    TEST_DATABASE_URL
)


# Session factory
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# create test tables
Base.metadata.create_all(
    bind=engine
)



def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Replace real DB dependency
app.dependency_overrides[get_db] = (
    override_get_db
)

@pytest.fixture
def client():
    return TestClient(app)