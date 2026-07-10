# PR Daily Check

Daily check for conflicts with your current work - compare against PRs or a specific branch.

## Prerequisites

- Memory bank initialized (run `init memory bank` first)
- GitHub CLI authenticated (`gh auth status` to verify) - required for PR mode only
- User needs to be working in a branch that is not main, because the comparison will be done against it.

## Workflow

### Step 1: Ask for comparison mode and folder

Before proceeding, ask the user three questions in sequence:

**Question 1: What do you want to compare against?**

1. **PRs** - Compare against merged/pending/draft Pull Requests
2. **A specific branch** - Compare against another branch directly

Wait for user response before continuing.

---

#### If user selected "PRs" (PR Mode):

**Question 2 (PR Mode): Which folder should I analyze for conflicts?**

1. `protiv-rails` - Backend Rails application
2. `@protiv/dashboard` - Frontend Ember dashboard
3. `docs` - Documentation
4. Custom path (ask user to specify)
5. `.` - All folders (entire repo)

Wait for user response, then ask:

**Question 3 (PR Mode): Which PR types do you want to check?**

The user can select one or more:
1. `merged` - PRs merged today (highest priority)
2. `pending` - Open PRs ready for review/merge (medium priority)
3. `draft` - Draft PRs still in progress (lower priority)
4. `all` - All

User can select multiple types (e.g., "merged and pending" or "all three").

Wait for user response before continuing to **Step 2 (PR Mode)**.

---

#### If user selected "A specific branch" (Branch Mode):

**Question 2 (Branch Mode): Which folder should I analyze for conflicts?**

1. `protiv-rails` - Backend Rails application
2. `@protiv/dashboard` - Frontend Ember dashboard
3. `docs` - Documentation
4. Custom path (ask user to specify)
5. `.` - All folders (entire repo)

Wait for user response, then ask:

**Question 3 (Branch Mode): What is the branch name to compare against?**

Ask user to provide the exact branch name (e.g., `feature/other-team-work`, `develop`, `release/v2.0`).

Wait for user response before continuing to **Step 2 (Branch Mode)**.

### Step 2: Run Python script

---

#### Step 2 (PR Mode): Execute PR data collection

Execute the data collection script with the chosen folder and PR types:

```bash
cd /Users/saulburgos/Documents/protiv-v2/protiv-rails && python3 .cursor/commands/pr-daily-check/pr_daily_check.py <folder_path> --types <pr_types>
```

Replace:
- `<folder_path>` with user's choice from Step 1 (Question 2)
- `<pr_types>` with comma-separated list from Step 1 (Question 3), e.g., `merged,pending` or `merged,pending,draft` or `all`

Examples:
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py protiv-rails --types merged`
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py protiv-rails --types merged,pending`
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py protiv-rails --types all`
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py protiv-rails --types all --force` (re-analyze all)

Wait for the script to complete. It will:
- Fetch only the selected PR types (merged/pending/draft)
- **Check each PR's commit SHA against tracking data**
- **Skip PRs that haven't changed since last check**
- Save diffs only for new/changed PRs to `tmp/daily-pr-check/`
- Save metadata to `tmp/daily-pr-check/pr-list.json`
- Update tracking file at `.cursor/docs/pr-impact-reports/pr-tracking.json`

**PR Change Detection:**
- 🆕 **New**: PR not seen before
- 🔄 **Updated**: PR has new commits since last check
- ⏭️ **Skipped**: No changes since last check (won't be analyzed)

Continue to **Step 3 (PR Mode)**.

---

#### Step 2 (Branch Mode): Execute branch comparison

Execute the data collection script with the chosen folder and branch name:

```bash
cd /Users/saulburgos/Documents/protiv-v2/protiv-rails && python3 .cursor/commands/pr-daily-check/pr_daily_check.py <folder_path> --branch <branch_name>
```

Replace:
- `<folder_path>` with user's choice from Step 1 (Question 2)
- `<branch_name>` with user's choice from Step 1 (Question 3)

Examples:
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py protiv-rails --branch feature/other-team-work`
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py @protiv/dashboard --branch develop`
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py . --branch release/v2.0`
- `python3 .cursor/commands/pr-daily-check/pr_daily_check.py protiv-rails --branch develop --force` (re-analyze even if unchanged)

Wait for the script to complete. It will:
- Verify the target branch exists (local or remote)
- **Check target branch SHA against tracking data**
- **Skip analysis if target branch hasn't changed since last check**
- Get diff between target branch and your current branch (HEAD)
- Save diff to `tmp/daily-pr-check/target-branch.diff`
- Save metadata to `tmp/daily-pr-check/branch-info.json`
- Save your branch diff vs merge-base to `tmp/daily-pr-check/my-branch.diff`
- Update tracking file at `.cursor/docs/pr-impact-reports/branch-tracking.json`

**Branch Change Detection:**
- 🆕 **New**: First time comparing against this branch+folder combination
- 🔄 **Updated**: Target branch has new commits since last check
- ⏭️ **Skipped**: Target branch unchanged since last check (won't be analyzed)

Continue to **Step 3 (Branch Mode)**.

### Step 3: Review collected data and confirm analysis

---

#### Step 3 (PR Mode): Review PR data and confirm

Read the following files from `tmp/daily-pr-check/`:

1. **pr-list.json** - PR metadata with tracking info:
   - `analyzed_prs`: PRs that are new or have new commits (will be analyzed)
   - `skipped_prs`: PRs with no changes since last check (won't be analyzed)
2. **pr-*.diff** - Diffs for analyzed PRs only
3. **my-branch.diff** - Current branch changes vs main

**Present a summary to the user:**

```
📊 Data Collection Complete

PRs to Analyze (new/updated):
- PR #XXX: [Title] - [Status: 🆕 New / 🔄 Updated]
- PR #YYY: [Title] - [Status: 🆕 New / 🔄 Updated]
...

PRs Skipped (no changes):
- PR #ZZZ: [Title] - Last checked: YYYY-MM-DD
...

Your Branch Changes:
- Files modified: X files
- Total changes: +XXX / -YYY lines
```

**Ask for confirmation:**

"Ready to proceed with conflict analysis? This will compare the PR diffs against your branch changes and generate a detailed report. Type 'yes' to continue or 'no' to cancel."

**Wait for user response:**
- If user says **"yes"** or confirms: Continue to **Step 4 (PR Mode)**
- If user says **"no"** or cancels: Stop here, present cleanup option, and exit

---

#### Step 3 (Branch Mode): Review branch data and confirm

Read the following files from `tmp/daily-pr-check/`:

1. **branch-info.json** - Branch comparison metadata:
   - `target_branch`: The branch being compared against
   - `current_branch`: Your current branch name
   - `target_sha`: Commit SHA of target branch
   - `current_sha`: Commit SHA of your current branch
   - `merge_base_sha`: Common ancestor commit SHA
   - `folder_analyzed`: The folder that was analyzed
2. **target-branch.diff** - Changes in target branch since merge-base
3. **my-branch.diff** - Your changes since merge-base

**Present a summary to the user:**

```
📊 Data Collection Complete

Branch Comparison:
- Your Branch: [current branch name] (SHA: [short sha])
- Target Branch: [target branch name] (SHA: [short sha])
- Merge Base: [short sha]
- Folder Analyzed: [folder path]
- Status: 🆕 New / 🔄 Updated

Changes Detected:
- Files modified in target branch: X files
- Files modified in your branch: Y files
- Total diff size: +XXX / -YYY lines
```

**Ask for confirmation:**

"Ready to proceed with conflict analysis? This will compare the branch differences and identify potential conflicts. Type 'yes' to continue or 'no' to cancel."

**Wait for user response:**
- If user says **"yes"** or confirms: Continue to **Step 4 (Branch Mode)**
- If user says **"no"** or cancels: Stop here, present cleanup option, and exit

### Step 4: Analyze saved diffs

---

#### Step 4 (PR Mode): Analyze PR diffs

**Important**: Only analyze PRs from `analyzed_prs`. The `skipped_prs` are included for reference only.

Continue to **Step 5 (PR Mode)**.

---

#### Step 4 (Branch Mode): Analyze branch diff

Continue to **Step 5 (Branch Mode)**.

### Step 5: Compare and assign severity

---

#### Step 5 (PR Mode): Compare PR diffs and assign severity

For each PR, compare its diff against `my-branch.diff`:

**Analysis criteria:**

Compare each PR diff against `my-branch.diff` to identify overlapping work:

1. **File-level overlap:**
   - Same files modified in both diffs
   - Files in the same directory as modified files

2. **Code-level overlap:**
   - Same functions, methods, or classes touched
   - Changed function signatures (parameters, return types)
   - Renamed, moved, or deleted files still referenced elsewhere

3. **Dependency overlap:**
   - Shared imports (files that import the same modules)
   - Related database tables or models
   - API endpoints that consume the same services

4. **High-risk areas** (flag if touched in both diffs):
   - Shared utilities (DTOs, schemas, helpers)
   - Domain models (User, Job, ProPay, etc.)
   - Critical business logic (bonus, payroll, billing, attendance)
   - Public APIs or external interfaces
   - Any breaking changes

**Severity levels:**

| Severity | Criteria | Action Required |
|----------|----------|-----------------|
| 🔴 Critical | Same file, overlapping lines | Immediate sync needed |
| 🟠 High | Same file, different sections | Review before merge |
| 🟡 Medium | Related files (same directory, shared imports) | Be aware |
| 🟢 Low | Potentially related (same feature area) | Monitor |

**Group results by PR state:**
1. Merged PRs Today (highest priority - already in main)
2. Pending PRs (medium priority - will merge soon)
3. Draft PRs (lower priority - may change)

Continue to **Step 5 (PR Mode)**.

---

#### Step 5 (Branch Mode): Analyze branch differences and assign severity

Analyze `target-branch.diff` to identify conflicts with your changes in `my-branch.diff`:

1. **File-level overlap:**
   - Same files modified in both diffs
   - Files in the same directory as modified files

2. **Code-level overlap:**
   - Same functions, methods, or classes touched
   - Changed function signatures (parameters, return types)
   - Renamed, moved, or deleted files still referenced elsewhere

3. **Dependency overlap:**
   - Shared imports (files that import the same modules)
   - Related database tables or models
   - API endpoints that consume the same services

4. **High-risk areas** (flag if touched in both diffs):
   - Shared utilities (DTOs, schemas, helpers)
   - Domain models (User, Job, ProPay, etc.)
   - Critical business logic (bonus, payroll, billing, attendance)
   - Public APIs or external interfaces
   - Any breaking changes

**Severity levels:**

| Severity | Criteria | Action Required |
|----------|----------|-----------------|
| 🔴 Critical | Same file, overlapping lines in both branches | Immediate coordination needed |
| 🟠 High | Same file modified in both branches | Review and potentially rebase |
| 🟡 Medium | Related files (same directory, shared imports) | Be aware before merging |
| 🟢 Low | Different files but same feature area | Monitor for integration issues |

Continue to **Step 6 (Branch Mode)**.

### Step 6: Generate report

Determine the report filename using consecutive numbering:

1. Start with base filename: `YYYY-MM-DD.md` (using today's date)
2. Check if `.cursor/docs/pr-impact-reports/YYYY-MM-DD.md` exists
3. If it exists, check for `YYYY-MM-DD-1.md`, `YYYY-MM-DD-2.md`, etc.
4. Use the next available number (e.g., if `2025-11-28.md` and `2025-11-28-1.md` exist, use `2025-11-28-2.md`)
5. If base file doesn't exist, use `YYYY-MM-DD.md` (no suffix)

**Examples:**
- First report today: `2025-11-28.md`
- Second report today: `2025-11-28-1.md`
- Third report today: `2025-11-28-2.md`

Create the markdown report at the determined filename in `.cursor/docs/pr-impact-reports/`

---

#### Step 6 (PR Mode): Generate PR impact report

**Report structure:**

```markdown
# PR Impact Report - YYYY-MM-DD

## Summary

- **Date**: YYYY-MM-DD
- **Mode**: PR Analysis
- **Your Branch**: [branch name]
- **Folder Analyzed**: [folder path]
- **Generated At**: [timestamp]

### Statistics

| Category | Count |
|----------|-------|
| PRs Analyzed (new/updated) | X |
| PRs Skipped (no changes) | X |
| **Total PRs Found** | X |

### PRs by Type (Analyzed Only)

| Type | Count |
|------|-------|
| Merged PRs (today) | X |
| Pending PRs | X |
| Draft PRs | X |

### Conflicts by Severity

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟠 High | X |
| 🟡 Medium | X |
| 🟢 Low | X |

---

## 🔴 Merged PRs Today (Highest Priority)

These PRs are already in main. You may need to rebase.

### PR #XXX: [Title]
- **Author**: @username
- **Merged**: YYYY-MM-DD HH:MM
- **URL**: [link]
- **Severity**: 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

**Conflicting Files:**
- `path/to/file.rb` - Lines XX-YY overlap with your changes

**Recommendation:** [Specific action to take]

---

## 🟠 Pending PRs (Medium Priority)

These PRs may merge soon. Coordinate with authors if conflicts exist.

### PR #XXX: [Title]
[Same structure as above]

---

## 🟡 Draft PRs (Lower Priority)

These PRs are still in progress and may change.

### PR #XXX: [Title]
[Same structure as above]

---

## ⏭️ Skipped PRs (No Changes)

These PRs were skipped because they have no new commits since last check.

| PR | Title | Author | Last Checked |
|----|-------|--------|--------------|
| #XXX | [Title] | @username | YYYY-MM-DD |

---

## Action Items (Have I resolved the conflicts I found?)

1. [ ] [Prioritized action based on severity]
2. [ ] [Next action]
3. [ ] [etc.]

---

*Report generated by /pr-daily-check command (PR Mode)*
```

Continue to **Step 7**.

---

#### Step 6 (Branch Mode): Generate branch comparison report

**Report structure:**

```markdown
# Branch Comparison Report - YYYY-MM-DD

## Summary

- **Date**: YYYY-MM-DD
- **Mode**: Branch Comparison
- **Your Branch**: [current branch name]
- **Compared Against**: [target branch name]
- **Folder Analyzed**: [folder path]
- **Generated At**: [timestamp]

### Branch Information

| Branch | Commit SHA |
|--------|------------|
| Your Branch ([name]) | [sha] |
| Target Branch ([name]) | [sha] |

### Conflicts by Severity

| Severity | Files |
|----------|-------|
| 🔴 Critical | X |
| 🟠 High | X |
| 🟡 Medium | X |
| 🟢 Low | X |

---

## Detailed Analysis

### 🔴 Critical Conflicts

Files with overlapping changes that will likely cause merge conflicts.

#### `path/to/file.rb`
- **Lines in target branch**: XX-YY
- **Lines in your branch**: XX-YY
- **Overlap**: Lines XX-YY modified in both branches

**Recommendation:** Coordinate with the team working on [target branch]. Consider rebasing to resolve conflicts early.

---

### 🟠 High Severity

Same files modified in both branches but different sections.

#### `path/to/other_file.rb`
- **Target branch changes**: [description]
- **Your changes**: [description]

**Recommendation:** Review changes before merging. Test thoroughly after integration.

---

### 🟡 Medium Severity

Related files that may have integration issues.

- `path/to/related_file.rb` - Imports from modified module
- `path/to/another_file.rb` - Same directory as modified files

---

### 🟢 Low Severity

Files in same feature area but unlikely to conflict.

- `path/to/low_risk_file.rb`

---

## Action Items

1. [ ] [Recommended action based on critical conflicts]
2. [ ] [Coordinate with team about specific files]
3. [ ] [Rebase/merge strategy recommendation]

---

*Report generated by /pr-daily-check command (Branch Mode)*
```

Continue to **Step 7**.

### Step 7: Cleanup temporary files

After successfully generating the report, run the cleanup script to delete all temporary files:

```bash
cd /Users/saulburgos/Documents/protiv-v2/protiv-rails && python3 .cursor/commands/pr-daily-check/pr_daily_check_cleanup.py
```

This will remove all files in `tmp/daily-pr-check/` directory:
- **PR Mode**: pr-list.json, pr-*.diff, my-branch.diff
- **Branch Mode**: branch-info.json, target-branch.diff, my-branch.diff

**Note**: Tracking files are NOT deleted (they persist for future comparisons):
- PR tracking: `.cursor/docs/pr-impact-reports/pr-tracking.json`
- Branch tracking: `.cursor/docs/pr-impact-reports/branch-tracking.json`

### Step 8: Present summary to user

After generating the report and cleaning up temporary files, present a brief summary.

---

#### Step 8 (PR Mode): Present PR analysis summary

Present:
1. Total PRs found vs analyzed vs skipped
2. Number of conflicts by severity (for analyzed PRs only)
3. Top 3 most critical items requiring attention
4. Link to full report

Example summary:
```
📊 PR Daily Check Summary
- Found: 15 PRs
- Analyzed: 5 PRs (3 new, 2 updated)
- Skipped: 10 PRs (no changes since last check)
- Conflicts: 1 🔴 Critical, 2 🟠 High, 2 🟡 Medium
```

Ask if the user wants to:
- See detailed analysis of any specific PR
- Open the full report
- Take any immediate action
- Force re-analyze a skipped PR (if needed)

---

#### Step 8 (Branch Mode): Present branch comparison summary

Present:
1. Target branch compared against
2. Total files with conflicts by severity
3. Top critical conflicts requiring attention
4. Link to full report

Example summary:
```
📊 Branch Comparison Summary
- Your Branch: feature/my-work
- Compared Against: feature/other-team-work
- Folder: protiv-rails
- Conflicts: 2 🔴 Critical, 3 🟠 High, 5 🟡 Medium
```

Ask if the user wants to:
- See detailed analysis of any specific file conflict
- Open the full report
- Rebase or merge the target branch
- Coordinate with the team working on the target branch
- Force re-analyze the branch (if it was skipped due to no changes)

