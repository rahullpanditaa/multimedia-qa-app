from unittest.mock import patch, Mock
from app.services.llm_service import generate_response

@patch("app.services.llm_service.requests.post")
def test_generate_response(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {
        "response": "Artificial intelligence is the simulation of human intelligence."
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = generate_response(
        "What is artificial intelligence?"
    )

    assert (
        result
        == "Artificial intelligence is the simulation of human intelligence."
    )