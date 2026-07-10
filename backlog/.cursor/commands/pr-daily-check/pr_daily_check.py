#!/usr/bin/env python3
"""
PR Daily Check Script

Fetches PR data (merged, pending, draft) from GitHub OR compares against a specific branch.
Used by the /pr-daily-check Cursor command.

Usage (PR Mode):
    python3 pr_daily_check.py <folder_path> --types <pr_types> [--force]
    python3 pr_daily_check.py protiv-rails --types merged
    python3 pr_daily_check.py protiv-rails --types merged,pending
    python3 pr_daily_check.py protiv-rails --types all
    python3 pr_daily_check.py protiv-rails --types all --force  # Re-analyze all

Usage (Branch Mode):
    python3 pr_daily_check.py <folder_path> --branch <branch_name> [--force]
    python3 pr_daily_check.py protiv-rails --branch feature/other-team-work
    python3 pr_daily_check.py . --branch develop
    python3 pr_daily_check.py protiv-rails --branch develop --force  # Re-analyze even if unchanged

PR types: merged, pending, draft, all (comma-separated)
Options:
    --force   Force re-analyze (ignore tracking data) - works for both PR and branch modes
    --branch  Compare against a specific branch instead of PRs

Tracking Files:
    PR Mode:     .cursor/docs/pr-impact-reports/pr-tracking.json
    Branch Mode: .cursor/docs/pr-impact-reports/branch-tracking.json
"""

import sys
import argparse
import os

# Add the parent directory to sys.path for direct script execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_operations import init_paths
from runners import run_branch_mode, run_pr_mode


# Configuration
REPO = "protiv/protiv-v2"
# These paths are relative to the git root
OUTPUT_DIR_RELATIVE = "protiv-rails/tmp/daily-pr-check"
TRACKING_FILE_RELATIVE = "protiv-rails/.cursor/docs/pr-impact-reports/pr-tracking.json"
BRANCH_TRACKING_FILE_RELATIVE = "protiv-rails/.cursor/docs/pr-impact-reports/branch-tracking.json"


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Fetch PR data or branch diff for conflict analysis")
    parser.add_argument("folder_path", help="Folder to focus on (e.g., 'protiv-rails', '.')")
    
    # Mutually exclusive group: --types OR --branch
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--types", help="Comma-separated PR types: merged,pending,draft,all")
    mode_group.add_argument("--branch", help="Compare against a specific branch instead of PRs")
    
    parser.add_argument("--force", action="store_true", help="Force re-analyze (ignore tracking) - works for both PR and branch modes")
    
    args = parser.parse_args()
    folder_path = args.folder_path
    
    # Initialize git root and paths
    git_root, output_dir, tracking_file, branch_tracking_file = init_paths(
        OUTPUT_DIR_RELATIVE,
        TRACKING_FILE_RELATIVE,
        BRANCH_TRACKING_FILE_RELATIVE
    )
    print(f"Working from git root: {git_root}")
    print()
    
    # Branch mode
    if args.branch:
        run_branch_mode(
            folder_path=folder_path,
            target_branch=args.branch,
            force_analyze=args.force,
            git_root=git_root,
            output_dir=output_dir,
            branch_tracking_file=branch_tracking_file
        )
        return
    
    # PR mode
    pr_types_raw = [t.strip().lower() for t in args.types.split(",")]
    
    # Handle "all" option - expand to all three types
    if "all" in pr_types_raw:
        pr_types = ["merged", "pending", "draft"]
    else:
        pr_types = pr_types_raw
    
    # Validate PR types
    valid_types = {"merged", "pending", "draft"}
    invalid_types = set(pr_types) - valid_types
    if invalid_types:
        print(f"✗ Invalid PR types: {', '.join(invalid_types)}")
        print(f"  Valid types: merged, pending, draft, all")
        sys.exit(1)
    
    run_pr_mode(
        folder_path=folder_path,
        pr_types=pr_types,
        force_analyze=args.force,
        git_root=git_root,
        output_dir=output_dir,
        tracking_file=tracking_file,
        repo=REPO
    )


if __name__ == "__main__":
    main()
