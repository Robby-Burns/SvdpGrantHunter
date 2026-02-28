# DATABASE_SCHEMA.md (Database Manager)

## Core State: GraphState
Defined in `schema.py`.
- `grant_id`: UUID/String
- `grant_source_url`: Source location
- `extracted_requirements`: List of strings
- `draft_payload`: JSON Q&A pairs
- `status`: Enum (Scouted, Drafting, Pending_Review, Approved, Rejected)

## Storage Layers
1. **Postgres/PGVector:** Stores verified organizational facts (embeddings) and the grant queue.
2. **S3/Blob Storage:** Stores the final generated PDFs/exports.

## Encryption
All database connections must use TLS/SSL. Sensitive API keys are stored as Environment Variables, never in code.
