#!/usr/bin/env python3
"""
Run integration tests for the NVIDIA RAG Certification Learning Package.

This script runs all integration tests for end-to-end workflows.
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Run integration tests with pytest"""
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    integration_tests_dir = tests_dir / "integration"
    
    if not integration_tests_dir.exists():
        print(f"Error: Integration tests directory not found: {integration_tests_dir}")
        return 1
    
    # Run pytest with integration test configuration
    cmd = [
        "pytest",
        str(integration_tests_dir),
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "-s",  # Show print statements
        "-m", "not slow",  # Skip slow tests by default
    ]
    
    print("Running integration tests...")
    print(f"Command: {' '.join(cmd)}")
    print("Note: Skipping slow tests (notebook execution). Use --run-slow to include them.")
    print("-" * 80)
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("\nError: pytest not found. Please install dependencies:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
