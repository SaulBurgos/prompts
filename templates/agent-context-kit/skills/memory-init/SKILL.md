---
name: memory-init
description: Initialize a new Memory Bank by analyzing the project and drafting core docs.
---

# Memory Bank Initialization

## When to use
- First-time setup of a project Memory Bank.
- The user requests `build memory bank` or `initialize memory bank`.

## Steps
1. Review the repository structure, key code paths, and existing docs.
2. Create `docs/memory-bank/` core files if missing:
   - `brief.md`, `product.md`, `architecture.md`, `tech.md`, `context.md`, `tasks.md`.
3. Draft concise initial content in each file.
4. Ask the user to verify and correct the content, especially `brief.md`.
5. Set `last_update_date` in all created or modified files.

## Notes
- Be thorough during initialization; mistakes compound.
- Keep the initial content short and factual.
