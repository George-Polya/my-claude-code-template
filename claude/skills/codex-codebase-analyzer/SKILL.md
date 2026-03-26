---
name: codex-codebase-analyzer
description: Deeply inspect an entire codebase or a specific folder and explain its structure, entrypoints, runtime flow, dependencies, tests, operational settings, and risks. Use when the user asks for whole-project analysis, wants to understand how a particular directory works in detail, or requests a Markdown report that documents how the codebase behaves.
---

# Codex Codebase Analyzer

## Overview

Reconstruct how the codebase actually works instead of stopping at a shallow directory tour.
Ground every explanation in concrete file paths and code evidence instead of filling gaps with guesswork.

## Quick Start

1. Confirm the analysis scope. If no path is provided, treat the current working directory as the default scope.
2. Run `scripts/repo_inventory.py` to build a structural inventory.
3. Use that inventory to prioritize entrypoints, configuration files, tests, and core modules.
4. Trace real call flow and data movement through the system.
5. If the user wants a written deliverable, use `references/analysis-template.md` to structure the Markdown report.

Example:

```bash
python3 scripts/repo_inventory.py .
python3 scripts/repo_inventory.py src/routes --max-depth 4 --format markdown
```

## Workflow

### 1. Separate scope from requested output

- Decide whether the request covers the whole repository or a specific folder.
- Separate interactive explanation, code review, and Markdown file output into distinct deliverable types.
- When the scope is large, find entrypoints and configuration first, then narrow into the core subsystems.

### 2. Build a structural inventory

- Run `scripts/repo_inventory.py` first to collect directory layout, extension counts, notable files, and a tree view.
- Exclude noise such as `.git`, virtual environments, caches, and generated directories during the inventory pass.
- Before reading everything, highlight likely entrypoints such as `main`, `app`, `server`, `routes`, `controllers`, `service`, `domain`, `schema`, `tests`, `config`, `Dockerfile`, `pyproject.toml`, and `package.json`.

### 3. Trace runtime flow

- Start from the entrypoint and follow control flow from routers or CLI commands into services, repositories, and external integrations.
- Track dependency injection, environment variables, configuration objects, and exception translation alongside the main flow.
- Explain async jobs, middleware, hooks, signals, and background workers in their own section when they exist.
- Read tests as evidence for intended behavior and coverage boundaries.
- Do not execute test suites or test code unless the user explicitly asks for execution.

### 4. Capture important details deeply

- For each important directory, explain what it owns, who calls it, what it returns, and how it fails.
- In layered codebases, inspect DTOs, schemas, interfaces, exception types, and boundary validation rules.
- Look for hidden constraints such as naming rules, path rules, size limits, timeouts, retries, permissions, and feature flags.
- Cross-check design intent against tests and configuration when the implementation alone is ambiguous.

### 5. Write the result clearly

- If the request is conversational, answer around the core flow and cite relevant file paths.
- If the user asks to organize the findings in Markdown, leave a document behind, or save a file, read `references/analysis-template.md` and follow that structure.
- If no destination is specified, save to `research/` when that directory exists; otherwise save in the workspace root as `<scope>-analysis.md`.
- Include scope, core flow, component responsibilities, testing or validation observations, and risks or unresolved areas in the report.

## Analysis Principles

- Start broad, then go deep.
- Do not stop at directory summaries; reconstruct execution order.
- Prefer evidence over inference and label unresolved points clearly.
- Do not execute tests during analysis unless the user explicitly requests it.
- Include configuration, failure paths, tests, and operational constraints when the user asks for detail.
- In large repositories, expand iteratively from entrypoints and central modules instead of trying to read everything at once.

## Output Standards

- Name file paths and function or class identifiers explicitly.
- Separate architecture summary from runtime flow explanation.
- Do not mix confirmed findings with speculation.
- Mention major risks or confusing edges even when the user did not explicitly ask for them.

## Resources

- `scripts/repo_inventory.py`
  Use this helper first to build a structural inventory for either the whole repository or a specific folder.
- `references/analysis-template.md`
  Read this only when the user wants a saved Markdown deliverable or a fully structured written report.
