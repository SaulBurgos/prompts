---
name: tasks
description: Index of repetitive tasks and their workflows. Simple tasks documented inline; complex tasks linked to dedicated files.
last_update_date: 2026-02-04
---

# Tasks

## Simple Tasks

### Adding a new prompt
**Purpose**: Add a new reusable prompt to the library.

**Files to modify**:
- `prompts/{prompt-name}.md` (create new file)

**Workflow**:
1. Create new Markdown file in `prompts/` directory using kebab-case naming
2. Structure file with:
   - `## Notes` section (optional - comments, usage tips, examples)
   - `# Prompt` section (the actual prompt text)
3. Add and commit:
   ```bash
   git add prompts/{prompt-name}.md
   git commit -m "feat: add {prompt-name} prompt"
   ```

**Notes**:
- Use descriptive, kebab-case filenames
- Keep notes section concise and practical
- Commit messages use `feat:` prefix for new prompts

### Editing an existing prompt
**Purpose**: Update or refine an existing prompt.

**Files to modify**:
- `prompts/{prompt-name}.md`

**Workflow**:
1. Edit the prompt file directly
2. Review changes: `git diff prompts/{prompt-name}.md`
3. Commit:
   ```bash
   git add prompts/{prompt-name}.md
   git commit -m "tweak: refine {prompt-name} instructions"
   ```

**Notes**:
- Small edits can be done directly on main branch
- For experiments, create a branch: `git switch -c exp-{prompt-name}-{description}`
- Commit messages use `tweak:` prefix for refinements

### Experimenting with a prompt (branch workflow)
**Purpose**: Test significant changes to a prompt without affecting main branch.

**Files to modify**:
- `prompts/{prompt-name}.md`

**Workflow**:
1. Create experiment branch: `git switch -c exp-{prompt-name}-{description}`
2. Make changes and commit as needed
3. When finished:
   - If successful: `git switch main && git merge exp-{prompt-name}-{description}`
   - If unsuccessful: `git branch -D exp-{prompt-name}-{description}`

**Notes**:
- Use `exp:` prefix in commit messages
- Delete branch if experiment doesn't work out

## Complex Tasks

_No complex tasks documented yet. Add entries here when multi-phase workflows or external integrations are needed._
