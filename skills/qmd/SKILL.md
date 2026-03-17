---
name: qmd
description: Search, retrieve, and manage markdown knowledge bases, notes, and documentation using QMD. Use when users ask to search notes, find documents, look up information, manage collections, add context, generate embeddings, or perform any QMD-related operation. Trigger on keywords like 'search notes', 'find in docs', 'qmd', 'knowledge base', 'search meetings', 'look up', 'find document'.
version: 1.0.0
author: heesukim
tags: [QMD, search, markdown, knowledge-base, notes, documentation, semantic-search, BM25, embeddings]
allowed-tools: Bash(qmd:*)
---

# QMD - Quick Markdown Search Skill

Local search engine for markdown content. Provides keyword search (BM25), semantic vector search, hybrid search with reranking, document retrieval, collection management, and context annotation.

## Prerequisites

QMD must be installed globally:

```bash
npm install -g @tobilu/qmd
```

Check status before any operation:

```bash
qmd status
```

## Instructions

When the user asks to search, find, retrieve, or manage documents through QMD, follow this guide. Use `$ARGUMENTS` to determine the user's intent and select the appropriate workflow.

---

## Workflow 1: Search & Query

Choose the right search method based on the user's needs.

### Decision Matrix

| User Intent | Command | When to Use |
|---|---|---|
| Knows exact terms, names, code identifiers | `qmd search` | Fast keyword/BM25 search, no LLM needed |
| Natural language question, doesn't know vocabulary | `qmd vsearch` | Semantic vector similarity only |
| Best quality, complex topics, ambiguous queries | `qmd query` | Hybrid search with auto-expansion + reranking (recommended default) |

### Keyword Search (BM25)

```bash
# Simple keyword search
qmd search "project timeline"

# Search within a specific collection
qmd search "API endpoint" -c docs

# Export all matches for processing
qmd search "authentication" --all --files --min-score 0.3

# Limit results
qmd search "deployment" -n 5
```

**When to use:** User knows exact terms, variable names, function names, or specific phrases.

### Semantic Search (Vector)

```bash
# Natural language query
qmd vsearch "how to deploy the application"

# Search specific collection
qmd vsearch "what decisions were made about the database" -c meetings
```

**When to use:** User asks a question in natural language, doesn't know the exact terminology used in documents.

### Hybrid Query (Recommended Default)

```bash
# Auto-expand: QMD generates lex/vec/hyde variations automatically
qmd query "quarterly planning process"

# Structured query document with multiple search types
qmd query $'lex: CAP theorem consistency\nvec: tradeoff between consistency and availability'

# Full structured query with all types
qmd query $'lex: rate limiter\nvec: how does rate limiting handle burst traffic\nhyde: The rate limiter uses a token bucket algorithm with configurable burst size'

# With intent for disambiguation
qmd query $'intent: web page load times\nlex: performance\nvec: how to improve page speed'

# With collection filter
qmd query "deployment strategy" -c docs

# Show score traces for debugging
qmd query --json --explain "authentication flow"
```

**When to use:** Default for most searches. Best recall and precision.

### Query Type Reference

| Type | Method | Best Input |
|---|---|---|
| `lex` | BM25 keyword | 2-5 exact terms, names, code identifiers |
| `vec` | Vector similarity | Full natural language question |
| `hyde` | Hypothetical document | 50-100 words of what the *answer* looks like |
| `expand` | Auto-expansion | Single-line question (LLM generates lex/vec/hyde) |

### Lex Query Syntax

| Syntax | Meaning | Example |
|---|---|---|
| `term` | Prefix match | `perf` matches "performance" |
| `"phrase"` | Exact phrase match | `"rate limiter"` |
| `-term` | Exclude term | `performance -sports` |

### Combining Types for Best Results

| Goal | Approach |
|---|---|
| Know exact terms | `lex` only |
| Don't know vocabulary | Single-line query (implicit `expand`) or `vec` |
| Best recall | `lex` + `vec` |
| Complex topic | `lex` + `vec` + `hyde` |
| Ambiguous query | Add `intent` to any combination |

**Note:** First query line gets 2x weight in fusion scoring. Put your best guess first.

---

## Workflow 2: Document Retrieval

### Get a Single Document

```bash
# By file path (relative to collection)
qmd get "meetings/2024-01-15.md"

# By full QMD URI
qmd get qmd://notes/ideas/project-x.md

# By document ID (shown in search results)
qmd get "#abc123"

# With line slice (start at line, show N lines)
qmd get "meetings/2024-01-15.md":50 -l 30
```

### Get Multiple Documents

```bash
# By glob pattern
qmd multi-get "journals/2025-05*.md"

# By comma-separated list (preserves order)
qmd multi-get notes/foo.md,notes/bar.md

# With line limit per document
qmd multi-get "meetings/2025-*.md" -l 40
```

### List Indexed Files

```bash
# List all indexed files
qmd ls

# List files in a specific collection
qmd ls notes

# List files in a subdirectory
qmd ls notes/meetings
```

---

## Workflow 3: Collection Management

### Add a Collection

```bash
# Add a directory as a collection
qmd collection add ~/notes --name notes
qmd collection add ~/Documents/meetings --name meetings
qmd collection add ~/work/docs --name docs

# Add with custom glob pattern
qmd collection add ~/project --name project --pattern "docs/**/*.md"
```

### List Collections

```bash
qmd collection list
```

### Show Collection Details

```bash
qmd collection show notes
```

### Remove a Collection

```bash
qmd collection remove notes
```

### Rename a Collection

```bash
qmd collection rename old-name new-name
```

---

## Workflow 4: Context Management

Context annotations improve search quality by providing human-written summaries that help QMD understand what each collection or subdirectory contains.

### Add Context

```bash
# Add context to a collection root
qmd context add qmd://notes "Personal notes and ideas about projects and learning"

# Add context to a subdirectory
qmd context add qmd://meetings "Meeting transcripts and notes from team syncs"
qmd context add qmd://meetings/standup "Daily standup meeting notes"

# Add context to docs collection
qmd context add qmd://docs "Work documentation including API specs and architecture decisions"
```

### List Contexts

```bash
qmd context list
```

### Remove Context

```bash
qmd context rm qmd://notes
```

**Best Practice:** Always add context after creating a collection. Context works as a tree — parent context is inherited by child paths. This is QMD's key feature for helping LLMs make better contextual choices.

---

## Workflow 5: Indexing & Embeddings

### Generate/Refresh Embeddings

```bash
# Generate embeddings for all collections
qmd embed

# Force regenerate all embeddings
qmd embed -f
```

### Update Index

```bash
# Re-index all collections (pick up new/changed files)
qmd update

# Re-index and git pull first
qmd update --pull
```

### Cleanup

```bash
# Clear caches and vacuum database
qmd cleanup
```

**When to run:**
- `qmd embed` — After adding a new collection or when `qmd status` shows stale embeddings
- `qmd update` — When files have been added/changed since last index
- `qmd cleanup` — When index size is unexpectedly large or after removing collections

---

## Workflow 6: Full Setup (New Knowledge Base)

Follow this checklist when setting up QMD from scratch:

```
QMD Setup:
- [ ] Step 1: Add collections
- [ ] Step 2: Add context annotations
- [ ] Step 3: Generate embeddings
- [ ] Step 4: Verify with test search
```

**Step 1: Add collections**

```bash
qmd collection add ~/notes --name notes
qmd collection add ~/Documents/meetings --name meetings
qmd collection add ~/work/docs --name docs
```

**Step 2: Add context annotations**

```bash
qmd context add qmd://notes "Personal notes and ideas"
qmd context add qmd://meetings "Meeting transcripts and notes"
qmd context add qmd://docs "Work documentation"
```

**Step 3: Generate embeddings**

```bash
qmd embed
```

**Step 4: Verify with test search**

```bash
qmd status
qmd query "test search to verify setup"
```

---

## Common Patterns

### Search-then-Retrieve Pattern

When the user wants to find and read specific content:

1. Search first to identify relevant documents
2. Retrieve the full document(s) that match

```bash
# Step 1: Find relevant docs
qmd query "deployment architecture"

# Step 2: Get the most relevant result
qmd get "#docid_from_results"
```

### Broad-to-Narrow Pattern

When exploring an unfamiliar topic in the knowledge base:

1. Start with a broad semantic search
2. Narrow with keyword search using terms from results

```bash
# Step 1: Broad exploration
qmd query "how does authentication work"

# Step 2: Narrow with specific terms found
qmd search "OAuth2 refresh token rotation" -c docs
```

### Multi-Collection Cross-Reference

When connecting information across different sources:

```bash
# Search meetings for decisions
qmd query "decided on database migration" -c meetings

# Find related documentation
qmd query "database migration guide" -c docs

# Find personal notes
qmd search "migration" -c notes
```

---

## Troubleshooting

**No results returned:**
- Run `qmd status` to check if collections are indexed
- Run `qmd update` to re-index
- Run `qmd embed` if vector search returns nothing
- Check collection exists: `qmd collection list`

**Stale results:**
- Run `qmd update` to pick up new/changed files
- Run `qmd embed -f` to force refresh embeddings

**Poor search quality:**
- Add context annotations: `qmd context add qmd://collection "description"`
- Use structured queries with multiple types (lex + vec + hyde)
- Add `intent` for ambiguous queries
- Try `qmd query --json --explain "query"` to debug scoring

**Collection not found:**
- Verify path exists and contains .md files
- Re-add: `qmd collection add /path --name name`
