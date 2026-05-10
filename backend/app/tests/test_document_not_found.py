
def test_get_document_not_found(client):
    response = client.get("/documents/999999")
    assert response.status_code == 404