
Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First
   
**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.


## 5. Python Environment

All Python work must use the project's `.venv` virtual environment.

```bash
source .venv/bin/activate        # activate before any Python command
pip install -r requirements.txt  # install inside venv, never globally
```

If `.venv` does not exist, request it to the user.

## 6. Readability First

**Readable code is code whose intent is obvious with minimal effort.**

When writing or editing code:

* Prefer clear names over clever names.
* Prefer straightforward control flow over compact tricks.
* Reduce unnecessary nesting, branching, and indirection.
* Keep functions focused and reasonably small.
* Use comments to explain why something exists, not what the code already says.
* Match the existing project style, even if you would normally write it differently.

Do not make readability changes outside the requested scope. If nearby code is hard to read but unrelated, mention it instead of changing it.

## 7. Clean Code, Practically Applied

**Clean code should reduce complexity, not introduce new abstractions.**

Apply Clean Code principles when they directly improve the requested change:

* Use intention-revealing names.
* Keep responsibilities separated.
* Remove duplication introduced by your changes.
* Prefer simple, explicit code over overly generic code.
* Avoid hidden side effects.
* Avoid premature abstraction.

Do not create helpers, classes, interfaces, configuration layers, or frameworks unless they are clearly needed by the current task.

A small amount of duplication is acceptable when abstraction would make the code harder to understand.

## 8. SOLID With Restraint

**SOLID principles are design tools, not mandatory ceremony.**

Use SOLID principles when working in an existing object-oriented design or when the requested change affects module boundaries.

Guidelines:

* Single Responsibility: keep each function, class, or module focused on one clear reason to change.
* Open/Closed: avoid modifying stable behavior unnecessarily, but do not add speculative extension points.
* Liskov Substitution: preserve expected behavior when changing inheritance or polymorphic code.
* Interface Segregation: avoid forcing callers to depend on methods they do not use.
* Dependency Inversion: depend on abstractions only when there is a real need for substitution, testing, or decoupling.

Do not introduce interfaces, base classes, dependency injection, or design patterns solely because SOLID exists. For simple code, the most SOLID solution is often the simplest direct implementation.


---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---
** MUST NOT ACCESS `.env` **


<!-- context7 -->
Use Context7 MCP to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service -- even well-known ones like React, Next.js, Prisma, Express, Tailwind, Django, or Spring Boot. This includes API syntax, configuration, version migration, library-specific debugging, setup instructions, and CLI tool usage. Use even when you think you know the answer -- your training data may not reflect recent changes. Prefer this over web search for library docs.

Do not use for: refactoring, writing scripts from scratch, debugging business logic, code review, or general programming concepts.

## Steps

1. Always start with `resolve-library-id` using the library name and the user's question, unless the user provides an exact library ID in `/org/project` format
2. Pick the best match (ID format: `/org/project`) by: exact name match, description relevance, code snippet count, source reputation (High/Medium preferred), and benchmark score (higher is better). If results don't look right, try alternate names or queries (e.g., "next.js" not "nextjs", or rephrase the question). Use version-specific IDs when the user mentions a version
3. `query-docs` with the selected library ID and the user's full question (not single words)
4. Answer using the fetched docs
<!-- context7 -->