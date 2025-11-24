# Add Prompt Item

## Overview

Guide the user through adding a new prompt to their personal prompt library. This command asks questions about the prompt they want to add, then creates a properly formatted Markdown file in the `prompts/` folder following the structure documented in `README.md`.

## Steps

1. **Gather Information About the New Prompt**
   - Ask the user: "What would you like to name this prompt? (This will be the filename, use kebab-case, e.g., 'coding-debugging-helper')"
   - Ask the user: "What is the actual prompt text you want to save?"
   - Ask the user: "Do you have any notes about this prompt? (e.g., when to use it, what works well, examples, usage tips)"
   - Ask the user: "Any additional context or examples you'd like to include?"

2. **Create the Prompt File**
   - Create the file: `prompts/{prompt-name}.md` (using kebab-case filename)
   - Structure the file according to `README.md` format:
     - `# Prompt` section with the actual prompt text
     - `## Notes` section with usage notes, tips, examples (if provided)
   - Use minimal line breaks: one blank line between sections, no extra blank lines within sections
   - Ensure proper Markdown formatting

3. **Review and Confirm**
   - Show the user the file structure/content that will be created
   - Ask for confirmation before proceeding

4. **Save to Git**
   - Add the file: `git add prompts/{prompt-name}.md`
   - Commit with message: `git commit -m "feat: add {prompt-name} prompt"`
   - Optionally show git status to confirm

## Checklist

- [ ] Asked user for prompt name (kebab-case filename)
- [ ] Asked user for prompt text content
- [ ] Asked user for notes/usage information (optional)
- [ ] Created file in `prompts/` folder with correct structure
- [ ] File includes `# Prompt` section
- [ ] File includes `## Notes` section (if notes provided)
- [ ] Used minimal line breaks (one blank line between sections, no extra blank lines within sections)
- [ ] The user prompt text should be wrap three simple backticks (```) similar to code in markdownfiles
- [ ] Reviewed file content with user
- [ ] Added file to git
- [ ] Committed with descriptive message
- [ ] Verified file appears in `prompts/` directory

## Important Notes

- **File naming**: Use kebab-case (e.g., `coding-debugging-helper.md`, `writing-idea-brainstorm.md`)
- **File structure**: Follow `README.md` format:
  - `# Prompt` - the actual prompt text
  - `## Notes` - comments, usage tips, examples
- **Formatting**: Use minimal line breaks - one blank line between sections, no extra blank lines within sections
- **Git workflow**: Always commit new prompts with `feat:` prefix in commit message
- **Location**: All prompts go in `prompts/` folder at project root
- **Parameters**: User can provide initial context after command (e.g., `/add-prompt-item for debugging Python code`)

