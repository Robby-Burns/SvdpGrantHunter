# ARCHITECTURE.md (Architect)

## Design Principles
1. **Vendor Agnosticism:** Never hardcode LLM, Database, or Orchestration logic directly into agents.
2. **Deterministic Orchestration:** Use LangGraph for predictable state transitions and HITL pauses.
3. **Strict RAG Confinement:** Agents must be "blank slates" without grounding in organizational facts.

## Component Overview
- **Factories (`factories/`):** Dynamic resolution of services (LLM, PGVector, LangGraph).
- **State Schema (`GraphState`):** Centralized `TypedDict` in `schema.py` tracking grant IDs, payload, and status.
- **Orchestrator (`graph.py`):** The LangGraph definition managing the `Scout -> Review -> Writer -> Export` flow.

## Swappability Layer
The system uses `llm_factory.py` and `db_factory.py` to allow the organization to switch from GPT-4o to Claude or Gemini with zero modifications to agent logic.
