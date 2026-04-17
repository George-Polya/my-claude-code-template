---
name: codebase-analyzer
description: "Deeply analyze a codebase or specific folder to fully understand its architecture, design patterns, data flow, business logic, dependencies, APIs, and all other aspects. Use this skill PROACTIVELY whenever the user asks to understand, analyze, or explore code — e.g., 'analyze this codebase', 'how does this project work?', 'explain the folder structure', 'break down this code for me', 'what does this project do?', 'deep dive into this code'. This is for comprehensive understanding, NOT for code review or bug fixing."
---

# Codebase Analyzer

Deeply read and fully understand a codebase, then explain it to the user in detail.

## Determining the Analysis Scope

- If the user mentions a specific folder or path → analyze only that folder
- If no specific path is mentioned → analyze the entire project

## Analysis Process

Analyze systematically. Order matters — understand the big picture first, then drill into details so you never lose context.

### Phase 1: Overall Structure

1. **Project root exploration**: Read config files (package.json, pyproject.toml, Cargo.toml, go.mod, etc.), README, and directory structure
2. **Directory tree**: Map out major directories and their roles
3. **Entry points**: Identify main files, app initialization points, server startup locations

### Phase 2: Dependencies & Tech Stack

1. **External dependencies**: Libraries/frameworks used and the role each plays
2. **Internal dependencies**: Import/require relationships between modules, dependency direction
3. **Tech stack summary**: Languages, frameworks, databases, infrastructure tools

### Phase 3: Architecture & Design Patterns

1. **Architecture pattern**: MVC, layered, hexagonal, microservices, etc.
2. **Design patterns**: Singleton, factory, observer, middleware chain, etc. — patterns found in the code
3. **Module organization**: Responsibilities and boundaries of each module/package

### Phase 4: Data Flow & Business Logic

1. **Request flow**: The full path from incoming request to outgoing response
2. **Data models**: Key entities, schemas, type definitions
3. **Core business logic**: The essential processing logic that defines the project's purpose
4. **State management**: Where data is stored and how it is transformed

### Phase 5: APIs & Interfaces

1. **External APIs**: REST/GraphQL/gRPC endpoints, WebSocket, etc.
2. **Internal interfaces**: Public APIs between modules, abstract classes, interfaces
3. **Events/messages**: Event-driven communication structures, if any

### Phase 6: Configuration & Environment

1. **Environment config**: Environment variables, config files, secret management
2. **Build & deploy**: CI/CD, Docker, build scripts
3. **Test structure**: Test frameworks, testing strategy

## Output Rules

### Default: Explain directly in conversation
Present findings in a well-structured format covering key discoveries from each phase. Be thorough but readable.

### Markdown document (only when explicitly requested)
Save as a markdown file only when the user explicitly asks — e.g., "save as a document", "create a markdown file", "write it to a file". Save as `CODEBASE_ANALYSIS.md` in the root of the analyzed target.

## Quality Standards

- **Read everything**: Actually read all significant files. Do not guess from filenames alone
- **Go deep**: Understand internal implementations, not just function signatures
- **Connect the dots**: Explain how files connect to form the whole, not just describe files individually
- **Explain the why**: Beyond "what this code does", explain "why it is structured this way"
- **No test execution**: Do not run tests, build commands, or execute any code. This skill is purely for reading and understanding — never for running anything
