"""
Tests for document endpoints.
"""

from app.tests.conftest import client

# test GET docs
def test_get_documents(client):
    response = client.get(
        "/documents/"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )