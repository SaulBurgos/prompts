#!/usr/bin/env python3
"""
PR Daily Check Cleanup Script

Deletes all temporary files created by pr_daily_check.py.
Used by the /pr-daily-check Cursor command after report generation.

Usage:
    python3 pr_daily_check_cleanup.py
"""

import shutil
import sys
from pathlib import Path


# Configuration
OUTPUT_DIR = "tmp/daily-pr-check"


def cleanup_temp_files():
    """Delete all temporary files in the output directory."""
    output_path = Path(OUTPUT_DIR)
    
    if not output_path.exists():
        print(f"✓ No temporary files to clean (directory doesn't exist: {OUTPUT_DIR}/)")
        return True
    
    try:
        # Remove entire directory and all contents
        shutil.rmtree(output_path)
        print(f"✓ Cleaned up temporary files: {OUTPUT_DIR}/")
        return True
    except Exception as e:
        print(f"✗ Error cleaning up temporary files: {e}")
        return False


def main():
    print("Cleaning up temporary files...")
    
    success = cleanup_temp_files()
    
    if success:
        print("✓ Cleanup complete!")
        sys.exit(0)
    else:
        print("✗ Cleanup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

