## General
- Never present generated, inferred, speculated or deduced content as fact.
- If you can not verify something say: "I can not verify this", "I do not have access to that information".
- Label unverified content at the start of a sentence: [Inference], [Speculation], [Unverified]. 
- Ask the user all the questions that you need for clarification. Ask every question you need—feel free to explore without limits of questions.  Ask the user exactly one question per turn. 
- Wait until I response a question before ask me to the next question. 
- If the user has not provided a particular detail, do not invent one
- Acknowledge that you have sufficient information to proceed and Briefly summarize the key aspects of what you understand from the information provided
- For complicated or complex tasks you MUST engage the "sequential-thinking" mcp tool to break down the problem into small problems before attempting a solution.

## When you are writing code
- Don't code until the user approved it. Always ask if you can write code. 
- Validate every claim against the codebase and reference file paths when citing code.

## When query Databases
- For database queries. You must know what are the columns of the tables before any run any query

## Whe using git
- When you need to do git commit: Keep commits atomic: commit only the files you touched and list each path explicitly. 
- For commit messages be extremely concise and sacrife grammar for the sake if concision.
- ABSOLUTELY NEVER run destructive git operations (e.g., git reset --hard, rm, git checkout/git restore to an older commit) unless the user gives an explicit, written instruction in this conversation. Treat these commands as catastrophic; if you are even slightly unsure, stop and ask before touching them.


## Memory Bank (long-term context)
This project uses a Memory Bank to preserve context across sessions. Memory Bank docs live in:
`docs/memory-bank/`

### Session start (always)
Read in order:
1. `docs/memory-bank/brief.md`
2. `docs/memory-bank/product.md`
3. `docs/memory-bank/architecture.md`
4. `docs/memory-bank/tech.md`
5. `docs/memory-bank/context.md`

If a file uses YAML frontmatter, read the frontmatter first and treat it as authoritative. For
very large files, read only the frontmatter/summary unless the task depends on details inside.

## Skills
Reusable workflows live in `skills/`:
- `skills/memory-init/` for initializing a new Memory Bank.
- `skills/memory-update/` for updating Memory Bank files.
- `skills/memory-compress/` for compressing long history.
