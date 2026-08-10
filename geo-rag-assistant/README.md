# Geospatial Research Assistant

Prototype for a multimodal RAG system that answers natural-language questions using both satellite imagery and mission/report documents.

## Project Layout

- `data/documents/`: sample PDF reports and mission documents
- `data/imagery/`: sample satellite imagery such as an EuroSAT or LEVIR-CD subset
- `src/ingestion/`: PDF extraction, chunking, and document embedding
- `src/vision/`: land-cover classification, optional change detection, and image metadata generation
- `src/rag/`: retrieval, fusion, and Claude client wrapper
- `src/app.py`: Streamlit UI entry point
- `vectorstore/`: persisted ChromaDB data
- `models/`: saved vision model weights
- `notebooks/`: exploration and training notebooks
- `tests/`: unit tests for retrieval and vision helpers

## Local Setup

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Add your Anthropic API key to `.env` as `ANTHROPIC_API_KEY=...`.
4. Place sample PDFs in `data/documents/` and imagery in `data/imagery/`.
5. Run the ingestion, vision, and app entry points once they are implemented.

## Notes

- The `vectorstore/` and `models/` directories are intentionally excluded from version control.
- The first implementation pass will focus on the document pipeline, then vision, then fusion.
