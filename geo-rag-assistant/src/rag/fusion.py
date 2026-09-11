"""Merge document and image retrieval results into grounded answer context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .retriever import RetrievalResult, retrieve_from_both_collections


@dataclass(frozen=True)
class GroundedContext:
	"""Retrieved evidence and the prompt used to answer from it."""

	query: str
	system_prompt: str
	context_block: str
	sources: list[RetrievalResult]


def build_system_prompt() -> str:
	return (
		"You are a geospatial research assistant. Answer only using the provided context. "
		"If the context does not support a claim, say so explicitly. "
		"Cite the source id for every factual claim using square brackets, for example [documents:foo] or [imagery:bar]. "
		"Do not invent facts, and do not use outside knowledge."
	)


def _format_context_line(result: RetrievalResult) -> str:
	return f"SOURCE {result.source_id} | COLLECTION {result.collection} | SCORE {result.score:.3f}\n{result.content.strip()}"


def build_context_block(results: Iterable[RetrievalResult]) -> str:
	lines = [_format_context_line(result) for result in results]
	return "\n\n".join(lines)


def fuse_query_context(
	query: str,
	persist_directory: str = "vectorstore",
	top_k_documents: int = 4,
	top_k_images: int = 4,
) -> GroundedContext:
	"""Fetch evidence from both collections and package it for the LLM."""

	sources = retrieve_from_both_collections(
		query,
		persist_directory=persist_directory,
		top_k_documents=top_k_documents,
		top_k_images=top_k_images,
	)
	context_block = build_context_block(sources)
	return GroundedContext(
		query=query,
		system_prompt=build_system_prompt(),
		context_block=context_block,
		sources=sources,
	)


def build_user_prompt(query: str, context_block: str) -> str:
	return f"Question: {query}\n\nContext:\n{context_block}\n\nAnswer with cited claims only."
def answer_query(
    query: str,
    persist_directory: str = "vectorstore",
    top_k_documents: int = 4,
    top_k_images: int = 4,
) -> dict:
    """Full pipeline: retrieve evidence, call the LLM, and return a grounded answer with sources."""

    from .llm_client import call_claude

    grounded = fuse_query_context(
        query,
        persist_directory=persist_directory,
        top_k_documents=top_k_documents,
        top_k_images=top_k_images,
    )

    if not grounded.sources:
        return {
            "answer": "No relevant information was found in the documents or imagery to answer this question.",
            "sources": [],
        }

    user_prompt = build_user_prompt(query, grounded.context_block)
    answer_text = call_claude(grounded.system_prompt, user_prompt)

    return {
        "answer": answer_text,
        "sources": [
            {"id": r.source_id, "collection": r.collection, "score": r.score}
            for r in grounded.sources
        ],
    }
