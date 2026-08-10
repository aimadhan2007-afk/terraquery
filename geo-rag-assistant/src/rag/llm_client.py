"""Claude API client wrapper for grounded answer generation."""

from __future__ import annotations

import os

from dotenv import load_dotenv


DEFAULT_MODEL = "claude-sonnet-4-6"


def load_anthropic_client():
	"""Create an Anthropic client after reading credentials from .env."""

	load_dotenv()
	api_key = os.getenv("ANTHROPIC_API_KEY")
	if not api_key:
		raise ValueError("ANTHROPIC_API_KEY is missing from the environment")

	try:
		from anthropic import Anthropic
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("anthropic is required to call Claude") from exc

	return Anthropic(api_key=api_key)


def call_claude(
	system_prompt: str,
	user_prompt: str,
	model: str = DEFAULT_MODEL,
	max_tokens: int = 1024,
	temperature: float = 0.2,
) -> str:
	"""Call Claude and return the assistant text response."""

	client = load_anthropic_client()
	response = client.messages.create(
		model=model,
		max_tokens=max_tokens,
		temperature=temperature,
		system=system_prompt,
		messages=[{"role": "user", "content": user_prompt}],
	)
	return "".join(block.text for block in response.content if hasattr(block, "text"))
