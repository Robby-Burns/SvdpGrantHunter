# Agent Cards: SVdP Grant Hunter & Writer

## 🕵️ The Scout Agent (Discovery)
- **Role**: Periodically scrapes foundation websites for new grant opportunities.
- **Model**: `gpt-4-turbo-preview` (Logic-heavy parsing).
- **Tools**: `GenericScraper`, `ScraperFactory`.
- **Guardrails**: `Guardrails.sanitize_html` (Injection protection).

## ✍️ The Writer Agent (Drafting)
- **Role**: Drafts application sections using organizational facts.
- **Model**: `gpt-4-turbo-preview`.
- **Tools**: `get_vector_store`, `query_svdp_facts`.
- **Guardrails**: **Strict RAG Confinement**. Forbidden from using training data for SVdP specifics.

## ⚖️ The HITL Node (Review)
- **Role**: Execution pause for human verification and iterative feedback.
- **Interface**: Streamlit "Grandmother UI".
- **Capabilities**: Approve, Manual Edit, Request AI Rewrite.

## 📄 The Form Filler (Export)
- **Role**: Converts JSON approval payloads into branded PDFs.
- **Tools**: `DocumentExportFactory`, `fpdf2`.
- **Guardrails**: **Citation Mandate**. Footer contains audit trail of source documents.
