"""Embed PDF chunks and persist them to Chroma.

This module is intentionally small so it can be run as a standalone document
ingestion step before the rest of the assistant is wired together.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import chromadb
from sentence_transformers import SentenceTransformer

from .pdf_loader import DocumentChunk, load_document_corpus


DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_COLLECTION_NAME = "documents"


def get_persistent_client(persist_directory: str | Path) -> chromadb.PersistentClient:
	"""Create a Chroma persistent client backed by the local vectorstore."""

	return chromadb.PersistentClient(path=str(persist_directory))


def get_document_collection(
	persist_directory: str | Path = "vectorstore",
	collection_name: str = DEFAULT_COLLECTION_NAME,
) -> chromadb.Collection:
	client = get_persistent_client(persist_directory)
	return client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})


def build_document_payload(chunk: DocumentChunk) -> tuple[str, dict[str, str | int]]:
	"""Convert a chunk into the text and metadata Chroma expects."""

	metadata = {
		"source_id": chunk.source_id,
		"pdf_path": chunk.pdf_path,
		"page_number": chunk.page_number,
		"chunk_index": chunk.chunk_index,
	}
	return chunk.text, metadata


def embed_document_chunks(
	chunks: Iterable[DocumentChunk],
	persist_directory: str | Path = "vectorstore",
	collection_name: str = DEFAULT_COLLECTION_NAME,
	model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> int:
	"""Embed chunks and store them in the local Chroma collection."""

	chunk_list = list(chunks)
	if not chunk_list:
		return 0

	model = SentenceTransformer(model_name)
	collection = get_document_collection(persist_directory=persist_directory, collection_name=collection_name)

	ids: list[str] = []
	documents: list[str] = []
	metadatas: list[dict[str, str | int]] = []

	for chunk in chunk_list:
		text, metadata = build_document_payload(chunk)
		ids.append(chunk.chunk_id)
		documents.append(text)
		metadatas.append(metadata)

	embeddings = model.encode(documents, normalize_embeddings=True).tolist()
	collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
	return len(ids)


def ingest_documents(
	documents_dir: str | Path,
	persist_directory: str | Path = "vectorstore",
	collection_name: str = DEFAULT_COLLECTION_NAME,
	model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> int:
	"""Extract, chunk, embed, and persist all PDFs in a directory."""

	chunks = load_document_corpus(documents_dir)
	return embed_document_chunks(
		chunks,
		persist_directory=persist_directory,
		collection_name=collection_name,
		model_name=model_name,
	)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Embed PDF documents into Chroma.")
	parser.add_argument("documents_dir", nargs="?", default="data/documents")
	parser.add_argument("--persist-directory", default="vectorstore")
	parser.add_argument("--collection-name", default=DEFAULT_COLLECTION_NAME)
	parser.add_argument("--model-name", default=DEFAULT_EMBEDDING_MODEL)
	args = parser.parse_args()

	count = ingest_documents(
		args.documents_dir,
		persist_directory=args.persist_directory,
		collection_name=args.collection_name,
		model_name=args.model_name,
	)
	print(f"Embedded {count} document chunks into {args.collection_name}.")
