import fitz

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extracts all text from a PDF.

    Args:
        filepath: Path to uploaded PDF

    Returns:
        Full extracted text
    """

    # Open the PDF document
    document = fitz.open(filepath)

    full_text = ""

    # Iterate through every page in the PDF
    for page in document:

        # Extract text from current page
        page_text = page.get_text()

        # Append extracted page text
        full_text += page_text

    document.close()
    return full_text.strip()