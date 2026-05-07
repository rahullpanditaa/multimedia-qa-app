"""
Tests for upload endpoints.
"""

from io import BytesIO

def test_pdf_upload(client, monkeypatch):
    def mock_extract_text(filepath):
        return "This is test PDF content."

    # oops
    monkeypatch.setattr(
        "app.api.routes.upload.extract_text_from_pdf",
        mock_extract_text,
    )

    fake_pdf = BytesIO(
        b"%PDF-1.4 fake pdf"
    )

    response = client.post(
        "/upload/pdf",

        files={
            "file": (
                "test.pdf",

                fake_pdf,

                "application/pdf",
            )
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert "chunks_created" in data

def test_media_upload(client, monkeypatch,):
    def mock_transcribe(filepath):
        return [
            {
                "text":
                    "Fear and loneliness.",

                "start": 0,

                "end": 5,
            }
        ]


    # Replace real transcription
    monkeypatch.setattr(
        "app.api.routes.media.transcribe_media",
        mock_transcribe,
    )

    fake_audio = BytesIO(
        b"fake audio content"
    )

    response = client.post(
        "/media/upload",
        files={
            "file": (
                "song.mp3",

                fake_audio,

                "audio/mpeg",
            )
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data