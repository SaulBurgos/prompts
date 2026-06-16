---
name: memory-compress
description: Compress long Memory Bank context history while preserving critical decisions.
---

# Memory Compression

## When to use
- `context.md` exceeds 300+ lines or spans 4+ weeks.
- The user requests `compress memory bank`.

## Strategy
### Basic Compression (simple projects)
- Read all of `context.md`.
- Summarize older entries while keeping recent detail.
- Preserve critical decisions and blockers.

### Hierarchical Compression (long-running projects)
Use this structure:
- Summary View (Monthly + Weekly)
- Detailed Entries (Recent 4 weeks)
- Archived Context (optional links)

Age-based rules:
- **Recent (4 weeks)**: keep full detail + weekly summaries.
- **1-3 months**: keep weekly summaries + compress details to 2-3 bullets.
- **3-6 months**: keep monthly summaries only.
- **6+ months**: archive to separate file and keep a short summary.

## Steps
1. Read `context.md` fully and assess age/size.
2. Generate weekly summaries from recent detailed entries.
3. Generate monthly summaries from weekly entries.
4. Apply age-based compression.
5. Archive very old content if needed.
