# Agent Context Kit

This folder is a tool-agnostic starter kit for `AGENTS.md` + Agent Skills + Memory Bank docs.
Copy it into any project to give AI agents stable instructions and long-term context.

## How to use
1. Copy the contents of this folder into the root of your target project:
   - `AGENTS.md`
   - `docs/memory-bank/`
   - `skills/`
2. Edit `docs/memory-bank/brief.md` and `product.md` to describe the project.
3. Update `docs/memory-bank/context.md` after significant work.
4. Use skills in `skills/` for repeatable workflows.

## Notes
- `AGENTS.md` is plain Markdown for maximum compatibility.
- Skills follow the Agent Skills spec (directory + `SKILL.md` with YAML frontmatter).
- Keep Memory Bank files concise and factual.
