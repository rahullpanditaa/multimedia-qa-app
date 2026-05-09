"""
This service handles communication with the local LLM via Ollama.

Responsibilities:
- send prompts to local model
- receive generated responses

This layer abstracts the model provider.

(Can swap Ollama later for OpenAI etc without changing route logic)
"""

import requests

from app.core.config import settings

def generate_response(prompt: str) -> str:
    """
    Send prompt to Ollama and return the generated response.
    """

    response = requests.post(
        f"{settings.ollama_url}/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False,
        },
    )

    response.raise_for_status()
    data = response.json()
    return data["response"]