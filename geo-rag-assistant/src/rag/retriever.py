"""Top-k retrieval helpers for document and imagery collections."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"


@dataclass(frozen=True)
class RetrievalResult:
	"""A citation-friendly retrieval hit."""

	source_id: str
	collection: str
	content: str
	score: float
	metadata: dict[str, Any]


def _get_client(persist_directory: str | Path) -> chromadb.PersistentClient:
	return chromadb.PersistentClient(path=str(persist_directory))


def _encode_query(query: str, model_name: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
	model = SentenceTransformer(model_name)
	return model.encode([query], normalize_embeddings=True).tolist()[0]


def retrieve_top_k(
	query: str,
	collection_name: str,
	persist_directory: str | Path = "vectorstore",
	top_k: int = 4,
	model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> list[RetrievalResult]:
	"""Retrieve the nearest neighbors for a query from one Chroma collection."""

	client = _get_client(persist_directory)
	try:
		collection = client.get_collection(name=collection_name)
	except Exception:
		return []

	query_embedding = _encode_query(query, model_name=model_name)
	response = collection.query(
		query_embeddings=[query_embedding],
		n_results=top_k,
		include=["documents", "metadatas", "distances"],
	)

	results: list[RetrievalResult] = []
	ids = response.get("ids", [[]])[0]
	documents = response.get("documents", [[]])[0]
	metadatas = response.get("metadatas", [[]])[0]
	distances = response.get("distances", [[]])[0]

	for source_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
		score = 1.0 - float(distance) if distance is not None else 0.0
		results.append(
			RetrievalResult(
				source_id=source_id,
				collection=collection_name,
				content=document or "",
				score=score,
				metadata=metadata or {},
			)
		)

	return results


def retrieve_from_both_collections(
	query: str,
	persist_directory: str | Path = "vectorstore",
	top_k_documents: int = 4,
	top_k_images: int = 4,
) -> list[RetrievalResult]:
	"""Retrieve results from both document and imagery collections."""

	results = []
	results.extend(
		retrieve_top_k(
			query,
			collection_name="documents",
			persist_directory=persist_directory,
			top_k=top_k_documents,
		)
	)
	results.extend(
		retrieve_top_k(
			query,
			collection_name="imagery",
			persist_directory=persist_directory,
			top_k=top_k_images,
		)
	)
	return results


def format_source_label(result: RetrievalResult) -> str:
	return f"[{result.collection}] {result.source_id}"
