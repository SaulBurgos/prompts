"""
GitHub API module for PR Daily Check.

Handles all GitHub CLI operations: fetching PRs, commit SHAs, and saving metadata.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_command(cmd: list[str], capture_output: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed and authenticated."""
    code, _, _ = run_command(["gh", "auth", "status"])
    return code == 0


def fetch_pr_commit_sha(pr_number: int, repo: str) -> str:
    """Fetch the latest commit SHA for a PR."""
    cmd = [
        "gh", "pr", "view", str(pr_number),
        "--repo", repo,
        "--json", "headRefOid"
    ]
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        return ""
    
    try:
        data = json.loads(stdout)
        return data.get("headRefOid", "")
    except json.JSONDecodeError:
        return ""


def fetch_prs_merged_today(repo: str, today: str) -> list[dict]:
    """Fetch PRs merged to main today."""
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--base", "main",
        "--state", "merged",
        "--search", f"merged:>={today}",
        "--json", "number,title,author,url,mergedAt",
        "--limit", "100"
    ]
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"⚠ Warning: Failed to fetch merged PRs: {stderr}")
        return []
    
    try:
        prs = json.loads(stdout) if stdout.strip() else []
        for pr in prs:
            pr["state"] = "merged"
        return prs
    except json.JSONDecodeError:
        print(f"⚠ Warning: Invalid JSON from merged PRs query")
        return []


def fetch_prs_pending(repo: str) -> list[dict]:
    """Fetch open PRs that are not drafts (ready for review/merge)."""
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--base", "main",
        "--state", "open",
        "--search", "-is:draft",
        "--json", "number,title,author,url,createdAt",
        "--limit", "100"
    ]
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"⚠ Warning: Failed to fetch pending PRs: {stderr}")
        return []
    
    try:
        prs = json.loads(stdout) if stdout.strip() else []
        for pr in prs:
            pr["state"] = "pending"
        return prs
    except json.JSONDecodeError:
        print(f"⚠ Warning: Invalid JSON from pending PRs query")
        return []


def fetch_prs_draft(repo: str) -> list[dict]:
    """Fetch draft PRs."""
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--base", "main",
        "--state", "open",
        "--search", "is:draft",
        "--json", "number,title,author,url,createdAt",
        "--limit", "100"
    ]
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"⚠ Warning: Failed to fetch draft PRs: {stderr}")
        return []
    
    try:
        prs = json.loads(stdout) if stdout.strip() else []
        for pr in prs:
            pr["state"] = "draft"
        return prs
    except json.JSONDecodeError:
        print(f"⚠ Warning: Invalid JSON from draft PRs query")
        return []


def fetch_pr_diff(pr_number: int, folder_path: str, repo: str) -> str:
    """Fetch diff for a specific PR, filtered by folder path."""
    cmd = [
        "gh", "pr", "diff", str(pr_number),
        "--repo", repo
    ]
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"  ⚠ Failed to get diff for PR #{pr_number}: {stderr}")
        return ""
    
    # If folder path is specified and not "." (all), filter the diff
    if folder_path and folder_path != ".":
        filtered_lines = []
        include_file = False
        
        for line in stdout.split("\n"):
            # Check if this is a file header
            if line.startswith("diff --git"):
                # Check if the file is in the target folder
                include_file = f"/{folder_path}/" in line or line.endswith(f"/{folder_path}")
            
            if include_file:
                filtered_lines.append(line)
        
        return "\n".join(filtered_lines)
    
    return stdout


# =============================================================================
# Metadata Saving Functions
# =============================================================================

def save_pr_diff(pr_number: int, diff_content: str, output_dir: str):
    """Save PR diff to file."""
    if not diff_content.strip():
        return
    
    filepath = Path(output_dir) / f"pr-{pr_number}.diff"
    filepath.write_text(diff_content)


def save_pr_metadata(prs: list[dict], output_dir: str):
    """Save PR metadata to JSON file."""
    filepath = Path(output_dir) / "pr-list.json"
    
    # Clean up author field (extract login)
    for pr in prs:
        if isinstance(pr.get("author"), dict):
            pr["author"] = pr["author"].get("login", "unknown")
    
    with open(filepath, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_prs": len(prs),
            "prs": prs
        }, f, indent=2)


def save_pr_metadata_with_tracking(analyzed_prs: list[dict], skipped_prs: list[dict], output_dir: str):
    """Save PR metadata including tracking info (analyzed vs skipped)."""
    filepath = Path(output_dir) / "pr-list.json"
    
    # Clean up author field (extract login)
    for pr in analyzed_prs + skipped_prs:
        if isinstance(pr.get("author"), dict):
            pr["author"] = pr["author"].get("login", "unknown")
    
    with open(filepath, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_analyzed": len(analyzed_prs),
            "total_skipped": len(skipped_prs),
            "analyzed_prs": analyzed_prs,
            "skipped_prs": skipped_prs
        }, f, indent=2)


def save_branch_info(target_branch: str, current_branch: str, target_sha: str, 
                     current_sha: str, merge_base_sha: str, folder_path: str, output_dir: str):
    """Save branch comparison metadata to JSON file."""
    filepath = Path(output_dir) / "branch-info.json"
    
    with open(filepath, "w") as f:
        json.dump({
            "mode": "branch",
            "generated_at": datetime.now().isoformat(),
            "target_branch": target_branch,
            "current_branch": current_branch,
            "target_sha": target_sha,
            "current_sha": current_sha,
            "merge_base_sha": merge_base_sha,
            "folder_analyzed": folder_path
        }, f, indent=2)

