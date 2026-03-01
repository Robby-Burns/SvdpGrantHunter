# BUGS.md

## Active Issues

| ID | Status | Severity | Description | Owner |
|----|--------|----------|-------------|-------|
| B-001 | OPEN | Low | Scraper logic for Catholic Foundation needs tighter DOM selectors | AI Engineer |
| B-002 | OPEN | Medium | PII Redaction sometimes over-redacts standard non-sensitive years (e.g., 2024) | Infosec |
| B-010 | OPEN | Medium | `run_scout_job()` blocks Streamlit thread, risking Gateway Timeline errors on large scans | AI Engineer |
| B-011 | OPEN | Low | `initialize_db.py` crashes completely if no ENV var is present instead of waiting | DevOps |

## Resolved Issues

| ID | Status | Severity | Description | Owner |
|----|--------|----------|-------------|-------|
| B-004 | RESOLVED | High | `ModuleNotFoundError` on Railway due to missing `__init__.py` files in package structure | AI Engineer |
| B-005 | RESOLVED | High | `TypeError: MarkdownMixin.markdown()` in Streamlit due to `unsafe_allow_value` typo | QA Engineer |
| B-006 | RESOLVED | Medium | `psycopg2.OperationalError` causing app crash locally without DB credentials | QA Engineer |
| B-007 | RESOLVED | Medium | `NameResolutionError` causing app crash when scraper hits offline foundation sites | QA Engineer |
| B-003 | RESOLVED | Medium | `ModuleNotFoundError` due to case sensitivity mismatch in `pyproject.toml` | AI Engineer |
| B-008 | RESOLVED | High | `app.py` crashes if OpenAI keys are invalid during LangGraph initialization | AI Engineer |
| B-009 | RESOLVED | High | PDFs generated in `exporter.py` vanish upon Railway restart due to ephemeral filesystem | DevOps |
