"""PDF ingestion entry points for extracting and chunking document text.

This module keeps the document pipeline self-contained so it can be tested
without the rest of the RAG stack.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

import fitz

import re


def clean_text(text: str) -> str:
    # Strip non-ASCII characters (removes garbled Devanagari artifacts)
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

DEFAULT_CHUNK_TOKENS = 400
DEFAULT_OVERLAP_RATIO = 0.15


@dataclass(frozen=True)
class DocumentChunk:
	"""A citation-friendly chunk extracted from a PDF page."""

	chunk_id: str
	source_id: str
	pdf_path: str
	page_number: int
	chunk_index: int
	text: str


def _tokenize(text: str) -> list[str]:
	return re.findall(r"\S+", text)


def _detokenize(tokens: Iterable[str]) -> str:
	return " ".join(tokens).strip()


def chunk_text(
	text: str,
	chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
	overlap_ratio: float = DEFAULT_OVERLAP_RATIO,
) -> list[str]:
	"""Split text into overlapping token windows.

	The implementation uses whitespace tokenization as a lightweight stand-in
	for model tokenization, which keeps the pipeline dependency-light while
	still matching the requested chunk sizing behavior closely.
	"""

	if chunk_tokens <= 0:
		raise ValueError("chunk_tokens must be positive")
	if not 0 <= overlap_ratio < 1:
		raise ValueError("overlap_ratio must be between 0 and 1")

	tokens = _tokenize(text)
	if not tokens:
		return []

	overlap_tokens = max(1, int(chunk_tokens * overlap_ratio))
	step = max(1, chunk_tokens - overlap_tokens)

	chunks: list[str] = []
	for start in range(0, len(tokens), step):
		end = start + chunk_tokens
		chunk = _detokenize(tokens[start:end])
		if chunk:
			chunks.append(chunk)
		if end >= len(tokens):
			break
	return chunks


def extract_text_from_pdf(pdf_path: str | Path) -> Iterator[tuple[int, str]]:
	"""Yield page number and extracted text for a PDF."""

	document = fitz.open(str(pdf_path))
	try:
		for page_index in range(document.page_count):
			page = document.load_page(page_index)
			yield page_index + 1, page.get_text("text")
	finally:
		document.close()


def load_pdf_chunks(
	pdf_path: str | Path,
	chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
	overlap_ratio: float = DEFAULT_OVERLAP_RATIO,
) -> list[DocumentChunk]:
	"""Load one PDF and return chunk objects with stable citation metadata."""

	pdf_path = Path(pdf_path)
	chunks: list[DocumentChunk] = []

	for page_number, page_text in extract_text_from_pdf(pdf_path):
		page_chunks = chunk_text(page_text, chunk_tokens=chunk_tokens, overlap_ratio=overlap_ratio)
		for chunk_index, chunk_text_value in enumerate(page_chunks):
			source_id = f"{pdf_path.stem}:p{page_number}:c{chunk_index}"
			chunks.append(
				DocumentChunk(
					chunk_id=source_id,
					source_id=source_id,
					pdf_path=str(pdf_path),
					page_number=page_number,
					chunk_index=chunk_index,
					text=chunk_text_value,
				)
			)

	return chunks


def load_document_corpus(
	documents_dir: str | Path,
	chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
	overlap_ratio: float = DEFAULT_OVERLAP_RATIO,
) -> list[DocumentChunk]:
	"""Load and chunk every PDF under a documents directory."""

	documents_dir = Path(documents_dir)
	chunks: list[DocumentChunk] = []
	for pdf_path in sorted(documents_dir.glob("**/*.pdf")):
		chunks.extend(load_pdf_chunks(pdf_path, chunk_tokens=chunk_tokens, overlap_ratio=overlap_ratio))
	return chunks
