---
name: implementation
description: >
  Implements new functions, APIs, or tools following a strict TDD workflow with full spec documentation.
  Use this skill PROACTIVELY whenever the user asks to implement, build, create, or add a new function,
  API endpoint, tool, or feature — including phrases like "implement this", "build this", "create a function",
  "add this feature", "make this work", or any request that requires writing new production code with tests.
  Do NOT use for bug fixes, refactoring, or code review — only for new implementations.
---

# Implementation Skill

This skill guides the full implementation lifecycle: from writing a spec document, through TDD (test-first development), to final code explanation. Every implementation produces three deliverables:

1. `<tool_name>.spec.md` — API specification
2. `tests/test_<tool_name>.py` — Tests (written FIRST)
3. `<tool_name>.py` — Implementation (written to pass the tests)

The reason for this strict ordering is that writing tests first forces you to think about the interface and edge cases before getting lost in implementation details. The spec document ensures the function is well-defined enough that anyone (human or AI) can understand when and how to call it.

---

## Workflow

### Phase 1: Spec Document

Before writing any code, create `<tool_name>.spec.md` with:

- **Function name** and one-line description
- **Usage scenario** — when and why this function is called
- **Input parameters** — type, required/optional, example values, validation rules (range/length/enum)
- **Output schema** — success and failure cases, error code/message conventions
- **Constraints/guardrails** — max processing time, max data size, rate limits
- **Sample request/response** — at least one complete example

Also document the runtime environment:
- Required permissions/credentials (DB access, API keys, service accounts)
- Dependencies (external APIs, internal services, DB, file storage)
- Runtime environment (local/server/container, OS/runtime versions)
- Security considerations (what must NOT appear in logs)
- Observability (log keys, error logs, trace ID)

Present the spec to the user and confirm before proceeding.

### Phase 2: Write Tests First (TDD)

Write `tests/test_<tool_name>.py` BEFORE writing the implementation. This is the core of TDD — the tests define the contract.

Tests must cover:
- **Happy path** — normal successful operation
- **Edge cases** — boundary values, empty inputs
- **Error cases** — nonexistent resources, permission denied, network timeout, invalid input (empty strings, path traversal, etc.)

Run the tests. They should all FAIL at this point (since the implementation doesn't exist yet). This confirms the tests are actually testing something real.

### Phase 3: Implement

Write `<tool_name>.py` with the goal of making all tests pass. The implementation must include:

**Logging** — every function must emit structured logs with these required keys:

| Key | Description |
|-----|-------------|
| request_id | Request trace ID (generate if not provided) |
| tool_name | Name of the executed tool |
| latency_ms | Execution time in milliseconds |
| status | `success` or `fail` |
| error_code | Error code on failure |

Sensitive information (access keys, secret keys, tokens) must NEVER appear in logs.

**Error handling** — handle these cases explicitly:
- Resource not found
- Insufficient permissions
- Network timeout
- Input validation failure

**I/O convention**:
- Input: JSON
- Output: JSON (even on failure)

**Comments** — focus on WHY, not WHAT. Use the NumPy docstring format for all functions:

```python
def function_name(param1: str, param2: str, param3: str):
    """
    One-line summary of the function.

    Purpose:
        Why this function exists and in what context it is used.

    Parameters
    ----------
    param1 : str
        Description of param1.
    param2 : str
        Description of param2.
    param3 : str
        Description of param3.

    Returns
    -------
    dict
        Description of return value.

    Raises
    ------
    ExceptionType
        When this exception is raised.
    """
```

Comment principles:
1. Every function needs a docstring: purpose, key inputs/outputs, exceptions
2. Complex logic gets intent explanation, not line-by-line narration
3. External dependencies are called out explicitly
4. Security-related handling is explained (why validation exists, what must not be logged)
5. TODOs and improvement notes are clearly marked

### Phase 4: Run Tests and Verify

Run all tests. Every test must pass. If any test fails:
1. Read the failure message
2. Fix the implementation (not the test, unless the test itself has a bug)
3. Re-run until green

### Phase 5: Explain the Code

After all tests pass, explain the implementation to the user:

1. **Architecture overview** — how the function fits into the broader system
2. **Key design decisions** — why you chose this approach over alternatives
3. **Data flow** — how input transforms into output, step by step
4. **Error handling strategy** — what can go wrong and how it's handled
5. **Security considerations** — what's protected and why

Keep the explanation concise but thorough enough that the user understands not just what the code does, but why it's built this way.

---

## Checklist (verify before presenting to user)

- [ ] Spec document is unambiguous — no room for misinterpretation
- [ ] Input/output schemas are JSON-schema-level clear
- [ ] Failure/exception cases are defined
- [ ] Environment/permissions/security are documented
- [ ] Code is maintainable by anyone reading it for the first time
- [ ] All tests pass
- [ ] Sensitive data never appears in logs

---

## Output Structure

```
project/
  <tool_name>.spec.md      # Specification document
  <tool_name>.py            # Implementation
  tests/
    test_<tool_name>.py     # Test cases
```
