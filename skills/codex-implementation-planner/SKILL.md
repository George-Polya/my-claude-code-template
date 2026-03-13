---
name: codex-implementation-planner
description: Analyze the codebase deeply and write a detailed implementation plan as a Markdown file under `plan/`. Use when the user asks to create a plan before coding, save a feature plan in `plan/`, leave a design note for a specific implementation task, or break a feature into concrete steps without writing the code yet. Trigger especially when the plan must include feature overview and objective, files to modify, code snippets, checkbox implementation tasks, trade-offs, validation scope, and explicit assumptions.
---

# Codex Implementation Planner

## Overview

Study the relevant code paths before planning.
Produce a real Markdown file under `plan/` and stop after the plan is written.

## Workflow

1. Lock the feature scope in one sentence.
2. Inspect the relevant entrypoints, services, domain types, infrastructure adapters, schemas, tests, configuration, and existing docs or plans.
3. Reconstruct the current behavior and constraints from code, not guesses.
4. Choose the output filename in `plan/` using the `001-feature-name.md` pattern.
5. Draft the plan by following `references/plan-template.md`.
6. Respond with the created path and the most important risks or open questions.

## Depth Requirements

- Read enough code to explain the current flow, ownership, constraints, and likely change surface.
- Trace call flow across layers instead of stopping at a directory summary.
- Check existing tests, specs, validators, and related documents to understand the intended contract.
- Reuse established repository patterns instead of inventing a new structure when a working pattern already exists.
- Label weak evidence explicitly as an assumption or open question.

## Planning Rules

- Do not implement the feature in the same turn. Planning only.
- Do not stop at a high-level summary. The plan must be actionable for later coding.
- Prefer concrete file paths, functions, classes, endpoints, settings, and test files.
- Mention companion updates when a contract change implies tests, schemas, validators, specs, docs, or error handling changes.
- Keep the current layer boundaries unless the plan explicitly justifies a change.
- If the user did not provide a filename, scan `plan/` and pick the next numeric prefix. If no numbered plan exists, start with `001-feature-name.md`.
- If older plan files use a different naming scheme, keep the new file in the numbered format unless the user explicitly asks otherwise.

## Required Sections

Every generated plan should include these sections, even for small changes.

- Feature Overview
- Objective
- Codebase Findings
- Files to Modify
- Proposed Design
- Code Snippets
- Step-by-Step Implementation Tasks
- Trade-offs
- Validation Plan
- Risks / Open Questions / Assumptions

## Section Standards

- `Feature Overview` and `Objective`: state what changes and why.
- `Codebase Findings`: explain the current behavior with file-based evidence.
- `Files to Modify`: list exact paths and why each file changes.
- `Code Snippets`: include short, relevant snippets from the current codebase that anchor the plan.
- `Step-by-Step Implementation Tasks`: use Markdown checkboxes and order them for execution.
- `Trade-offs`: compare the chosen approach against at least one alternative when architecture or API behavior changes.
- `Validation Plan`: include success cases, failure cases, regression risk, and manual verification when relevant.

## Repository-Specific Reminders

- Read existing documents under `plan/` first when present.
- Check router, application, domain, infrastructure, schema, and test layers for related behavior.
- Preserve existing architectural boundaries and error or validation patterns unless the plan explicitly calls out a justified change.
- Include operational concerns such as logging, limits, permissions, timeouts, or security rules when they matter to the feature.

## Resources

- `references/plan-template.md`
  Read this before drafting. It defines the filename pattern, required sections, and reusable Markdown skeleton.
