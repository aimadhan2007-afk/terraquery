"""Streamlit entry point for the Geospatial Research Assistant prototype."""

from __future__ import annotations

import streamlit as st

from src.rag.fusion import build_user_prompt, fuse_query_context
from src.rag.llm_client import call_claude


def render_sources(sources) -> None:
	if not sources:
		st.info("No sources were retrieved for this query.")
		return

	for index, source in enumerate(sources, start=1):
		with st.expander(f"Source {index}: {source.source_id}"):
			st.caption(f"Collection: {source.collection} | Score: {source.score:.3f}")
			st.write(source.content)


def main() -> None:
	st.set_page_config(page_title="Geospatial Research Assistant", layout="wide")
	st.title("Geospatial Research Assistant")
	st.write("Ask a question grounded in both mission documents and satellite imagery.")

	query = st.text_area("Question", height=120, placeholder="What changed around the project area between the mission report and the latest imagery?")
	submitted = st.button("Answer", type="primary")

	if submitted and query.strip():
		grounded_context = fuse_query_context(query.strip())
		user_prompt = build_user_prompt(grounded_context.query, grounded_context.context_block)

		with st.spinner("Generating grounded answer..."):
			answer = call_claude(grounded_context.system_prompt, user_prompt)

		answer_col, sources_col = st.columns([2, 1])
		with answer_col:
			st.subheader("Answer")
			st.write(answer)
		with sources_col:
			st.subheader("Sources")
			render_sources(grounded_context.sources)
	elif submitted:
		st.warning("Enter a question before asking for an answer.")


if __name__ == "__main__":
	main()
