# DEPLOYMENT_CHECKLIST.md (DevOps Manager)

## Pre-Launch Requirements
- [ ] Environment variables validated (`OPENAI_API_KEY`, `DATABASE_URL`).
- [ ] Database migrations applied.
- [ ] Vector store indexed with latest SVdP success metrics.
- [ ] HITL logic tested for infinite loops.

## Monitoring
- Track token usage per grant request.
- Monitor Postgres latency for RAG queries.
- Alerts configured for "Blank Response" spikes (indicating RAG failures).
