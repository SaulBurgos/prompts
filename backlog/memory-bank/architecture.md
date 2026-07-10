---
name: architecture
description: High-level system architecture, key decisions, and component relationships.
last_update_date: 2026-02-05
---

# Architecture

## High-level structure
- **`prompts/`**: Core prompt library - individual Markdown files with reusable prompts
- **`templates/`**: Reusable templates, including `agent-context-kit` for setting up Memory Bank systems
- **`.cursor/`**: Cursor-specific configurations
  - `commands/`: Custom Cursor commands (e.g., `add-prompt-item.md`, `pr-daily-check/`)
  - `skills/`: Reusable workflows (memory-init, memory-update, memory-compress)
- **`docs/memory-bank/`**: Long-term context documentation for this repository
- **`agents/`**: Agent-specific prompt templates
- **`AGENTS.md`**: Root-level agent instructions and rules

## Key decisions
- **File-based storage**: Prompts as Markdown files for simplicity and Git compatibility
- **Git version control**: Full history tracking, branching for experiments, tagging for stable versions
- **Memory Bank pattern**: Structured docs (`brief.md`, `product.md`, `architecture.md`, `tech.md`, `context.md`) for context preservation
- **Cursor integration**: Native support for Cursor's command and skill systems

## Design patterns
- **Template pattern**: `templates/agent-context-kit/` provides reusable structure for other projects
- **Skill pattern**: Reusable workflows in `skills/` directory with YAML frontmatter
- **Command pattern**: Cursor commands in `.cursor/commands/` for common operations

## Critical paths
- Adding new prompt: Create file → Add to Git → Commit with `feat:` prefix
- Editing prompt: Modify file → Review diff → Commit with descriptive message
- Experimenting: Create branch → Make changes → Merge or discard
- Memory Bank updates: Use `memory-update` skill after significant changes
