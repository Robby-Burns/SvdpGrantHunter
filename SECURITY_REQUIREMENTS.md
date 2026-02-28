# SECURITY_REQUIREMENTS.md (Infosec Lead)

## Security Posture: Level 8/17 (Moderate-High Risk)
As this system generates financial documents and handles organizational facts, it requires active guardrails.

## Critical Guardrails
1. **PII Redaction:** All ingested documents in `ingestion.py` MUST pass through the `Presidio` or regex scrubbing layer in `guardrails.py`.
2. **Sanitization:** Web scraper inputs in `scout.py` must be cleaned to prevent injection.
3. **Audit Trail:** Every factual answer in a draft MUST contain a `source_citation` back to the vector store.

## The Kill Switch
The `Infosec Lead` reserves the right to activate the emergency kill switch (hard-stop orchestrator) if anomalous drafting behavior or credential leaks are detected.
