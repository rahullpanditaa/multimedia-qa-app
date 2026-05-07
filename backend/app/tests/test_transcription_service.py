"""
Tests for transcription service.
"""

from app.services.transcription_service import (
    transcribe_media,
)

def test_transcribe_media(monkeypatch):
    def mock_transcription(filepath):
        return [
            {
                "text":
                    "Fear and loneliness.",
                "start": 0,
                "end": 5,
            }
        ]


    # Replace real function
    monkeypatch.setattr(
        "app.tests.test_transcription_service.transcribe_media",
        mock_transcription,
    )

    result = transcribe_media("fake.mp3")

    assert len(result) == 1
    assert result[0]["text"] == "Fear and loneliness."