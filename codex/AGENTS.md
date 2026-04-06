# CLAUDE.md

Guidelines to reduce common LLM coding mistakes. For trivial tasks, use judgment.

## Approach

- Think before acting. Read existing files before writing code.
- Be concise in output but thorough in reasoning.
- Prefer editing over rewriting whole files.
- Do not re-read files you have already read unless the file may have changed.
- Test your code before declaring done.
- No sycophantic openers or closing fluff.
- Keep solutions simple and direct. No over-engineering.
- If unsure: say so. Never guess or invent file paths.
- User instructions always override this file.

## 1. Think First, Then Search, Then Code

**Don't assume. Don't write code blind. Surface tradeoffs.**

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- Search the codebase for existing implementations, patterns, and conventions before writing anything.
- Read sufficient context to understand how relevant modules work.
- Identify reusable components before creating new ones.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity and Surgical Changes

**Minimum code that solves the problem. Touch only what you must.**

Writing new code:
- No features beyond what was asked.
- No abstractions for single-use code.
- No speculative "flexibility" or error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.
- Follow OOP and SOLID principles. Keep code clean and runnable.

Editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken. Match existing style.
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked — mention it instead.

The test: every changed line should trace directly to the user's request.

## 3. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

## 4. Autonomous Agent & Skill Dispatch

Specialized agents and skills live in `~/.claude/agents/` and `~/.claude/skills/`. Proactively dispatch them — don't wait to be asked.

- **After writing or modifying code** → dispatch a code review agent.
- **For API or database design** → dispatch an architecture agent.
- **Independent subtasks** → dispatch multiple agents in parallel.
- **Complex tasks** → Analyze → Plan → Execute → Review.

## 5. Efficiency

- Read before writing. Understand the problem before coding.
- No redundant file reads. Read each file once.
- One focused coding pass. Avoid write-delete-rewrite cycles.
- Test once, fix if needed, verify once. No unnecessary iterations.
- Budget: 50 tool calls maximum. Work efficiently.

## 6. Python Environment

All Python work must use the project's `.venv` virtual environment.

```bash
source .venv/bin/activate        # activate before any Python command
pip install -r requirements.txt  # install inside venv, never globally
```

If `.venv` does not exist, request it to the user.

---
** MUST NOT ACCESS `.env` ** 
**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
