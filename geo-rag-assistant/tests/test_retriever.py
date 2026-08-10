"""Retriever tests for the geospatial RAG prototype."""

from src.ingestion.pdf_loader import chunk_text


def test_chunk_text_uses_overlap_and_preserves_order():
	text = " ".join(f"token{i}" for i in range(1, 701))

	chunks = chunk_text(text, chunk_tokens=400, overlap_ratio=0.15)

	assert len(chunks) == 2
	assert chunks[0].startswith("token1 token2")
	assert chunks[1].startswith("token341 token342")
