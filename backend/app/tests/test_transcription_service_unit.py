from unittest.mock import patch, Mock
from app.services.transcription_service import transcribe_media

@patch("app.services.transcription_service.model")
def test_transcribe_media(mock_model):
    # Mock one transcription segment
    mock_segment = Mock()
    mock_segment.text = "Hello world"
    mock_segment.start = 0.0
    mock_segment.end = 2.5

    # Mock model.transcribe() return value
    mock_model.transcribe.return_value = (
        [mock_segment],  # segments
        None, 
    )
    
    result = transcribe_media("test.mp3")

    # Verify output
    assert result == [
        {
            "text": "Hello world",
            "start": 0.0,
            "end": 2.5,
        }
    ]