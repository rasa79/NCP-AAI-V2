#!/usr/bin/env python3
"""
Run unit tests for the NVIDIA RAG Certification Learning Package.

This script runs all unit tests for content validation.
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Run unit tests with pytest"""
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    unit_tests_dir = tests_dir / "unit"
    
    if not unit_tests_dir.exists():
        print(f"Error: Unit tests directory not found: {unit_tests_dir}")
        return 1
    
    # Run pytest with unit test configuration
    cmd = [
        "pytest",
        str(unit_tests_dir),
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "-s",  # Show print statements
    ]
    
    print("Running unit tests...")
    print(f"Command: {' '.join(cmd)}")
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
