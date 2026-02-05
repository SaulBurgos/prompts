# AGENTS.md

This file is a “README for agents”: project context + working rules + commands.

## Project overview
- **What this project is**: [fill in]
- **Primary goal**: [fill in]
- **Non-goals**: [fill in]

## Repo layout
- **Key directories**: [fill in]
- **Where to start reading**: [fill in]

## Setup commands
- **Install deps**: `[fill in]`
- **Start dev server**: `[fill in]`
- **Run tests**: `[fill in]`
- **Lint / typecheck**: `[fill in]`

## Testing instructions
- **CI plan**: [point to `.github/workflows/` or equivalent]
- **Fast loop**: [fill in]
- **Full suite**: [fill in]
- **Expectations**:
  - Fix failing tests/type/lint errors before finishing.
  - Add/update tests when behavior changes.

## Code style guidelines
- **Formatting**: [prettier/rubocop/etc]
- **Naming**: [fill in]
- **Architecture constraints**: [fill in]

## Security considerations
- Never commit secrets (tokens, API keys, `.env`, credentials).
- Ask before running destructive operations.
- If the repo touches prod data/PII, be explicit about constraints and handling.

## Agent operating rules
- Be extremely concise; preserve action -> result logic.
- Never present unverified content as fact. Label unverified statements with:
  `[Inference]`, `[Speculation]`, or `[Unverified]`.
- Ask before writing code or running destructive commands.
- Validate claims against the codebase and reference file paths when citing code.

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
6. `docs/memory-bank/tasks.md`

If a file uses YAML frontmatter, read the frontmatter first and treat it as authoritative. For
very large files, read only the frontmatter/summary unless the task depends on details inside.

## Skills
Reusable workflows live in `skills/`:
- `skills/memory-init/` for initializing a new Memory Bank.
- `skills/memory-update/` for updating Memory Bank files.
- `skills/memory-compress/` for compressing long history.
