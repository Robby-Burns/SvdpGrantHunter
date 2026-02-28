# Executive One-Pager: SVdP Grant Hunter & Writer

## 🎯 Problem Solved
Grant discovery and drafting are manual, slow, and prone to volunteer burnout. This system automates the "busy work" of finding local grants (3 Rivers, Catholic Foundation) and creates 90% accurate drafts based *only* on verified SVdP facts.

## 🏗️ Architecture Choice
We use **LangGraph** (Stateful Orchestration). This ensures the AI **always stops** for a human to review the work before any document is finalized.

## 💰 Resource & Cost Ceiling
- **Monthly Infrastructure (Railway)**: ~$5 - $10 (Sleep on Idle enabled).
- **AI Variable Cost (OpenAI)**: Estimated <$0.50 per grant application.
- **Total Monthly Ceiling**: Recommended $20 budget cap on OpenAI.

## 🛑 Kill Switch & Safety
- **Kill Switch**: Set `SYSTEM_ACTIVE=false` in environment variables or simply click "Disconnect" in the Railway project dashboard.
- **Safety**: The AI is "Gagged"—it cannot answer questions about finances or mission unless it finds the specific text in our approved SVdP documents.
- **Redaction**: All incoming documents have Names, Phones, and Emails auto-redacted before the AI sees them.

---
**Status:** PRODUCTION READY (St. Pats Conference)
