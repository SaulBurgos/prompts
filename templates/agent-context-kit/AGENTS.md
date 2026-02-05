# AGENTS.md

## Purpose
This project uses a Memory Bank to preserve context across sessions. The Memory Bank lives in
`docs/memory-bank/` and is the source of truth for project state.

## Session Start (always)
1. Read `docs/memory-bank/brief.md`.
2. Read `docs/memory-bank/product.md`.
3. Read `docs/memory-bank/architecture.md`.
4. Read `docs/memory-bank/tech.md`.
5. Read `docs/memory-bank/context.md`.
6. Read `docs/memory-bank/tasks.md`.

If a file uses YAML frontmatter, read the frontmatter first and treat it as authoritative. For
very large files, read only the frontmatter or summary unless the task depends on details inside.

## Communication Rules
- Be extremely concise; preserve action -> result logic.
- Never present unverified content as fact. Label unverified statements with
  `[Inference]`, `[Speculation]`, or `[Unverified]`.
- Ask before writing code or running destructive commands.
- Validate claims against the codebase and reference file paths when citing code.

## Memory Status
At the start of each task, include:
- `[Memory Bank: Active]` if Memory Bank files were read.
- `[Memory Bank: Missing]` if they are missing or empty (warn the user).

## Memory Updates
After significant changes (or when the user requests `update memory bank`):
- Review all Memory Bank files.
- Update `docs/memory-bank/context.md` with a dated entry:
  `## YYYY-MM-DD - [Section Name]`.
- Update `last_update_date` in any modified Memory Bank files.
- Report any drift between the Memory Bank and the codebase.

## Memory Compression
When `context.md` exceeds 300+ lines or spans 4+ weeks, use the `memory-compress` skill to
summarize older entries while preserving critical decisions.

## Skills
Reusable workflows live in `skills/`:
- `skills/memory-update/` for updating Memory Bank files.
- `skills/memory-compress/` for compressing long history.
- `skills/memory-init/` for initializing a new Memory Bank.
