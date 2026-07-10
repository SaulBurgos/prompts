---
name: memory-update
description: Synchronize Memory Bank docs with the current project state after significant changes.
---

# Memory Update

## When to use
- After significant changes to code or architecture.
- When the user requests `update memory bank`.
- When you detect drift between docs and code.

## Steps
1. Read all Memory Bank files in `docs/memory-bank/`.
2. Review recent changes in the codebase and compare against `architecture.md` and `tech.md`.
3. Update `context.md` with a dated entry:
   - `## YYYY-MM-DD - [Section Name]`
   - Include **Status**, **Recent changes**, and **Next steps**.
4. Update `last_update_date` in any modified Memory Bank files.
5. Report significant drift to the user.

## Notes
- Keep entries factual and concise.
- Prioritize `brief.md` as the source of truth if conflicts appear.
