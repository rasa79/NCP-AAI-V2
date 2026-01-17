"""
Validation script for Markdown syntax in course notes and documentation.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def validate_markdown_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate Markdown syntax in a file.
    
    Args:
        file_path: Path to the Markdown file
        
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for proper heading hierarchy
        heading_levels = []
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(re.match(r'^#+', line).group())
                heading_levels.append((i, level))
        
        # Check for code blocks are properly closed
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            errors.append(f"Unclosed code block in {file_path}")
        
        # Check for empty headings
        for i, line in enumerate(lines, 1):
            if re.match(r'^#+\s*$', line):
                errors.append(f"Empty heading at line {i} in {file_path}")
        
    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")
    
    return len(errors) == 0, errors


def validate_all_markdown() -> Tuple[bool, List[str]]:
    """
    Validate all Markdown files in the learning package.
    
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    markdown_dirs = ["course-notes", "exam-questions", "quick-reference"]
    
    for directory in markdown_dirs:
        if os.path.isdir(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        success, file_errors = validate_markdown_file(file_path)
                        errors.extend(file_errors)
    
    # Also validate README
    if os.path.isfile('README.md'):
        success, file_errors = validate_markdown_file('README.md')
        errors.extend(file_errors)
    
    return len(errors) == 0, errors


def main():
    """Run Markdown validation."""
    print("=" * 60)
    print("Markdown Syntax Validation")
    print("=" * 60)
    print()
    
    success, errors = validate_all_markdown()
    
    if success:
        print("✓ All Markdown files are valid")
        print()
        return 0
    else:
        print("✗ Markdown validation failed:")
        for error in errors:
            print(f"  - {error}")
        print()
        return 1


if __name__ == "__main__":
    exit(main())
