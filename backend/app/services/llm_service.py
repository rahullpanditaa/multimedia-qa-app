"""
This service handles communication with the local LLM via Ollama.

Responsibilities:
- send prompts to local model
- receive generated responses

This layer abstracts the model provider.

(Can swap Ollama later for OpenAI etc without changing route logic)
"""

import requests


# Ollama chat endpoint
OLLAMA_CHAT_URL = "http://localhost:11434/api/generate"

LLM_MODEL = "llama3"


def generate_response(prompt: str) -> str:
    """
    Generate response from local LLM.

    Args:
        prompt:
            Fully constructed RAG prompt

    Returns:
        Generated response text
    """

    response = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
        },
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]