"""
Tracking module for PR Daily Check.

Handles loading, saving, and validating tracking data for both PR and branch modes.
Tracking files persist between runs to detect changes and skip unchanged PRs/branches.
"""

import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path


def validate_pr_tracking_structure(data: dict) -> bool:
    """Validate that PR tracking data has expected structure."""
    if not isinstance(data, dict):
        return False
    if "prs" not in data or not isinstance(data.get("prs"), dict):
        return False
    # Validate PR entries have required fields
    for pr_num, pr_data in data.get("prs", {}).items():
        if not isinstance(pr_data, dict):
            return False
        if "sha" not in pr_data:
            return False
    return True


def load_pr_tracking_data(tracking_file: str) -> dict:
    """Load PR tracking data from file with corruption recovery."""
    tracking_path = Path(tracking_file)
    backup_path = Path(tracking_file + ".backup")
    empty_data = {"last_run": None, "prs": {}}
    
    # Try main file first
    if tracking_path.exists():
        try:
            with open(tracking_path, "r") as f:
                data = json.load(f)
            if validate_pr_tracking_structure(data):
                return data
            else:
                print(f"⚠ Tracking file has invalid structure, trying backup...")
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠ Tracking file corrupted ({type(e).__name__}), trying backup...")
    
    # Try backup file
    if backup_path.exists():
        try:
            with open(backup_path, "r") as f:
                data = json.load(f)
            if validate_pr_tracking_structure(data):
                print(f"✓ Recovered from backup file")
                # Restore main file from backup
                try:
                    shutil.copy(backup_path, tracking_path)
                except Exception:
                    pass  # Best effort restoration
                return data
            else:
                print(f"⚠ Backup file also has invalid structure")
        except (json.JSONDecodeError, IOError):
            print(f"⚠ Backup file also corrupted")
    
    # Both files failed or don't exist
    if tracking_path.exists() or backup_path.exists():
        print(f"⚠ Starting fresh - all PRs will be analyzed")
    
    return empty_data


def save_pr_tracking_data(tracking_data: dict, tracking_file: str):
    """Save PR tracking data to file with atomic write and backup."""
    tracking_path = Path(tracking_file)
    backup_path = Path(tracking_file + ".backup")
    tracking_path.parent.mkdir(parents=True, exist_ok=True)
    
    tracking_data["last_run"] = datetime.now().isoformat()
    
    # Create backup of existing file (if it exists and is valid)
    if tracking_path.exists():
        try:
            shutil.copy(tracking_path, backup_path)
        except Exception as e:
            print(f"⚠ Could not create backup: {e}")
    
    # Atomic write: write to temp file first, then rename
    temp_fd = None
    temp_path = None
    try:
        # Create temp file in same directory (for atomic rename)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=tracking_path.parent,
            prefix=".pr-tracking-",
            suffix=".tmp"
        )
        
        # Write to temp file
        with os.fdopen(temp_fd, "w") as f:
            temp_fd = None  # os.fdopen takes ownership
            json.dump(tracking_data, f, indent=2)
        
        # Atomic rename (on POSIX systems)
        os.replace(temp_path, tracking_path)
        temp_path = None  # Successfully moved
        
    except Exception as e:
        print(f"⚠ Error saving tracking data: {e}")
        # Clean up temp file if it still exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        raise
    finally:
        # Close temp_fd if still open (shouldn't happen, but safety)
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except Exception:
                pass


def is_pr_changed(pr_number: int, current_sha: str, tracking_data: dict) -> tuple[bool, str]:
    """
    Check if a PR has changed since last check.
    Returns (has_changed, reason).
    """
    pr_key = str(pr_number)
    
    if pr_key not in tracking_data.get("prs", {}):
        return True, "new"
    
    stored_sha = tracking_data["prs"][pr_key].get("sha", "")
    
    if stored_sha != current_sha:
        return True, "updated"
    
    return False, "unchanged"


# =============================================================================
# Branch Tracking Functions
# =============================================================================

def validate_branch_tracking_structure(data: dict) -> bool:
    """Validate that branch tracking data has expected structure."""
    if not isinstance(data, dict):
        return False
    if "branches" not in data or not isinstance(data.get("branches"), dict):
        return False
    # Validate branch entries have required fields
    for branch_name, branch_data in data.get("branches", {}).items():
        if not isinstance(branch_data, dict):
            return False
        if "target_sha" not in branch_data:
            return False
    return True


def load_branch_tracking_data(tracking_file: str) -> dict:
    """Load branch tracking data from file with corruption recovery."""
    tracking_path = Path(tracking_file)
    backup_path = Path(tracking_file + ".backup")
    empty_data = {"last_run": None, "branches": {}}
    
    # Try main file first
    if tracking_path.exists():
        try:
            with open(tracking_path, "r") as f:
                data = json.load(f)
            if validate_branch_tracking_structure(data):
                return data
            else:
                print(f"⚠ Branch tracking file has invalid structure, trying backup...")
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠ Branch tracking file corrupted ({type(e).__name__}), trying backup...")
    
    # Try backup file
    if backup_path.exists():
        try:
            with open(backup_path, "r") as f:
                data = json.load(f)
            if validate_branch_tracking_structure(data):
                print(f"✓ Recovered from backup file")
                # Restore main file from backup
                try:
                    shutil.copy(backup_path, tracking_path)
                except Exception:
                    pass  # Best effort restoration
                return data
            else:
                print(f"⚠ Backup file also has invalid structure")
        except (json.JSONDecodeError, IOError):
            print(f"⚠ Backup file also corrupted")
    
    # Both files failed or don't exist
    if tracking_path.exists() or backup_path.exists():
        print(f"⚠ Starting fresh - branch will be analyzed")
    
    return empty_data


def save_branch_tracking_data(tracking_data: dict, tracking_file: str):
    """Save branch tracking data to file with atomic write and backup."""
    tracking_path = Path(tracking_file)
    backup_path = Path(tracking_file + ".backup")
    tracking_path.parent.mkdir(parents=True, exist_ok=True)
    
    tracking_data["last_run"] = datetime.now().isoformat()
    
    # Create backup of existing file (if it exists and is valid)
    if tracking_path.exists():
        try:
            shutil.copy(tracking_path, backup_path)
        except Exception as e:
            print(f"⚠ Could not create backup: {e}")
    
    # Atomic write: write to temp file first, then rename
    temp_fd = None
    temp_path = None
    try:
        # Create temp file in same directory (for atomic rename)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=tracking_path.parent,
            prefix=".branch-tracking-",
            suffix=".tmp"
        )
        
        # Write to temp file
        with os.fdopen(temp_fd, "w") as f:
            temp_fd = None  # os.fdopen takes ownership
            json.dump(tracking_data, f, indent=2)
        
        # Atomic rename (on POSIX systems)
        os.replace(temp_path, tracking_path)
        temp_path = None  # Successfully moved
        
    except Exception as e:
        print(f"⚠ Error saving branch tracking data: {e}")
        # Clean up temp file if it still exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        raise
    finally:
        # Close temp_fd if still open (shouldn't happen, but safety)
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except Exception:
                pass


def is_branch_changed(target_branch: str, current_sha: str, folder_path: str, tracking_data: dict) -> tuple[bool, str, str]:
    """
    Check if a target branch has changed since last check.
    Returns (has_changed, reason, last_checked_date).
    
    Skips analysis if target branch SHA is unchanged (regardless of your branch changes).
    """
    # Create a unique key combining branch name and folder
    branch_key = f"{target_branch}:{folder_path}"
    
    if branch_key not in tracking_data.get("branches", {}):
        return True, "new", ""
    
    stored_data = tracking_data["branches"][branch_key]
    stored_sha = stored_data.get("target_sha", "")
    last_checked = stored_data.get("last_checked", "unknown")
    
    if stored_sha != current_sha:
        return True, "updated", last_checked
    
    return False, "unchanged", last_checked

