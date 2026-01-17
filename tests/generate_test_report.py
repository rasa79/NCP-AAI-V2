#!/usr/bin/env python3
"""
Generate a comprehensive test report for the learning package.

This script runs all tests and generates a summary report.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def run_test_suite(test_dir, suite_name):
    """Run a test suite and return results"""
    cmd = [
        "python3", "-m", "pytest",
        str(test_dir),
        "-v",
        "--tb=short",
        "-m", "not slow",
        "--quiet"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Parse output for summary
        output_lines = result.stdout.split('\n')
        summary_line = [line for line in output_lines if 'passed' in line or 'failed' in line]
        
        return {
            'name': suite_name,
            'passed': result.returncode == 0,
            'output': result.stdout,
            'summary': summary_line[-1] if summary_line else "No summary available"
        }
    except Exception as e:
        return {
            'name': suite_name,
            'passed': False,
            'output': str(e),
            'summary': f"Error running tests: {e}"
        }


def main():
    """Generate test report"""
    print("=" * 80)
    print("NVIDIA RAG CERTIFICATION LEARNING PACKAGE - TEST REPORT")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests_dir = Path(__file__).parent
    
    # Test suites to run
    suites = [
        (tests_dir / "unit", "Unit Tests"),
        (tests_dir / "property", "Property-Based Tests"),
        (tests_dir / "integration", "Integration Tests")
    ]
    
    results = []
    
    for test_dir, suite_name in suites:
        if test_dir.exists():
            print(f"\nRunning {suite_name}...")
            result = run_test_suite(test_dir, suite_name)
            results.append(result)
            print(f"  {result['summary']}")
        else:
            print(f"\n{suite_name}: Directory not found, skipping")
    
    # Generate summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    total_passed = sum(1 for r in results if r['passed'])
    total_suites = len(results)
    
    for result in results:
        status = "✓ PASSED" if result['passed'] else "✗ FAILED"
        print(f"{result['name']}: {status}")
        print(f"  {result['summary']}")
    
    print("\n" + "=" * 80)
    print(f"Overall: {total_passed}/{total_suites} test suites passed")
    print("=" * 80)
    
    return 0 if total_passed == total_suites else 1


if __name__ == "__main__":
    sys.exit(main())
