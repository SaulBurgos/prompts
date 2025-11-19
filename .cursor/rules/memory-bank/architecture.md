Last update date: 19 nov 2025

# Architecture

## High-level structure

- Local Git repository on macOS.
- Core folders and files:
  - `README.md` – human-facing description of the prompt library and Git workflow.
  - `prompts/` – intended location for individual prompt files (one Markdown file per prompt).
  - `.cursor/rules/memory-bank/` – long-term Memory Bank for this project.

## Prompt storage pattern

- Each prompt is stored in its own Markdown file, e.g. `prompts/coding-debugging-helper.md`.
- Recommended structure inside each prompt file:
  - `# Prompt` – actual text used with AI tools.
  - `## Notes` – how/when it is used, what works, examples, and ideas for improvement.
- Git tracks both the prompt text and the notes together as the file evolves.

## Git workflow relationship

- Commits capture meaningful changes to prompts and notes.
- Branches can be used for larger experiments on specific prompts.
- Tags can mark “stable” or especially good prompt versions at the repository level.
- History inspection tools (`git log`, `git diff`, `git blame`) are used to review how prompts evolve.


