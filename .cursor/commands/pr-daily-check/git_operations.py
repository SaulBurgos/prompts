"""
Git Operations module for PR Daily Check.

Handles all git-related operations: repository info, branch management, and diff generation.
"""

import os
import subprocess
import sys
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


def get_git_root() -> str:
    """Get the root directory of the git repository."""
    cmd = ["git", "rev-parse", "--show-toplevel"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def init_paths(output_dir_relative: str, tracking_file_relative: str, 
               branch_tracking_file_relative: str) -> tuple[str, str, str, str]:
    """
    Initialize GIT_ROOT and all paths, change to git root directory.
    
    Returns: (git_root, output_dir, tracking_file, branch_tracking_file)
    """
    git_root = get_git_root()
    
    if not git_root:
        print("✗ Not in a git repository")
        sys.exit(1)
    
    # Set absolute paths for output and tracking files
    output_dir = os.path.join(git_root, output_dir_relative)
    tracking_file = os.path.join(git_root, tracking_file_relative)
    branch_tracking_file = os.path.join(git_root, branch_tracking_file_relative)
    
    # Change to git root directory for all subsequent operations
    os.chdir(git_root)
    
    return git_root, output_dir, tracking_file, branch_tracking_file


def ensure_output_dir(output_dir: str):
    """Create output directory if it doesn't exist."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {output_dir}/")


def get_current_branch_name() -> str:
    """Get the name of the current git branch."""
    cmd = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        return "unknown"
    return stdout.strip()


def get_branch_commit_sha(branch_name: str) -> str:
    """Get the commit SHA of a branch."""
    cmd = ["git", "rev-parse", branch_name]
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        return ""
    return stdout.strip()


def check_branch_exists(branch_name: str) -> bool:
    """Check if a branch exists (local or remote)."""
    # Try local branch first
    cmd = ["git", "rev-parse", "--verify", branch_name]
    code, _, _ = run_command(cmd)
    if code == 0:
        return True
    
    # Try remote branch
    cmd = ["git", "rev-parse", "--verify", f"origin/{branch_name}"]
    code, _, _ = run_command(cmd)
    return code == 0


def get_merge_base(branch1: str, branch2: str) -> str:
    """Get the merge-base (common ancestor) between two branches."""
    cmd = ["git", "merge-base", branch1, branch2]
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        return ""
    return stdout.strip()


def get_branch_ref(branch_name: str) -> str:
    """Get the proper reference for a branch (local or origin/)."""
    cmd = ["git", "rev-parse", "--verify", branch_name]
    code, _, _ = run_command(cmd)
    if code == 0:
        return branch_name
    return f"origin/{branch_name}"


# =============================================================================
# Diff Operations
# =============================================================================

def get_my_branch_diff(folder_path: str) -> str:
    """Get diff between current branch and main, filtered by folder."""
    cmd = ["git", "diff", "main..HEAD"]
    
    if folder_path and folder_path != ".":
        cmd.append("--")
        cmd.append(folder_path)
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"⚠ Warning: Failed to get branch diff: {stderr}")
        return ""
    
    return stdout


def get_diff_from_base(base_sha: str, target_ref: str, folder_path: str) -> str:
    """Get diff from a base commit to a target ref, filtered by folder."""
    cmd = ["git", "diff", f"{base_sha}..{target_ref}"]
    
    if folder_path and folder_path != ".":
        cmd.append("--")
        cmd.append(folder_path)
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"⚠ Warning: Failed to get diff: {stderr}")
        return ""
    
    return stdout


def get_branch_diff(target_branch: str, folder_path: str) -> str:
    """Get diff between target branch and current HEAD, filtered by folder."""
    # Try target branch directly first, then origin/target_branch
    branch_ref = target_branch
    cmd = ["git", "rev-parse", "--verify", target_branch]
    code, _, _ = run_command(cmd)
    if code != 0:
        branch_ref = f"origin/{target_branch}"
    
    cmd = ["git", "diff", f"{branch_ref}..HEAD"]
    
    if folder_path and folder_path != ".":
        cmd.append("--")
        cmd.append(folder_path)
    
    code, stdout, stderr = run_command(cmd)
    if code != 0:
        print(f"⚠ Warning: Failed to get branch diff: {stderr}")
        return ""
    
    return stdout


# =============================================================================
# Diff Saving Functions
# =============================================================================

def save_my_branch_diff(diff_content: str, output_dir: str):
    """Save current branch diff to file."""
    filepath = Path(output_dir) / "my-branch.diff"
    filepath.write_text(diff_content)


def save_branch_diff(diff_content: str, output_dir: str):
    """Save branch comparison diff to file."""
    filepath = Path(output_dir) / "branch-diff.diff"
    filepath.write_text(diff_content)


def save_target_branch_diff(diff_content: str, output_dir: str):
    """Save target branch changes (from merge-base) to file."""
    filepath = Path(output_dir) / "target-branch.diff"
    filepath.write_text(diff_content)

