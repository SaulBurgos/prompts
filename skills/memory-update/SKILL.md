---
name: memory-update
description: Synchronize Memory Bank docs with the current project state after significant changes.
---

# Memory Update

## When to use
Memory Bank updates occur when:

1. You or the User Discover new project patterns
2. After implementing significant changes
3. When user explicitly requests with the phrase `update memory bank` (MUST review ALL files)
4. When context needs clarification

## Steps
1. Read all Memory Bank files in `docs/memory-bank/`. in the following order: 
   brief.md → product.md → architecture.md → tech.md → context.md. 
2. Identify discrepancies between memory bank documentation and current codebase
3. Report significant drift to user (e.g., architectural changes, renamed modules, new technologies)
4. Document current state
5. Document Insights & Patterns
6. Update `last_update_date` in any modified Memory Bank files.
7. Update `context.md` with a dated entry:
   - `## YYYY-MM-DD - [Section Name]`
   - Include **Status**, **Recent changes**, and **Next steps**.
5. Report significant drift to the user.

