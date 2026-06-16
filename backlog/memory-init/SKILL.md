---
name: memory-init
description: Initialize a new Memory Bank by analyzing the project and drafting core docs.
---

# Memory Bank Initialization

## When to use

### Session Initialization

   When user explicitly requests with the phrase `init memory bank` you MUST:

   - Read ALL memory bank files (this is not optional) in the following order: 
   brief.md → product.md → architecture.md → tech.md → context.md. 
   - The memory bank files are located in folder called `/memory-bank/`.
   - you will include `[Memory Bank: Active]` at the beginning of you response if you successfully read the memory bank files, or `[Memory Bank: Missing]` if the folder doesn't exist or is empty. 
   - If memory bank is missing, you will warn the user about potential issues and suggest initialization. You must give short summarize your understanding of the project to confirm alignment with the user's expectations.

## First-time setup of a project Memory Bank.

When user explicitly requests with the phrase `build memory bank`. you'll perform an exhaustive analysis of the project, including:

- All source code files and their relationships
- Configuration files and build system setup
- Project structure and organization patterns
- Documentation and comments
- Dependencies and external integrations
- Testing frameworks and patterns

You must be extremely thorough during initialization, spending extra time and effort to build a comprehensive understanding of the project. A high-quality initialization will dramatically improve all future interactions, while a rushed or incomplete initialization will permanently limit my effectiveness.


##  File Types & Formats

The Memory Bank consists of core files and optional context files, all in Markdown format.

### Core Files (Required)
1. `brief.md`:
   - This file is created and maintained manually by the developer. Don't edit this file directly but suggest to user to update it if it can be improved.
   - Foundation document that shapes all other files
   - Created at project start if it doesn't exist
   - Defines core requirements and goals
   - Source of truth for project scope
   - Must include "Last update date" at the top of the file (or YAML frontmatter for complex files)

Example of prompt to create the brief.md content:

`
   Provide a concise and comprehensive description of this project, highlighting its main objectives, key features, used technologies and significance. Then, write this description into a text file named appropriately to reflect the project's content, ensuring clarity and professionalism in the writing. Stay brief and short.
`

2. `product.md`:
   - Why this project exists
   - Problems it solves
   - How it should work
   - User experience goals
   - Must include "Last update date" at the top of the file (or YAML frontmatter for complex files)

3. `context.md`:
   - This file should be short and factual, not creative or speculative.
   - Current work focus
   - Recent changes
   - Next steps
   - **For long-running projects**: May include optional "Summary View" section with hierarchical summaries (weekly/monthly) to improve navigation of extensive history

4. `architecture.md`:
   - System architecture
   - Source Code paths
   - Key technical decisions
   - Design patterns in use
   - Component relationships
   - Critical implementation paths
   - Keep high-level and concise; if the file exceeds 150 lines, move detailed flows or diagrams to sub-docs (e.g., data-flows.md) and link them in the frontmatter.
   - Must include "Last update date" at the top of the file (or YAML frontmatter for complex files)

5. `tech.md`:
   - Technologies used
   - Development setup
   - Technical constraints
   - Dependencies
   - Tool usage patterns
   - Must include "Last update date" at the top of the file (or YAML frontmatter for complex files)


