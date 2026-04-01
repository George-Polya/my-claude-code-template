---
name: spec-writer
description: >
  Writes API specification documents (`<tool_name>.spec.md`) for new functions, APIs, or tools.
  Use this skill PROACTIVELY whenever the user asks to write a spec, create an API spec, define a function spec,
  or draft a specification document — including phrases like "spec document", "API spec", "write a spec",
  "define the spec", "spec for this function". This skill ONLY produces the spec document — it does not
  write tests or implementation code. Do NOT use when the user asks to implement, build, or write code.
---

# Spec Writer Skill

This skill produces a single deliverable: `<tool_name>.spec.md` — a complete API specification document that defines the function's interface, behavior, constraints, and environment before any code is written.

The spec document serves as the contract that both tests and implementation derive from. Writing the spec first forces clarity on what the function does, what it accepts, what it returns, and how it fails — before anyone gets lost in implementation details.

---

## Workflow

### Step 1: Understand the Request

Read the codebase to understand the existing structure, patterns, and conventions. If the request is ambiguous, ask clarifying questions before writing.

Key things to clarify:
- What does this function do and when is it called?
- What are the inputs and outputs?
- What external systems does it depend on?
- What can go wrong?

### Step 2: Write the Spec Document

Create `<tool_name>.spec.md` using the `Write` tool. The document follows this structure:

```markdown
# <function_name>

> One-line description of the function.

## Usage Scenario

When and why this function is called. What triggers it, what context it operates in.

## Input Parameters

| Parameter | Type | Required | Example | Validation Rules |
|-----------|------|----------|---------|-----------------|
| param1 | str | Yes | "example" | Max 255 chars |
| param2 | int | No | 10 | Range: 1-100 |

## Output Schema

### Success Response

```json
{
  "status": "success",
  "data": { ... }
}
```

### Failure Response

```json
{
  "status": "fail",
  "error_code": "RESOURCE_NOT_FOUND",
  "message": "The requested resource does not exist."
}
```

## Error Cases

| Error Code | Condition | HTTP Status |
|------------|-----------|-------------|
| RESOURCE_NOT_FOUND | Target resource does not exist | 404 |
| PERMISSION_DENIED | Insufficient permissions | 403 |
| VALIDATION_ERROR | Invalid input | 400 |
| TIMEOUT | Operation exceeded time limit | 408 |

## Constraints / Guardrails

- Max processing time: ...
- Max data size: ...
- Rate limits: ...
- Input validation: ...
- Path traversal prevention: ...

## Runtime Environment

- **Permissions/Credentials**: DB access, API keys, service accounts needed
- **Dependencies**: External APIs, internal services, DB, file storage
- **Execution Environment**: Local/server/container, OS/runtime versions

## Security

- Sensitive information that must NOT appear in logs (access keys, secret keys, tokens)
- Input validation rationale

## Observability

Required log keys:

| Key | Description |
|-----|-------------|
| request_id | Request trace ID (generate if not provided) |
| tool_name | Name of the executed tool |
| latency_ms | Execution time in milliseconds |
| status | `success` or `fail` |
| error_code | Error code on failure |

## Sample Request / Response

### Request

```json
{
  "param1": "example_value",
  "param2": 10
}
```

### Response (Success)

```json
{
  "status": "success",
  "data": { ... }
}
```

### Response (Failure)

```json
{
  "status": "fail",
  "error_code": "VALIDATION_ERROR",
  "message": "param2 must be between 1 and 100."
}
```
```

### Step 3: Present and Confirm

After writing the spec file, present a summary to the user covering:
- Function purpose
- Key inputs/outputs
- Error cases
- Notable constraints or security considerations

Ask the user to review and confirm before they proceed to tests or implementation.

---

## Checklist (verify before presenting)

- [ ] Function name and purpose are unambiguous
- [ ] Input/output schemas are JSON-schema-level clear
- [ ] At least one sample request/response is included
- [ ] All failure/exception cases are defined with error codes
- [ ] Environment/permissions/security are documented
- [ ] Observability log keys are specified
- [ ] Sensitive data handling is called out

---

## Output

```
project/
  <tool_name>.spec.md      # Specification document (the only output)
```
