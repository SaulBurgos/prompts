"""
Runner module for PR Daily Check.

Contains the main execution logic for both PR mode and Branch mode.
"""

import sys
from datetime import datetime

from tracking import (
    load_pr_tracking_data,
    save_pr_tracking_data,
    is_pr_changed,
    load_branch_tracking_data,
    save_branch_tracking_data,
    is_branch_changed,
)
from github_api import (
    check_gh_cli,
    fetch_pr_commit_sha,
    fetch_prs_merged_today,
    fetch_prs_pending,
    fetch_prs_draft,
    fetch_pr_diff,
    save_pr_diff,
    save_pr_metadata,
    save_pr_metadata_with_tracking,
    save_branch_info,
)
from git_operations import (
    ensure_output_dir,
    get_current_branch_name,
    get_branch_commit_sha,
    check_branch_exists,
    get_merge_base,
    get_branch_ref,
    get_my_branch_diff,
    get_diff_from_base,
    save_my_branch_diff,
    save_target_branch_diff,
)


def get_today_date() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def run_branch_mode(folder_path: str, target_branch: str, force_analyze: bool,
                    git_root: str, output_dir: str, branch_tracking_file: str):
    """Run branch comparison mode."""
    print("=" * 60)
    print("Branch Comparison Mode")
    print("=" * 60)
    print(f"Git root: {git_root}")
    print(f"Folder focus: {folder_path if folder_path != '.' else 'All folders'}")
    print(f"Target branch: {target_branch}")
    print(f"Force re-analyze: {'Yes' if force_analyze else 'No'}")
    print(f"Date: {get_today_date()}")
    print()
    
    # Check if target branch exists
    print("Checking target branch...")
    if not check_branch_exists(target_branch):
        print(f"✗ Branch '{target_branch}' does not exist (checked local and origin)")
        sys.exit(1)
    print(f"✓ Branch '{target_branch}' found")
    
    # Get current branch info
    current_branch = get_current_branch_name()
    print(f"✓ Current branch: {current_branch}")
    
    if current_branch == target_branch:
        print("✗ Cannot compare branch to itself")
        sys.exit(1)
    
    # Create output directory
    ensure_output_dir(output_dir)
    print()
    
    # Get branch references
    target_ref = get_branch_ref(target_branch)
    print(f"  Using target ref: {target_ref}")
    
    # Get commit SHAs
    print("Getting commit information...")
    target_sha = get_branch_commit_sha(target_ref)
    current_sha = get_branch_commit_sha("HEAD")
    print(f"  Target SHA: {target_sha[:8] if target_sha else 'unknown'}...")
    print(f"  Current SHA: {current_sha[:8] if current_sha else 'unknown'}...")
    print()
    
    # Load branch tracking data and check if analysis needed
    print("Loading branch tracking data...")
    tracking_data = load_branch_tracking_data(branch_tracking_file)
    
    if force_analyze:
        print("⚠️  Force mode: will re-analyze branch (ignoring tracking)")
        should_analyze = True
        change_reason = "forced"
    else:
        if tracking_data.get("last_run"):
            print(f"✓ Last run: {tracking_data['last_run']}")
            print(f"✓ Tracked branches: {len(tracking_data.get('branches', {}))}")
        else:
            print("✓ First run - no tracking data yet")
        
        # Check if target branch has changed
        should_analyze, change_reason, last_checked = is_branch_changed(
            target_branch, target_sha, folder_path, tracking_data
        )
        
        if should_analyze:
            if change_reason == "new":
                print(f"🆕 First time comparing against '{target_branch}' for folder '{folder_path}'")
            else:
                print(f"🔄 Target branch has new commits since last check ({last_checked})")
        else:
            print(f"⏭️  Target branch unchanged since last check ({last_checked})")
            print()
            print("=" * 60)
            print("✓ Branch comparison skipped - no changes in target branch")
            print(f"  Target branch: {target_branch}")
            print(f"  Last checked: {last_checked}")
            print(f"  Target SHA: {target_sha[:8]}...")
            print()
            print("  To force re-analysis, run with --force flag:")
            print(f"    python3 pr_daily_check.py {folder_path} --branch {target_branch} --force")
            print("=" * 60)
            sys.exit(0)
    
    print()
    
    # Get merge-base (common ancestor)
    print("Finding merge-base (common ancestor)...")
    merge_base_sha = get_merge_base(target_ref, "HEAD")
    if not merge_base_sha:
        print("⚠ Could not find merge-base, falling back to direct diff")
        merge_base_sha = target_sha
    else:
        print(f"  Merge-base SHA: {merge_base_sha[:8]}...")
    print()
    
    # Get YOUR changes (merge-base → HEAD)
    print(f"Getting YOUR changes (merge-base → HEAD)...")
    my_diff = get_diff_from_base(merge_base_sha, "HEAD", folder_path)
    save_my_branch_diff(my_diff, output_dir)
    if my_diff.strip():
        my_diff_lines = len([l for l in my_diff.split('\n') if l.startswith('+') or l.startswith('-')])
        print(f"✓ Saved to {output_dir}/my-branch.diff ({my_diff_lines} changed lines)")
    else:
        print("⚠ No changes in your branch since merge-base")
    print()
    
    # Get TARGET BRANCH changes (merge-base → target)
    print(f"Getting TARGET BRANCH changes (merge-base → {target_branch})...")
    target_diff = get_diff_from_base(merge_base_sha, target_ref, folder_path)
    save_target_branch_diff(target_diff, output_dir)
    if target_diff.strip():
        target_diff_lines = len([l for l in target_diff.split('\n') if l.startswith('+') or l.startswith('-')])
        print(f"✓ Saved to {output_dir}/target-branch.diff ({target_diff_lines} changed lines)")
    else:
        print(f"⚠ No changes in {target_branch} since merge-base")
    print()
    
    # Save branch metadata
    print("Saving branch comparison metadata...")
    save_branch_info(target_branch, current_branch, target_sha, current_sha, merge_base_sha, folder_path, output_dir)
    print(f"✓ Saved to {output_dir}/branch-info.json")
    
    # Update tracking data
    print()
    print("Updating branch tracking data...")
    today = get_today_date()
    branch_key = f"{target_branch}:{folder_path}"
    tracking_data.setdefault("branches", {})[branch_key] = {
        "target_sha": target_sha,
        "target_branch": target_branch,
        "my_branch": current_branch,
        "my_sha": current_sha,
        "folder_analyzed": folder_path,
        "last_checked": today,
        "change_reason": change_reason
    }
    save_branch_tracking_data(tracking_data, branch_tracking_file)
    print(f"✓ Tracking data saved to {branch_tracking_file}")
    
    print()
    print("=" * 60)
    print("✓ Branch comparison data collection complete!")
    print(f"  Output directory: {output_dir}/")
    print(f"  Tracking file: {branch_tracking_file}")
    print()
    print(f"  Files created:")
    print(f"    - branch-info.json (branch metadata + merge-base)")
    print(f"    - my-branch.diff (YOUR changes since merge-base)")
    print(f"    - target-branch.diff ({target_branch} changes since merge-base)")
    print()
    print("  For conflict analysis, compare files that appear in BOTH diffs.")
    print()
    print("Next: Run /pr-daily-check command to analyze conflicts")
    print("=" * 60)


def run_pr_mode(folder_path: str, pr_types: list[str], force_analyze: bool,
                git_root: str, output_dir: str, tracking_file: str, repo: str):
    """Run PR analysis mode."""
    print("=" * 60)
    print("PR Daily Check Script")
    print("=" * 60)
    print(f"Git root: {git_root}")
    print(f"Repository: {repo}")
    print(f"Folder focus: {folder_path if folder_path != '.' else 'All folders'}")
    print(f"PR types: {', '.join(pr_types)}")
    print(f"Force re-analyze: {'Yes' if force_analyze else 'No'}")
    print(f"Date: {get_today_date()}")
    print()
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_gh_cli():
        print("✗ GitHub CLI not authenticated. Run: gh auth login")
        sys.exit(1)
    print("✓ GitHub CLI authenticated")
    
    # Create output directory
    ensure_output_dir(output_dir)
    print()
    
    # Fetch PRs based on selected types
    print("Fetching PRs...")
    today = get_today_date()
    
    all_prs = []
    
    if "merged" in pr_types:
        print("  → Merged PRs (today)...", end=" ", flush=True)
        merged_prs = fetch_prs_merged_today(repo, today)
        print(f"found {len(merged_prs)}")
        all_prs.extend(merged_prs)
    
    if "pending" in pr_types:
        print("  → Pending PRs (open, not draft)...", end=" ", flush=True)
        pending_prs = fetch_prs_pending(repo)
        print(f"found {len(pending_prs)}")
        all_prs.extend(pending_prs)
    
    if "draft" in pr_types:
        print("  → Draft PRs...", end=" ", flush=True)
        draft_prs = fetch_prs_draft(repo)
        print(f"found {len(draft_prs)}")
        all_prs.extend(draft_prs)
    print(f"\nTotal PRs to analyze: {len(all_prs)}")
    print()
    
    if not all_prs:
        print("No PRs found. Nothing to analyze.")
        # Still save empty metadata for consistency
        save_pr_metadata([], output_dir)
        sys.exit(0)
    
    # Load tracking data
    print("Loading PR tracking data...")
    tracking_data = load_pr_tracking_data(tracking_file)
    if force_analyze:
        print("⚠️  Force mode: will re-analyze all PRs (ignoring tracking)")
    elif tracking_data.get("last_run"):
        print(f"✓ Last run: {tracking_data['last_run']}")
        print(f"✓ Tracked PRs: {len(tracking_data.get('prs', {}))}")
    else:
        print("✓ First run - no tracking data yet")
    print()
    
    # Check which PRs have changed
    print("Checking for PR changes...")
    prs_to_analyze = []
    prs_skipped = []
    
    for pr in all_prs:
        pr_num = pr["number"]
        pr_state = pr["state"]
        print(f"  → PR #{pr_num} ({pr_state})...", end=" ", flush=True)
        
        # Fetch current commit SHA
        current_sha = fetch_pr_commit_sha(pr_num, repo)
        if not current_sha:
            print("couldn't fetch SHA, will analyze")
            pr["sha"] = ""
            pr["change_reason"] = "unknown"
            prs_to_analyze.append(pr)
            continue
        
        pr["sha"] = current_sha
        
        # Force mode: analyze all PRs
        if force_analyze:
            pr["change_reason"] = "forced"
            prs_to_analyze.append(pr)
            print(f"🔄 forced re-analyze")
            continue
        
        # Check if changed
        has_changed, reason = is_pr_changed(pr_num, current_sha, tracking_data)
        
        if has_changed:
            pr["change_reason"] = reason
            prs_to_analyze.append(pr)
            if reason == "new":
                print(f"🆕 new PR")
            else:
                print(f"🔄 updated (new commits)")
        else:
            # Get last checked date for display
            last_checked = tracking_data["prs"].get(str(pr_num), {}).get("last_checked", "unknown")
            pr["last_checked"] = last_checked
            prs_skipped.append(pr)
            print(f"⏭️  skipped (no changes since {last_checked})")
    
    print()
    print(f"PRs to analyze: {len(prs_to_analyze)}")
    print(f"PRs skipped (no changes): {len(prs_skipped)}")
    print()
    
    # Fetch diffs only for changed PRs
    if prs_to_analyze:
        print("Fetching PR diffs for changed PRs...")
        for pr in prs_to_analyze:
            pr_num = pr["number"]
            pr_state = pr["state"]
            change_reason = pr.get("change_reason", "")
            print(f"  → PR #{pr_num} ({pr_state}, {change_reason})...", end=" ", flush=True)
            
            diff = fetch_pr_diff(pr_num, folder_path, repo)
            if diff.strip():
                save_pr_diff(pr_num, diff, output_dir)
                print("saved")
            else:
                print("no changes in target folder")
    else:
        print("No PRs need analysis - all unchanged since last check.")
    
    print()
    
    # Get current branch diff
    print("Getting current branch diff (main..HEAD)...")
    my_diff = get_my_branch_diff(folder_path)
    save_my_branch_diff(my_diff, output_dir)
    if my_diff.strip():
        print(f"✓ Saved to {output_dir}/my-branch.diff")
    else:
        print("⚠ No changes in current branch (or same as main)")
    
    print()
    
    # Update tracking data for analyzed PRs
    print("Updating PR tracking data...")
    today = get_today_date()
    for pr in prs_to_analyze:
        pr_key = str(pr["number"])
        tracking_data.setdefault("prs", {})[pr_key] = {
            "sha": pr.get("sha", ""),
            "last_checked": today,
            "title": pr.get("title", ""),
            "state": pr.get("state", "")
        }
    
    save_pr_tracking_data(tracking_data, tracking_file)
    print(f"✓ Tracking data saved to {tracking_file}")
    
    print()
    
    # Save metadata (include both analyzed and skipped for report)
    print("Saving PR metadata...")
    save_pr_metadata_with_tracking(prs_to_analyze, prs_skipped, output_dir)
    print(f"✓ Saved to {output_dir}/pr-list.json")
    
    print()
    print("=" * 60)
    print("✓ Data collection complete!")
    print(f"  Output directory: {output_dir}/")
    print(f"  Tracking file: {tracking_file}")
    print()
    print(f"  Summary:")
    print(f"    - PRs analyzed: {len(prs_to_analyze)}")
    print(f"    - PRs skipped (no changes): {len(prs_skipped)}")
    print()
    print(f"  Files created:")
    print(f"    - pr-list.json (metadata)")
    print(f"    - pr-*.diff (PR diffs for changed PRs)")
    print(f"    - my-branch.diff (your changes)")
    print()
    print("Next: Run /pr-daily-check command to analyze conflicts")
    print("=" * 60)

