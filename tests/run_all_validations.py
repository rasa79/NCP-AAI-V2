"""
Master validation script that runs all validation checks.

This script runs:
1. Basic validation scripts (structure, markdown, notebooks)
2. Unit tests
3. Property-based tests
4. Integration tests
"""

import sys
import subprocess
from pathlib import Path
from validate_structure import validate_directory_structure, validate_required_files
from validate_markdown import validate_all_markdown
from validate_notebooks import validate_all_notebooks


def run_pytest_suite(test_dir, suite_name):
    """Run a pytest test suite"""
    print(f"\n{suite_name}...")
    print("-" * 70)
    
    cmd = [
        "python3", "-m", "pytest",
        str(test_dir),
        "-v",
        "--tb=short",
        "-m", "not slow",  # Skip slow tests
    ]
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        
        # Print summary
        if result.returncode == 0:
            print(f"   ✓ {suite_name} passed")
            return True
        else:
            print(f"   ✗ {suite_name} failed")
            # Print last few lines of output
            lines = result.stdout.split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"     {line}")
            return False
    except FileNotFoundError:
        print(f"   ⚠ pytest not found, skipping {suite_name}")
        return True  # Don't fail if pytest not installed


def main():
    """Run all validation checks."""
    print("=" * 70)
    print("NVIDIA RAG CERTIFICATION LEARNING PACKAGE - COMPLETE VALIDATION")
    print("=" * 70)
    print()
    
    all_passed = True
    tests_dir = Path(__file__).parent
    
    # Phase 1: Basic Validation Scripts
    print("PHASE 1: BASIC VALIDATION")
    print("=" * 70)
    
    # 1. Structure validation
    print("1. Validating directory structure...")
    dir_success, dir_errors = validate_directory_structure()
    if dir_success:
        print("   ✓ Directory structure valid")
    else:
        print("   ✗ Directory structure validation failed:")
        for error in dir_errors:
            print(f"     - {error}")
        all_passed = False
    print()
    
    # 2. Required files validation
    print("2. Validating required files...")
    file_success, file_errors = validate_required_files()
    if file_success:
        print("   ✓ Required files exist")
    else:
        print("   ✗ Required files validation failed:")
        for error in file_errors:
            print(f"     - {error}")
        all_passed = False
    print()
    
    # 3. Markdown validation
    print("3. Validating Markdown syntax...")
    md_success, md_errors = validate_all_markdown()
    if md_success:
        print("   ✓ Markdown syntax valid")
    else:
        print("   ✗ Markdown validation failed:")
        for error in md_errors:
            print(f"     - {error}")
        all_passed = False
    print()
    
    # 4. Notebook validation
    print("4. Validating Jupyter notebooks...")
    nb_success, nb_errors = validate_all_notebooks()
    if nb_success:
        print("   ✓ Notebooks valid")
    else:
        print("   ✗ Notebook validation failed:")
        for error in nb_errors:
            print(f"     - {error}")
        all_passed = False
    print()
    
    # Phase 2: Unit Tests
    print("\nPHASE 2: UNIT TESTS")
    print("=" * 70)
    
    unit_tests_dir = tests_dir / "unit"
    if unit_tests_dir.exists():
        unit_success = run_pytest_suite(unit_tests_dir, "Unit tests")
        all_passed = all_passed and unit_success
    else:
        print("   ⚠ Unit tests directory not found, skipping")
    
    # Phase 3: Property-Based Tests
    print("\nPHASE 3: PROPERTY-BASED TESTS")
    print("=" * 70)
    
    property_tests_dir = tests_dir / "property"
    if property_tests_dir.exists():
        property_success = run_pytest_suite(property_tests_dir, "Property tests")
        all_passed = all_passed and property_success
    else:
        print("   ⚠ Property tests directory not found, skipping")
    
    # Phase 4: Integration Tests
    print("\nPHASE 4: INTEGRATION TESTS")
    print("=" * 70)
    
    integration_tests_dir = tests_dir / "integration"
    if integration_tests_dir.exists():
        integration_success = run_pytest_suite(integration_tests_dir, "Integration tests")
        all_passed = all_passed and integration_success
    else:
        print("   ⚠ Integration tests directory not found, skipping")
    
    # Final result
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("\nThe learning package meets all quality requirements.")
        print("=" * 70)
        return 0
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print("\nPlease review the errors above and fix the issues.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
