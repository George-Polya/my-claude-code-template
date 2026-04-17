# Tool Usage Rule

## General Rules
- ALWAYS follow the tool call schema exactly and provide all necessary parameters
- NEVER call tools that are not explicitly provided
- Use `web_search` when information is missing from the codebase or when external documentation/fact verification is needed
- **NEVER refer to tool names directly when speaking to the USER.** Explain *why* you are calling a tool
- Only call tools when necessary. If the task is general or you know the answer, respond directly

## Search & Read Priority
- Prefer `codebase_search` (semantic search) over `grep_search`/`file_search`/`list_dir`
- When calling `codebase_search`, reuse the User's query wording
- Use `read_file` to **read large sections at once**. Avoid repeated small read calls
- Stop searching/reading and proceed once sufficient information is gathered

## Available Tools
| Tool | Purpose |
| --- | --- |
| `codebase_search` | Semantic search (top priority) |
| `read_file` | Read file contents (up to 250 lines per call). Reading entire files is disallowed unless edited/attached by the user |
| `run_terminal_cmd` | Propose a command to run (user approval required). Append `\| cat` for interactive commands. Use `is_background` for long-running tasks. No newlines in the command |
| `list_dir` | Directory discovery |
| `grep_search` | Fast text/regex exact matching (ripgrep) |
| `edit_file` | Propose edits to existing files. Use `// ... existing code ...` for unchanged parts. Provide sufficient context and minimize unchanged code repetition |
| `file_search` | Fuzzy search for file paths |
| `delete_file` | Delete a file |
| `reapply` | Reapply immediately after a failed `edit_file` |
| `web_search` | Search the web for real-time/up-to-date information |
| `diff_history` | Retrieve recent file change history |

## Honest Output
- Reflect actual tool outcomes (success/failure/error) as they are
- Inform the User of any issues beforehand
- Never fabricate content that differs from actual results
