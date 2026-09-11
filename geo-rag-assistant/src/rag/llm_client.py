"""Gemini API client wrapper for grounded answer generation."""

from __future__ import annotations

import os

from dotenv import load_dotenv


DEFAULT_MODEL = "gemini-3.6-flash"


def load_gemini_client():
    """Create a Gemini client after reading credentials from .env."""

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing from the environment")

    try:
        from google import genai
    except ImportError as exc:  # pragma: no cover - depends on optional package
        raise ImportError("google-genai is required to call the LLM") from exc

    return genai.Client(api_key=api_key)


def call_claude(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
    temperature: float = 0.2,
) -> str:
    """Call the LLM and return the assistant text response.

    Function name kept as call_claude for compatibility with fusion.py.
    """

    client = load_gemini_client()
    response = client.models.generate_content(
        model=model,
        contents=f"{system_prompt}\n\n{user_prompt}",
        config={
            "max_output_tokens": max_tokens,
            "temperature": temperature,
        },
    )
    return response.text