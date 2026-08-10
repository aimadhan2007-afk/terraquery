"""Convert classified imagery into structured JSON facts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


DEFAULT_COLLECTION_NAME = "imagery"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"


@dataclass(frozen=True)
class ImageMetadata:
	"""Structured facts extracted from a satellite image."""

	region: str
	date: str
	class_name: str
	confidence: float

	def to_dict(self) -> dict[str, str | float]:
		return {
			"region": self.region,
			"date": self.date,
			"class": self.class_name,
			"confidence": float(self.confidence),
		}


def metadata_to_description(metadata: ImageMetadata) -> str:
	return (
		f"Region: {metadata.region}. Date: {metadata.date}. "
		f"Class: {metadata.class_name}. Confidence: {metadata.confidence:.3f}."
	)


def metadata_to_json(metadata: ImageMetadata) -> str:
	return json.dumps(metadata.to_dict(), ensure_ascii=True)


def build_image_record(
	region: str,
	date: str,
	class_name: str,
	confidence: float,
) -> dict[str, str | float]:
	return ImageMetadata(region=region, date=date, class_name=class_name, confidence=confidence).to_dict()


def embed_image_record(
	record: dict[str, str | float],
	source_id: str,
	persist_directory: str | Path = "vectorstore",
	collection_name: str = DEFAULT_COLLECTION_NAME,
	model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> None:
	"""Store the image record as a short text description in Chroma."""

	try:
		import chromadb
		from sentence_transformers import SentenceTransformer
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("chromadb and sentence-transformers are required for image metadata embedding") from exc

	metadata = ImageMetadata(
		region=str(record["region"]),
		date=str(record["date"]),
		class_name=str(record["class"]),
		confidence=float(record["confidence"]),
	)
	document = metadata_to_description(metadata)
	client = chromadb.PersistentClient(path=str(persist_directory))
	collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
	model = SentenceTransformer(model_name)
	embedding = model.encode([document], normalize_embeddings=True).tolist()

	collection.upsert(
		ids=[source_id],
		documents=[document],
		metadatas=[{"source_id": source_id, **metadata.to_dict()}],
		embeddings=embedding,
	)


def write_metadata_json(metadata: ImageMetadata, output_path: str | Path) -> str:
	output_path = Path(output_path)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(metadata_to_json(metadata), encoding="utf-8")
	return str(output_path)
