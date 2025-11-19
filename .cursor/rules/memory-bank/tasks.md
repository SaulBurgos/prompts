Last update date: 19 nov 2025

# Tasks

This document contains reusable workflows for common operations in this prompt library project.

---

## Simple Tasks

### Add Command

**Purpose:** Create a new Cursor command using the standard template structure.

**Files to create:**
- `.cursor/commands/{your-command-name}.md` – new command file

**Steps:**

1. **Create the command file**
   - Navigate to `.cursor/commands/` directory (create it if it doesn't exist)
   - Create a new file: `{your-command-name}.md` (use kebab-case for the filename)

2. **Fill in the template structure**
   - Use the following template and fill in each section:

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

3. **Commit the new command**
   ```bash
   git add .cursor/commands/{your-command-name}.md
   git commit -m "feat: add {command-name} cursor command"
   ```

**Important notes:**
- Directory structure: `.cursor/commands/` must exist in project root
- File naming: Use kebab-case (e.g., `add-new-prompt.md`, `review-prompt-history.md`)
- Template sections: Overview, Steps (with categories), and Checklist sections are standard
- Each command should be self-contained and follow the template structure for consistency

**Example:**
- Command name: `add-new-prompt`
- File: `.cursor/commands/add-new-prompt.md`
- Content: Template filled with steps for creating a new prompt file in `prompts/` folder

---

## Complex Tasks (Detailed Task Files)

_No complex tasks documented yet. Complex tasks (> 100 lines) will be stored in separate files referenced here._

