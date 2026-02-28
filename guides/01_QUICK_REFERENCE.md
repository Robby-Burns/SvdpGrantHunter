# 🎯 Quick Reference - AI Agent Development Framework

**Version:** 1.3.0 | **Updated:** February 19, 2026 | **Part:** 2/9  
**Status:** Production Ready ✅  
**Purpose:** Fast lookup for formulas, checklists, matrices, and decision trees

---

## 📍 Purpose

This file is your **reference desk** for quick answers. No long explanations, just:
- **7-step process** (memorize this)
- **Risk scoring formula** (0-17 scale)
- **Guardrails by risk level** (what to enable)
- **Architecture & Orchestration matrix** (what engine to use)
- **Easy swapping patterns** (code examples)

**When to use:** During design decisions, implementation, deployment. Pinned in your browser.

---

## 🗺️ Quick Navigation

- [The 7-Step Process](#-the-7-step-process)
- [Risk Scoring Formula](#-risk-scoring-formula-0-17-scale)
- [Auto-Enabled Guardrails](#-auto-enabled-guardrails-by-risk-level)
- [Orchestration Decision Matrix](#-orchestration-decision-matrix)
- [Architecture Decision Matrix](#-architecture-decision-matrix)

---

## 🔢 The 7-Step Process

1. **DISCOVERY** (What problem?)
2. **RISK SCORING** (0-17)
3. **GUARDRAILS** (What to enable?)
4. **ARCHITECTURE** (Monolith? Graph Orchestration? Distributed?)
5. **TOOLING** (Local vs MCP?)
6. **IMPLEMENTATION** (Build + Test + Eval)
7. **DEPLOY & MONITOR** (Terraform + OTEL)

---

## 📊 Orchestration Decision Matrix

Before jumping to distributed workers, decide how your agents collaborate in memory.

| Your Workflow Type | Recommended Orchestrator | Why in 2026? |
| :--- | :--- | :--- |
| **Linear / Simple RAG** | Simple Async / Custom Python | No overhead. Fast execution. |
| **Role-Playing Teams** | CrewAI | Best for sequential, hierarchical task delegation (e.g., Researcher -> Analyst -> Writer). |
| **Cyclic / Stateful** | LangGraph | Best for loops, reflection, explicit state checkpoints, and dynamic branching. |

---

## 🏗️ Architecture Decision Matrix

How do we scale the backend?

| Need | Architecture | Description |
| :--- | :--- | :--- |
| Fast MVP | **Modular Monolith** | Everything in one FastAPI app. Best for 80% of projects. |
| Heavy Processing | **Worker Queue** | FastAPI handles HTTP, Celery/Redis handles the heavy agent execution in the background. |
| Strict Security | **Sidecar Proxy** | Agent runs isolated. All DB/API calls go through a strict validation proxy container. |

---

## 📋 Quick Reference Cards

### Print These & Pin Them

**Card 1: Risk Scoring (Pocket Size)**
```text
RISK = Input (0-5) + Output (0-5) + Data (0-4) + Model (0-3)
0-4:   LOW      (Basic validation)
5-10:  MEDIUM   (+ Rate limiting, standard timeouts)
11-17: HIGH     (+ Human approval, strict circuit breakers)

# Never do this:
client = Anthropic(api_key="...") 
# Always do this:
llm = get_llm_provider()
orchestrator = get_orchestrator()