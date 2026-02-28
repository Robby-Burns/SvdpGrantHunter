# 🏭 Agnostic Factories - Swap Components Without Rewriting Code

**Version:** 1.3.0 | **Updated:** February 19, 2026 | **Part:** 9/9  
**Status:** Production Ready ✅  
**Purpose:** Build adaptable systems that swap databases, LLMs, and Orchestrators via config.

---

## 📍 Purpose

This is the final framework file. It ensures your agents never depend directly on a specific library.
- Swap PostgreSQL ↔ Qdrant Vector DB
- Swap Claude ↔ OpenAI
- Swap Simple Routing ↔ LangGraph ↔ CrewAI
- **No code rewrites. Pure configuration.**

**Core Pattern:** "One interface, many implementations. Pick at runtime."

---

## 🗺️ Quick Navigation

- [The Database Factory](#-the-database-factory)
- [The LLM Factory](#-the-llm-factory)
- [The Orchestrator Factory](#-the-orchestrator-factory-swap-routing-engines)
- [Best Practices](#-best-practices)

---

## 🏗️ The Database Factory

Ensure your agent logic calls a generic interface, not a specific database driver.

```python
import os

def get_database_adapter() -> DatabaseAdapter:
    """Creates the database connection based on environment settings."""
    db_type = os.getenv("DATABASE_TYPE", "postgresql").lower()
    
    if db_type == "qdrant":
        return QdrantAdapter() # Vector DB for RAG
    
    return PostgresAdapter()   # Relational DB for state
```

---

## 🤖 The LLM Factory

This allows you to switch providers (Anthropic, OpenAI, Google) by changing a single line in `scale.yaml`.

```python
def get_llm_provider(model_type: str = "primary") -> LLMProvider:
    """Fetches the provider configured in scale.yaml."""
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    
    if provider == "openai":
        return OpenAILLM()
    elif provider == "google":
        return GoogleGeminiLLM()
        
    return ClaudeLLM()
```

---

## 🎼 The Orchestrator Factory (Swap Routing Engines)

Multi-agent orchestration frameworks change constantly. This factory isolates your business logic from the specific library used to route tasks.

### Interface
```python
# app/interfaces/orchestrator.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class AgentOrchestrator(ABC):
    """Abstract interface for multi-agent routing and state management."""
    @abstractmethod
    async def run_workflow(self, initial_state: Dict, agents: List[Any]) -> Dict:
        pass
```

### Factory Implementation
```python
# app/factory.py
import os

def get_orchestrator() -> AgentOrchestrator:
    """Creates the router based on scale.yaml/env settings."""
    engine = os.getenv("ORCHESTRATION_ENGINE", "antigravity").lower() # Default to antigravity
    
    if engine == "antigravity":
        from app.adapters.antigravity_orchestrator import AntigravityOrchestrator
        return AntigravityOrchestrator()
    elif engine == "langgraph":
        from app.adapters.langgraph_orchestrator import LangGraphOrchestrator
        return LangGraphOrchestrator()
    elif engine == "crewai":
        from app.adapters.crew_orchestrator import CrewOrchestrator
        return CrewOrchestrator()
    
    from app.adapters.simple_orchestrator import SimpleAsyncOrchestrator
    return SimpleAsyncOrchestrator()
```

---

## 💡 Best Practices

1. **Lazy Imports:** Import heavy libraries (like `langgraph` or `crewai`) inside the factory functions so you don't load unnecessary dependencies into memory.
2. **Standardized State:** Ensure every orchestrator adapter accepts and returns a standard `State` dictionary so your agents don't have to change.
3. **Environment Overrides:** Always provide a sensible default (like `simple_async`) so the system runs locally without complex setups.

---

## 📌 File Meta

**Version:** 1.3.0  
**Released:** February 19, 2026  
**Status:** Production Ready ✅  
**Part of:** 9-Part AI Agent Framework  

**🏁 THE FRAMEWORK IS COMPLETE.**