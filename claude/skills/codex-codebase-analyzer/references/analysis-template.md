# Analysis Report Template

Read this file only when the user asks for a Markdown deliverable or wants the analysis saved as a document.

## Suggested Titles

- Whole repository: `# Codebase Analysis Report`
- Specific folder: `# <folder-name> Analysis Report`

## Suggested Sections

### 1. Scope and Assumptions

- Target path
- Excluded areas
- Evidence files used in the analysis

### 2. Structure at a Glance

- Top-level directory responsibilities
- Primary entrypoints
- Important configuration files

### 3. Core Runtime Flow

- Where execution or request handling starts
- Which layers it passes through
- Where it connects to external systems

### 4. Directory or Module Responsibilities

- What each directory owns
- Representative files and key functions or classes
- Inputs, outputs, and failure paths

### 5. Testing and Validation Observations

- What tests exist
- What behavior those tests actually guarantee
- Which guarantees are missing or weak
- Whether the analysis was based on reading tests only without executing them

### 6. Operational and Configuration Notes

- Environment variables
- Dependency injection
- Build or runtime entry process
- Deployment or CI-relevant settings

### 7. Risks and Unresolved Areas

- Structurally confusing areas
- Hidden constraints
- Points that cannot be confirmed from code evidence alone

### 8. Reference Files

- Critical file paths
- Optional one-line role summary for each file

## Writing Rules

- Prioritize reconstructed execution order over raw directory listing.
- Keep confirmed findings separate from inference.
- Name file paths and function or class identifiers together.
- In long reports, put the conclusion and main flow in the opening paragraph.

## File Placement Rules

- If the user specifies a destination, use it.
- If no destination is given and a `research/` directory exists, save there.
- Otherwise save in the current workspace root as `<scope>-analysis.md`.
