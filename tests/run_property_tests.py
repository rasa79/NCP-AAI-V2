#!/usr/bin/env python3
"""
Run property-based tests for the NVIDIA RAG Certification Learning Package.

This script runs all property tests with appropriate configuration for
property-based testing (100+ iterations per test).
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Run property tests with pytest"""
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    property_tests_dir = tests_dir / "property"
    
    if not property_tests_dir.exists():
        print(f"Error: Property tests directory not found: {property_tests_dir}")
        return 1
    
    # Run pytest with property test configuration
    cmd = [
        "pytest",
        str(property_tests_dir),
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--hypothesis-show-statistics",  # Show Hypothesis statistics
        "-s",  # Show print statements
    ]
    
    print("Running property-based tests...")
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
