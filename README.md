# My Library Prompts

My Personal Prompts library that I have used in all my projects

## Using Git with My Prompt Library

### Overview
- **Goal**: use Git to safely save, edit, and track the evolution of each prompt.
- **What Git gives me**: a full history of changes, the ability to experiment in branches, and tags to mark especially good versions.

I store all prompts as Markdown files in a simple structure:

- **Folder structure**
  - `prompts/`
    - `my-prompt-name.md`
    - `another-prompt.md`

Each prompt file can include:

- `## Notes` – comments on how it works, ideas, examples, etc. (comes first)
- `# Prompt` – the actual text I paste/use.

---

### One-time setup (per machine)

Repository is already created, but for reference:

```bash
git init              # only if this is not already a git repo
git add README.md     # track the readme
git add prompts/      # track all prompt files
git commit -m "chore: initial prompt library"
```

---

### Saving a new prompt

1. **Create the file** in `prompts/`:
   - Example: `prompts/coding-debugging-helper.md`
2. **Write the content** inside the file (see file structure above for `## Notes` and `# Prompt` sections)
3. **Add and commit** the new prompt:

```bash
git add prompts/coding-debugging-helper.md
git commit -m "feat: add coding-debugging-helper prompt"
```

---

### Editing and improving a prompt

#### Normal/small edits (directly on main branch)

1. Edit the existing file in `prompts/`.
2. Optionally review what changed:

```bash
git diff
```

3. Commit the change with a clear message:

```bash
git add prompts/coding-debugging-helper.md
git commit -m "tweak: refine coding-debugging-helper instructions"
```

#### Bigger experiments (use a branch)

1. Create and switch to an experiment branch:

```bash
git switch -c exp-coding-debugging-new-style
```

2. Edit the prompt file and commit as many times as needed:

```bash
git add prompts/coding-debugging-helper.md
git commit -m "exp: try new style for coding-debugging-helper"
```

3. When finished experimenting:
   - If I **like** the result, merge it into `main`:

```bash
git switch main
git merge exp-coding-debugging-new-style
```

   - If I **don’t like** the result, just delete the branch:

```bash
git branch -D exp-coding-debugging-new-style
```

---

### Reviewing the history of a prompt

- **See all commits that touched a specific prompt**:

```bash
git log prompts/coding-debugging-helper.md
```

- **See line-by-line changes over time**:

```bash
git log -p prompts/coding-debugging-helper.md
```

- **See who/when changed a specific line** (deep dive):

```bash
git blame prompts/coding-debugging-helper.md
```

---

### Marking great versions with tags

When a prompt feels especially good or “stable”, I mark that version with an **annotated tag**:

```bash
git tag -a coding-debugging-v1 -m "First stable version of coding-debugging-helper"
```

- **List all tags**:

```bash
git tag
```

- **Compare current version of a prompt with a tagged version**:

```bash
git diff coding-debugging-v1 -- prompts/coding-debugging-helper.md
```

If I ever want to copy or restore text from that tagged version, I can inspect it and manually copy the parts I like.

---

### Notes about prompts

Notes go in the `## Notes` section of each prompt file (see file structure above). Use it for:
- When to use this prompt
- What works well / what doesn't
- Example conversations or usage tips

Because notes live in the same file, Git automatically tracks changes to both the **prompt text** and **notes** together over time.
