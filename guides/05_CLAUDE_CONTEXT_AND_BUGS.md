# 🧠 Claude Context & Bug Tracking - AI Project Memory

**Version:** 1.3.0 | **Updated:** February 19, 2026 | **Part:** 6/9  
**Status:** Production Ready ✅  
**Purpose:** Give AI Coding Assistants project memory to prevent repeated bugs and architecture drift.

---

## 📍 Purpose

AI Coding Assistants (Cursor, Claude Code) have **zero memory between sessions**. 

To solve this, we use two files that the **AI is responsible for reading and updating**:
1. **`.claude-context.md`** — Project state, recent changes, architecture
2. **`.bugs_tracker.md`** — Active bugs, patterns, root causes

**Core Rule:** The AI must manage its own memory through a strict "Read -> Act -> Update" loop (enforced via `.cursorrules` in File `04`).

---

## 🗺️ Quick Navigation

- [The AI-First Bookkeeping Workflow](#-the-ai-first-bookkeeping-workflow)
- [File 1: .claude-context.md Template](#-file-1-claude-contextmd)
- [File 2: .bugs_tracker.md Template](#-file-2-bugs_trackermd)
- [Troubleshooting Memory Loss](#-troubleshooting)

---

## 🤖 The AI-First Bookkeeping Workflow

You do not need to manually update these files. You enforce that the AI does it.

### Step 1: Session Start (READ)
The AI reads `.claude-context.md` automatically via `.cursorrules`. 
**You say:** "Let's continue building the Research Agent."

### Step 2: Coding (ACT)
The AI writes the code, adds the factory patterns, and runs tests.

### Step 3: Session End (UPDATE)
**You say:** "Great, that works. Update `.claude-context.md` with what we built today and any new architectural decisions. If we hit any bugs, log them in `.bugs_tracker.md`."

---

## 📄 File 1: `.claude-context.md`

### Template (Create this in your root folder)

```markdown
# AI Context Memory - [PROJECT NAME]

**Last Updated:** [DATE/TIME]  
**Project Phase:** [Discovery/Build/Test/Deploy/Maintain]  
**Risk Score:** [0-17]  

---

## 📍 Current State

### What I'm Working On Right Now
- **Feature:** [Current feature name]
- **Status:** [Started/In Progress/Testing/Blocked]
- **Blocker:** [What's blocking progress]

### Recent Changes (AI-UPDATED)
- **[DATE]:** Built [feature/component]
  - Files modified: `app/agents/researcher.py`
  - Architectural Decision: Decided to use LangGraph for orchestration.

---

## 🏗️ Project Structure
[Provide a brief tree of your /app, /infra, and /tests folders here]

---

## ⚙️ Configuration & Factories
- **LLM Engine:** [e.g., Anthropic via scale.yaml]
- **Orchestration:** [e.g., LangGraph]
- **Database:** [e.g., PostgreSQL]
- **Environment:** Hybrid MCP + Local

---

## 🛠️ Important Architectural Decisions
*(AI: Never delete these entries. Add to them when making technical choices)*

**Decision:** Use hybrid tooling  
**Why:** DB queries need speed (local); file access needs safety (MCP)

**Decision:** Agent Orchestration  
**Why:** Decided to use LangGraph to manage cyclic agent routing instead of linear scripts.
```

---

## 📄 File 2: `.bugs_tracker.md`

### Template (Create this in your root folder)

```markdown
# Bug Tracker & Pattern Memory

**Last Updated:** [DATE]  
**Active Bugs:** [COUNT]  

---

## 🚨 Active Bugs
### BUGS-001: MCP Connection Timeout
**Status:** Active | **Severity:** Major  
**Description:** Agent fails to connect to `mcp-filesystem` on initial startup.
**Fix Attempts:** Tried sleep(5). Didn't work reliably. Next step: Add Tenacity retry backoff.

---

## 🔍 Bug Patterns Identified (AI-UPDATED)
*(AI: Read this before writing new integration code to avoid repeating mistakes)*

### Pattern 1: Sidecar Race Conditions
**Occurrences:** 2 times (MCP filesystem + Database)  
**Root cause:** Containers starting before services are ready  
**Solution:** Always use exponential backoff decorators on connection logic.
```

---

## 📌 File Meta

**Version:** 1.3.0  
**Released:** February 19, 2026  
**Status:** Production Ready ✅  
**Part of:** 9-Part AI Agent Framework  

**Next File:** [06_INFRASTRUCTURE_AS_CODE.md](./06_INFRASTRUCTURE_AS_CODE.md) (Deployment)