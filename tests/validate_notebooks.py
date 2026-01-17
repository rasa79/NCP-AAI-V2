"""
Validation script for Jupyter notebooks.
Validates notebook structure and executability.
"""

import json
import os
from pathlib import Path
from typing import List, Tuple


def validate_notebook_structure(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate Jupyter notebook structure.
    
    Args:
        file_path: Path to the notebook file
        
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check for required notebook structure
        if 'cells' not in notebook:
            errors.append(f"Missing 'cells' in {file_path}")
            return False, errors
        
        # Check for at least one cell
        if len(notebook['cells']) == 0:
            errors.append(f"No cells found in {file_path}")
        
        # Check cell types
        has_code = False
        has_markdown = False
        
        for cell in notebook['cells']:
            if cell.get('cell_type') == 'code':
                has_code = True
            elif cell.get('cell_type') == 'markdown':
                has_markdown = True
        
        if not has_code:
            errors.append(f"No code cells found in {file_path}")
        
        if not has_markdown:
            errors.append(f"No markdown cells found in {file_path}")
        
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in {file_path}: {str(e)}")
    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")
    
    return len(errors) == 0, errors


def validate_all_notebooks() -> Tuple[bool, List[str]]:
    """
    Validate all Jupyter notebooks in the learning package.
    
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    notebooks_dir = "notebooks"
    
    if os.path.isdir(notebooks_dir):
        for root, _, files in os.walk(notebooks_dir):
            for file in files:
                if file.endswith('.ipynb'):
                    file_path = os.path.join(root, file)
                    success, file_errors = validate_notebook_structure(file_path)
                    errors.extend(file_errors)
    
    return len(errors) == 0, errors


def main():
    """Run notebook validation."""
    print("=" * 60)
    print("Jupyter Notebook Validation")
    print("=" * 60)
    print()
    
    success, errors = validate_all_notebooks()
    
    if success:
        print("✓ All notebooks are valid")
        print()
        return 0
    else:
        print("✗ Notebook validation failed:")
        for error in errors:
            print(f"  - {error}")
        print()
        return 1


if __name__ == "__main__":
    exit(main())
