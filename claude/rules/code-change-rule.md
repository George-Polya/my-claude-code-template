# Code Change Rule

## Output Policy
- NEVER output code directly to the USER. Use code edit tools (`edit_file`)
- Use code edit tools at most once per turn
- **Write code following Object-Oriented Programming and SOLID Principles**

## Runnable Code
- Generated code must be runnable
- Group edits to the same file into one `edit_file` call
- When creating from scratch:
  - Include dependency files (`requirements.txt`, etc.)
  - Include a README
- For new web apps, aim for a modern UI/UX
- Never generate non-textual code (binary, long hashes)

## Edit Workflow
- Read the file contents/sections before editing (except for small appends or creating new files)
- Bundle edits to the same file into a single call
- Fix introduced linter errors when the solution is clear. **Stop after 3 attempts on the same file and ask the User**
- If a reasonable `edit_file` wasn't applied correctly, try `reapply`

## Search Before Writing
- Search the codebase for existing implementations, patterns, and conventions before writing code
- Read sufficient context to understand how relevant modules work
- Identify reusable components first
- Stop and ask if something is unclear

## Surgical Changes
- No features beyond what was asked
- No abstractions for single-use code
- No speculative "flexibility" or error handling for impossible scenarios
- If 200 lines could be 50, rewrite it
- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken. Match existing style
- Only remove imports/variables/functions that YOUR changes made unused
- Don't remove pre-existing dead code unless asked — mention it instead

## Test
- Every changed line should trace directly to the user's request
- Test the code before declaring it done
