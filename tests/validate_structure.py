"""
Validation script for learning package structure.
Validates that all required directories and files exist.
"""

import os
from pathlib import Path
from typing import List, Tuple


def validate_directory_structure() -> Tuple[bool, List[str]]:
    """
    Validate that all required directories exist.
    
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    required_dirs = [
        "course-notes",
        "notebooks",
        "notebooks/setup",
        "exam-questions",
        "quick-reference",
        "labs",
        "tests",
    ]
    
    # Add module directories
    for i in range(1, 11):
        required_dirs.append(f"notebooks/module-{i:02d}")
    
    # Add lab directories
    lab_names = [
        "lab-01-basic-rag-agent",
        "lab-02-multi-agent-research",
        "lab-03-production-deployment",
        "lab-04-evaluation-optimization",
        "lab-05-safe-compliant-agent",
    ]
    for lab in lab_names:
        required_dirs.append(f"labs/{lab}")
    
    for directory in required_dirs:
        if not os.path.isdir(directory):
            errors.append(f"Missing directory: {directory}")
    
    return len(errors) == 0, errors


def validate_required_files() -> Tuple[bool, List[str]]:
    """
    Validate that required files exist.
    
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    required_files = [
        "requirements.txt",
        "README.md",
    ]
    
    for file_path in required_files:
        if not os.path.isfile(file_path):
            errors.append(f"Missing file: {file_path}")
    
    return len(errors) == 0, errors


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("NVIDIA RAG Certification Learning Package - Structure Validation")
    print("=" * 60)
    print()
    
    # Validate directory structure
    print("Validating directory structure...")
    dir_success, dir_errors = validate_directory_structure()
    if dir_success:
        print("✓ All required directories exist")
    else:
        print("✗ Directory structure validation failed:")
        for error in dir_errors:
            print(f"  - {error}")
    print()
    
    # Validate required files
    print("Validating required files...")
    file_success, file_errors = validate_required_files()
    if file_success:
        print("✓ All required files exist")
    else:
        print("✗ File validation failed:")
        for error in file_errors:
            print(f"  - {error}")
    print()
    
    # Overall result
    if dir_success and file_success:
        print("=" * 60)
        print("✓ VALIDATION PASSED")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("✗ VALIDATION FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
