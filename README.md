# SvdpGrantAgent

Automated Grant System for Saint Vincent de Paul (Pasco).

## Getting Started

1. **Environment Setup**:
   - Copy `.env.example` to `.env` and fill in your `OPENAI_API_KEY`.
   - Ensure you have a PostgreSQL database running with the `pgvector` extension.
   - Install dependencies: `pip install .`

2. **Phase 0: Knowledge Base**:
   - Place organizational documents (PDF, DOCX, TXT) in a `docs/` directory.
   - Run `python -m SvdpGrantAgent.ingestion` (from the parent directory) to populate the vector database.

3. **Phase 1: Scout MVP**:
   - Run the simulation: `python -m SvdpGrantAgent.simulate_flow` (from the parent directory).
   - The system uses `graph.py` to orchestrate the evaluation flow via LangGraph.

## Project Structure
- `schema.py`: Data models and Pydantic schemas.
- `ingestion.py`: RAG pipeline for organizational knowledge.
- `scout.py`: Web scraper factory and Scout Agent logic.
- `graph.py`: LangGraph orchestration workflow.
- `pyproject.toml`: Project dependencies and configuration.

