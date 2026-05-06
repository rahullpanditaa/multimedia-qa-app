# Handles chunking of text
def chunk_text(text: str, chunk_size: int = 500, 
               overlap: int = 100) -> list[str]:
    """
    Splits text into overlapping chunks. Overlap helps preserve continuity.

    Example:
    chunk 1 = chars 0-500
    chunk 2 = chars 400-900    

    Args:
        text: The full extracted document text
        chunk_size: Maximum chunk size
        overlap: Shared context between chunks

    Returns:
        List of text chunks
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        # Move forward while preserving overlap
        start += chunk_size - overlap

    return chunks