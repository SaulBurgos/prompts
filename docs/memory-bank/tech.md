---
name: tech
description: Technologies, setup, constraints, and tooling patterns.
last_update_date: 2026-02-04
---

# Technologies and Setup

## Core technologies
- **Git**: Version control system for tracking prompt evolution
- **Markdown**: File format for all prompts and documentation
- **Python**: Used for Cursor commands (e.g., `pr-daily-check` scripts)
- **Cursor IDE**: Primary development environment with custom commands and skills

## Development setup
- Standard Git repository - clone and use
- No build process or dependencies required for basic usage
- Python scripts in `.cursor/commands/pr-daily-check/` may require Python 3.x
- Cursor IDE recommended for full feature support (commands, skills)

## Constraints
- Single-user repository (not designed for collaboration)
- File-based storage (no database)
- Markdown-only format for prompts
- Cursor-specific features require Cursor IDE

## Tooling patterns
- **Git workflow**: Feature branches (`feat:`), experiments (`exp:`), tweaks (`tweak:`)
- **Commit messages**: Concise, grammar sacrificed for brevity
- **File naming**: Kebab-case for prompt files (e.g., `coding-debugging-helper.md`)
- **YAML frontmatter**: Used in skills and Memory Bank docs for metadata
