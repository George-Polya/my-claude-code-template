# Plan Template

## Filename Rule

- Save the file under `plan/`.
- Use the `NNN-feature-name.md` format.
- `NNN` must be a zero-padded three-digit sequence such as `001`, `002`, or `013`.
- `feature-name` must be lowercase kebab-case.
- If numbered plans already exist, pick the next highest number.
- If no numbered plan exists, start with `001`.

Example:

```text
plan/001-upload-object-from-url.md
```

## Planning Expectations

- Analyze the codebase before writing the plan.
- Cite real file paths and existing code patterns.
- Keep the plan specific enough that a later implementation pass can execute it without re-planning from scratch.
- Include concise code snippets from the current codebase when they clarify the current flow or the planned change surface.
- Stop after writing the plan. Do not implement the feature in the same turn.

## Markdown Skeleton

```md
# <Feature Name>

Date: YYYY-MM-DD

## 1. Feature Overview

<Brief summary of the requested capability and the user-facing change.>

## 2. Objective

- <Primary goal>
- <Secondary goal or non-goal when relevant>

## 3. Codebase Findings

### 3.1 Current flow

- `<path>`: <What it currently does>
- `<path>`: <Why it matters>

### 3.2 Constraints and patterns

- <Validation rule, architectural boundary, operational constraint, or repository convention>

## 4. Files to Modify

| Path | Why it changes |
|------|----------------|
| `<path>` | <reason> |
| `<path>` | <reason> |

## 5. Proposed Design

### 5.1 Main approach

- <Design decision>
- <Expected behavior>

### 5.2 Layer-by-layer impact

- `<layer or path>`: <planned change>
- `<layer or path>`: <planned change>

## 6. Code Snippets

### 6.1 `<path>`

```python
<short existing code snippet>
```

Why it matters:
- <reason>

### 6.2 `<path>`

```python
<short existing code snippet>
```

Why it matters:
- <reason>

## 7. Step-by-Step Implementation Tasks

- [ ] <Task 1 in execution order>
- [ ] <Task 2 in execution order>
- [ ] <Task 3 in execution order>

## 8. Trade-offs

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| `<option A>` | <pros> | <cons> | <chosen or rejected> |
| `<option B>` | <pros> | <cons> | <chosen or rejected> |

## 9. Validation Plan

- Success cases: <list>
- Failure cases: <list>
- Regression checks: <list>
- Manual verification: <list or `Not required`>

## 10. Risks / Open Questions / Assumptions

- Risk: <risk and mitigation>
- Open question: <unknown that needs confirmation>
- Assumption: <assumption being made>
```

## Quality Checklist

- The plan includes both feature overview and objective.
- The plan lists the files to modify with reasons.
- The plan includes at least one current-code snippet when the change depends on existing flow.
- The implementation tasks are written as Markdown checkboxes.
- The trade-off section compares the chosen direction against at least one alternative.
- The plan ends with validation plus risks, open questions, or assumptions.
