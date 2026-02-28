# 🤖 AI Assistant Integration - Tool-Agnostic Workflows

**Version:** 1.3.0 | **Updated:** February 19, 2026 | **Part:** 5/9  
**Status:** Production Ready ✅  
**Purpose:** How to configure and interact with AI coding assistants (Cursor, Windsurf, Claude Code) so they follow this framework.

---

## 📍 Purpose

AI coding assistants change constantly. This file teaches you the **principles** of guiding any AI assistant so it doesn't hallucinate architectures, forget your context, or write insecure code.

**The Golden Rule of AI Assistants:** "The AI is a junior developer with infinite typing speed but zero object permanence. You must force it to read the rules and update the project memory every single time."

---

## 🗺️ Quick Navigation

- [The Universal Rules File](#-the-universal-rules-file)
- [Context Loading Strategy](#-context-loading-strategy)
- [Enforcing the Risk Score](#-enforcing-the-risk-score)
- [Standardized Commands (Prompt Patterns)](#-standardized-commands-prompt-patterns)
- [Troubleshooting AI Hallucinations](#-troubleshooting-ai-hallucinations)

---

## 📜 The Universal Rules File (.cursorrules)

Most modern AI IDEs support a project-level rules file. Create a file named `agent.md` (or your IDE's equivalent) in the root of your project and paste this exactly:

```text
# 🤖 SYSTEM BEHAVIOR PROTOCOLS for [Project Name]

You are an expert AI Systems Architect building a production-grade AI agent system. You have finite context memory, so you MUST rely on your project memory files to avoid getting overwhelmed.

You must strictly follow this "Read -> Act -> Update" loop for every task:

1. **PHASE 1: READ (MANDATORY)** Before writing any code, you MUST silently read `.claude-context.md` and `.bugs_tracker.md`. Use this to understand where we left off, what the current architecture is, and what bugs to avoid. Do not ask for setup information that is already in these files.

2. **PHASE 2: ACT (THE RISK SCORE LOCK)**
   You are FORBIDDEN from generating agent code or architecture until you know the 0-17 Risk Score (defined in `docs/01_QUICK_REFERENCE.md`). 
   - Use the Agnostic Factory pattern (`docs/08_AGNOSTIC_FACTORIES.md`) for all external dependencies (DBs, LLMs, Orchestrators).
   - System behavior must be driven by `config/scale.yaml`, not hardcoded.
   - Always implement security guardrails appropriate to the Risk Score before writing core business logic.

3. **PHASE 3: UPDATE (MANDATORY BOOKKEEPING)**
   Immediately after making a change, fixing a bug, or making an architectural decision, YOU must update the memory files:
   - Fixed a bug? Add the root cause and solution to `.bugs_tracker.md`.
   - Built a feature or changed a file? Update the "Current State" and "Recent Changes" sections in `.claude-context.md`.
```

---

## 🧠 Context Loading Strategy

Because AI context windows are finite, do not dump all 9 framework files into every prompt. 

**The Optimal Context Loading Sequence:**
1. **Always in Context:** `agent.md`, `.claude-context.md`, `.bugs_tracker.md`.
2. **On Project Start:** Have the AI read `00_START_HERE.md` and `01_QUICK_REFERENCE.md`.
3. **When doing DevOps:** `@` or reference `06_INFRASTRUCTURE_AS_CODE.md` specifically.
4. **When refactoring/swapping:** `@` or reference `08_AGNOSTIC_FACTORIES.md`.

---

## 🚫 Enforcing the Risk Score

If the AI tries to write code without knowing the risk score, it will guess the guardrails (usually getting them wrong). 

**Your workflow when starting a new agent:**
> **You:** "Let's build a new agent that reads customer emails and drafts refund approvals. The Risk Score is 13 (High). Read `01_QUICK_REFERENCE.md` to see what guardrails are required, then propose the architecture."

**If the AI starts coding immediately without guardrails, stop it:**
> **You:** "Halt. You forgot the Risk Score 13 guardrails. Implement the Circuit Breaker and Human-in-the-loop HITL brake before writing the email parsing logic."

---

## 💬 Standardized Commands (Prompt Patterns)

Instead of typing long paragraphs, use these standardized prompt patterns.

### `/new-agent`
> "I want to create a new agent named [Name]. The Risk Score is [X]. Please: 
> 1. Read `.claude-context.md`.
> 2. Define its interface using our factory pattern.
> 3. Create a mock tool adapter for testing.
> 4. Write the Pytest file with LLM-as-a-judge Eval checks.
> Do not write the implementation until we agree on the tests."

### `/swap-component`
> "We need to swap our [Database/LLM/Orchestrator] from [Current] to [New]. 
> Please read `08_AGNOSTIC_FACTORIES.md`. Write the new adapter class, add it to the factory, tell me what environment variable to update in `scale.yaml`, and update `.claude-context.md` with this architectural decision."

---

## 🔧 Troubleshooting AI Hallucinations

| Problem | AI Cause | Solution |
|---------|----------|----------|
| **AI hardcodes OpenAI API calls** | Default training bias | Point it to `08_AGNOSTIC_FACTORIES.md` and say "Use the LLM Factory." |
| **AI forgets previous decisions** | Context window pushed out | Say: "Read `.claude-context.md` to refresh your memory." |
| **AI writes monolithic code** | Lazy generation | Say: "Refactor this into the Modular Monolith structure defined in `02_COMPLETE_GUIDE.md`." |
| **AI installs random libraries** | Pip hallucination | Say: "Check `pyproject.toml` and use `uv` for dependency management." |

---

## 📌 File Meta

**Version:** 1.3.0  
**Released:** February 19, 2026  
**Status:** Production Ready ✅  
**Part of:** 9-Part AI Agent Framework  

**Next File:** [05_CLAUDE_CONTEXT_AND_BUGS.md](./05_CLAUDE_CONTEXT_AND_BUGS.md) (Memory)