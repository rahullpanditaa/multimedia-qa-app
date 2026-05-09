"""
This service generates embeddings using Ollama.

Embeddings convert text into vectors that capture semantic meaning.
These vectors enable semantic similarity search.

Text embedding model used- nomic-embed-text
"""

import requests
import os


# Ollama embeddings endpoint
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    """
    Generate embedding vector using Ollama.

    Args:
        text: Input text

    Returns:
        Vector embedding
    """

    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text,
        },
    )

    response.raise_for_status()
    data = response.json()

    return data["embedding"]