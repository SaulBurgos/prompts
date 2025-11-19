Last update date: 19 nov 2025

# Tasks

This document contains reusable workflows for common operations in this prompt library project.

---

## Simple Tasks

### Add Command

**Purpose:** Create a new Cursor command that can be triggered with `/` prefix in the chat input box. Commands are reusable workflows stored as plain Markdown files.

**How commands work:**
- Commands appear automatically when you type `/` in the Cursor chat input box
- They can be stored in three locations:
  1. **Project commands**: `.cursor/commands/` (project root) - recommended for this repo
  2. **Global commands**: `~/.cursor/commands/` (home directory) - available across all projects
  3. **Team commands**: Created in Cursor Dashboard (Team/Enterprise plans)
- Commands accept parameters: any text typed after the command name is included in the prompt
- Example usage: `/commit and /pr these changes to address DX-523`

**Files to create:**
- `.cursor/commands/{your-command-name}.md` – new command file (plain Markdown)

**Steps:**

1. **Create the command file**
   - Navigate to `.cursor/commands/` directory in project root (create it if it doesn't exist)
   - Create a new file: `{your-command-name}.md` (use kebab-case for the filename, e.g., `review-code.md`, `write-tests.md`)

2. **Write the command content**
   - Commands are plain Markdown files describing what the command should do
   - Use the following suggested template structure (flexible based on your needs):

```markdown
# [Command Name]

## Overview
[Brief description of what the command does]

## Steps

1. **[Step Category 1]**
   - [Action item 1]
   - [Action item 2]
   - [Action item 3]

2. **[Step Category 2]**
   - [Action item 1]
   - [Action item 2]

## [Section Name] Checklist
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]
```

3. **Test the command**
   - Type `/` in Cursor chat input to verify the command appears in the list
   - The command name will be based on the filename (without `.md` extension)

4. **Commit the new command**
   ```bash
   git add .cursor/commands/{your-command-name}.md
   git commit -m "feat: add {command-name} cursor command"
   ```

**Important notes:**
- **Directory structure**: `.cursor/commands/` must exist in project root for project commands
- **File naming**: Use kebab-case (e.g., `add-new-prompt.md`, `review-prompt-history.md`, `code-review-checklist.md`)
- **Content format**: Plain Markdown - the template structure is suggested but flexible
- **Parameters**: Users can add context after the command name (e.g., `/review-code in src/utils/`)
- **Reference**: See [Cursor Commands Documentation](https://cursor.com/docs/agent/chat/commands) for official details

**Example:**
- Command name: `add-new-prompt`
- File: `.cursor/commands/add-new-prompt.md`
- Usage: Type `/add-new-prompt` in chat, optionally with parameters like `/add-new-prompt for debugging Python code`
- Content: Markdown describing the workflow for creating a new prompt file in `prompts/` folder

---

## Complex Tasks (Detailed Task Files)

_No complex tasks documented yet. Complex tasks (> 100 lines) will be stored in separate files referenced here._

