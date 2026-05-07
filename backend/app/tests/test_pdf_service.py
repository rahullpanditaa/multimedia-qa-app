"""
Tests for PDF extraction service.
"""

from unittest.mock import MagicMock

from app.services.pdf_service import extract_text_from_pdf

def test_extract_text_from_pdf(monkeypatch):
    mock_page = MagicMock()

    mock_page.get_text.return_value = "This is page text."

    # mock doc
    mock_document = MagicMock()
    mock_document.__iter__.return_value = [mock_page, mock_page]

    monkeypatch.setattr(
        "fitz.open",
        lambda filepath:
            mock_document,
    )
    text = extract_text_from_pdf("fake.pdf")
    assert "This is page text." in text