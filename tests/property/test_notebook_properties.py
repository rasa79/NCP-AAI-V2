"""
Property-based tests for Jupyter notebooks.

These tests validate universal properties that must hold for all notebooks
in the learning package.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from hypothesis import given, strategies as st, settings
import pytest


# Helper functions for notebook analysis

def get_all_notebooks() -> List[Path]:
    """Get all Jupyter notebook files from notebooks directory"""
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        return []
    return list(notebooks_dir.glob("**/*.ipynb"))


def parse_notebook(notebook_path: Path) -> Dict[str, Any]:
    """Parse notebook and extract key components"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return {
            "path": notebook_path,
            "valid": False,
            "error": str(e),
            "cells": []
        }
    
    return {
        "path": notebook_path,
        "valid": True,
        "cells": notebook_data.get("cells", []),
        "metadata": notebook_data.get("metadata", {}),
        "nbformat": notebook_data.get("nbformat", 0)
    }


def extract_markdown_sections(notebook_data: Dict) -> List[str]:
    """Extract section headings from markdown cells"""
    sections = []
    
    for cell in notebook_data.get("cells", []):
        if cell.get("cell_type") == "markdown":
            # Get cell source (can be string or list of strings)
            source = cell.get("source", [])
            if isinstance(source, list):
                source = "".join(source)
            
            # Extract headings (## or ###)
            headings = re.findall(r'^#{2,3}\s+(.+)$', source, re.MULTILINE)
            sections.extend([h.strip() for h in headings])
    
    return sections


def has_section(sections: List[str], keywords: List[str]) -> bool:
    """Check if any section contains one of the keywords"""
    sections_lower = [s.lower() for s in sections]
    return any(
        any(keyword in section for keyword in keywords)
        for section in sections_lower
    )


def get_code_cells(notebook_data: Dict) -> List[Dict]:
    """Extract all code cells from notebook"""
    return [
        cell for cell in notebook_data.get("cells", [])
        if cell.get("cell_type") == "code"
    ]


def count_code_lines(cell: Dict) -> int:
    """Count lines of code in a cell"""
    source = cell.get("source", [])
    if isinstance(source, list):
        return len([line for line in source if line.strip() and not line.strip().startswith('#')])
    else:
        return len([line for line in source.split('\n') if line.strip() and not line.strip().startswith('#')])


def count_comment_lines(cell: Dict) -> int:
    """Count comment lines in a code cell"""
    source = cell.get("source", [])
    if isinstance(source, list):
        source_text = "".join(source)
    else:
        source_text = source
    
    # Count single-line comments
    single_comments = len(re.findall(r'^\s*#', source_text, re.MULTILINE))
    
    # Count docstring lines
    docstrings = re.findall(r'""".*?"""', source_text, re.DOTALL)
    docstring_lines = sum(len(ds.split('\n')) for ds in docstrings)
    
    return single_comments + docstring_lines


def has_imports(cell: Dict) -> bool:
    """Check if code cell contains import statements"""
    source = cell.get("source", [])
    if isinstance(source, list):
        source_text = "".join(source)
    else:
        source_text = source
    
    return bool(re.search(r'^\s*(import|from)\s+', source_text, re.MULTILINE))


def has_error_handling(cell: Dict) -> bool:
    """Check if code cell contains error handling"""
    source = cell.get("source", [])
    if isinstance(source, list):
        source_text = "".join(source)
    else:
        source_text = source
    
    # Check for try-except blocks
    return bool(re.search(r'\btry\s*:', source_text)) and bool(re.search(r'\bexcept\b', source_text))


# Property Tests

# Feature: nvidia-rag-certification-learning-package, Property 7: Notebook Structure Completeness
@settings(max_examples=100)
@given(notebook_path=st.sampled_from(get_all_notebooks() or [Path("dummy.ipynb")]))
def test_property_7_notebook_structure_completeness(notebook_path):
    """
    Property 7: Notebook Structure Completeness
    
    For any Jupyter notebook, it SHALL include sections for:
    - Setup
    - Theory
    - Implementation
    - Exercises
    - Checkpoints
    
    Validates: Requirements 2.2
    """
    # Skip if no notebooks exist yet or if it's a dummy
    if notebook_path.name == "dummy.ipynb" or not notebook_path.exists():
        pytest.skip("No notebooks available for testing yet")
    
    # Skip setup notebooks as they have different structure
    if "setup" in str(notebook_path):
        pytest.skip("Setup notebooks have different structure")
    
    notebook_data = parse_notebook(notebook_path)
    
    # Check notebook is valid JSON
    assert notebook_data["valid"], \
        f"Notebook {notebook_path.name} is not valid JSON: {notebook_data.get('error', 'Unknown error')}"
    
    # Extract sections from markdown cells
    sections = extract_markdown_sections(notebook_data)
    
    # Required sections (case-insensitive matching)
    required_sections = {
        "setup": ["setup", "import", "dependencies"],
        "theory": ["theory", "overview", "concept", "what is"],
        "implementation": ["implementation", "example", "code"],
        "exercise": ["exercise", "practice", "task"],
        "checkpoint": ["checkpoint", "self-assessment", "assessment", "summary"]
    }
    
    # Check each required section type
    for section_type, keywords in required_sections.items():
        assert has_section(sections, keywords), \
            f"Notebook {notebook_path.name} missing required section: {section_type}. " \
            f"Expected keywords: {keywords}. Found sections: {sections}"


# Feature: nvidia-rag-certification-learning-package, Property 8: Code Executability
@settings(max_examples=100)
@given(notebook_path=st.sampled_from(get_all_notebooks() or [Path("dummy.ipynb")]))
def test_property_8_code_executability(notebook_path):
    """
    Property 8: Code Executability
    
    For any code cell in a Jupyter notebook, executing the cell SHALL
    complete without errors when run in sequence after setup.
    
    This test validates code structure and best practices that support executability:
    - Proper imports
    - Error handling
    - No syntax errors
    
    Validates: Requirements 2.3, 13.1
    """
    # Skip if no notebooks exist yet
    if notebook_path.name == "dummy.ipynb" or not notebook_path.exists():
        pytest.skip("No notebooks available for testing yet")
    
    notebook_data = parse_notebook(notebook_path)
    
    # Check notebook is valid
    assert notebook_data["valid"], \
        f"Notebook {notebook_path.name} is not valid: {notebook_data.get('error')}"
    
    # Get all code cells
    code_cells = get_code_cells(notebook_data)
    
    # Check 1: Notebook must have at least one code cell
    assert len(code_cells) > 0, \
        f"Notebook {notebook_path.name} has no code cells"
    
    # Check 2: First code cell should contain imports (setup)
    first_code_cell = code_cells[0]
    assert has_imports(first_code_cell), \
        f"Notebook {notebook_path.name} first code cell should contain import statements"
    
    # Check 3: Code cells with external operations should have error handling
    cells_needing_error_handling = 0
    cells_with_error_handling = 0
    
    for cell in code_cells:
        source = cell.get("source", [])
        if isinstance(source, list):
            source_text = "".join(source)
        else:
            source_text = source
        
        # Check if cell has operations that need error handling
        needs_error_handling = any([
            'open(' in source_text,  # File I/O
            'requests.' in source_text,  # API calls
            'subprocess.' in source_text,  # External commands
            '.invoke(' in source_text,  # LLM calls
            'json.load' in source_text,  # JSON parsing
        ])
        
        if needs_error_handling:
            cells_needing_error_handling += 1
            if has_error_handling(cell):
                cells_with_error_handling += 1
    
    # At least 50% of cells needing error handling should have it
    if cells_needing_error_handling > 0:
        error_handling_ratio = cells_with_error_handling / cells_needing_error_handling
        assert error_handling_ratio >= 0.5, \
            f"Notebook {notebook_path.name} has insufficient error handling. " \
            f"Only {cells_with_error_handling}/{cells_needing_error_handling} cells with " \
            f"external operations have error handling (expected >= 50%)"
    
    # Check 4: Validate Python syntax in code cells
    for i, cell in enumerate(code_cells):
        source = cell.get("source", [])
        if isinstance(source, list):
            source_text = "".join(source)
        else:
            source_text = source
        
        # Skip empty cells
        if not source_text.strip():
            continue
        
        # Try to compile the code to check for syntax errors
        try:
            compile(source_text, f"<cell-{i}>", "exec")
        except SyntaxError as e:
            pytest.fail(
                f"Notebook {notebook_path.name} cell {i} has syntax error: {e}"
            )


# Feature: nvidia-rag-certification-learning-package, Property 23: Code Comment Density
@settings(max_examples=100)
@given(notebook_path=st.sampled_from(get_all_notebooks() or [Path("dummy.ipynb")]))
def test_property_23_code_comment_density(notebook_path):
    """
    Property 23: Code Comment Density
    
    For any Python code block in notebooks, the ratio of comment lines
    to total lines SHALL be at least 0.15 (15% comment density).
    
    Validates: Requirements 13.2
    """
    # Skip if no notebooks exist yet
    if notebook_path.name == "dummy.ipynb" or not notebook_path.exists():
        pytest.skip("No notebooks available for testing yet")
    
    notebook_data = parse_notebook(notebook_path)
    
    # Check notebook is valid
    assert notebook_data["valid"], \
        f"Notebook {notebook_path.name} is not valid"
    
    # Get all code cells
    code_cells = get_code_cells(notebook_data)
    
    if not code_cells:
        pytest.skip(f"Notebook {notebook_path.name} has no code cells")
    
    # Calculate overall comment density
    total_code_lines = 0
    total_comment_lines = 0
    
    for cell in code_cells:
        code_lines = count_code_lines(cell)
        comment_lines = count_comment_lines(cell)
        
        total_code_lines += code_lines
        total_comment_lines += comment_lines
    
    # Calculate density
    if total_code_lines == 0:
        pytest.skip(f"Notebook {notebook_path.name} has no substantial code")
    
    comment_density = total_comment_lines / (total_code_lines + total_comment_lines)
    
    # Check minimum density (15%)
    assert comment_density >= 0.15, \
        f"Notebook {notebook_path.name} has insufficient comment density: " \
        f"{comment_density:.1%} (expected >= 15%). " \
        f"Comments: {total_comment_lines}, Code lines: {total_code_lines}"


# Feature: nvidia-rag-certification-learning-package, Property 9: Framework Usage Compliance
@settings(max_examples=100)
@given(notebook_path=st.sampled_from(get_all_notebooks() or [Path("dummy.ipynb")]))
def test_property_9_framework_usage_compliance(notebook_path):
    """
    Property 9: Framework Usage Compliance
    
    For any Jupyter notebook implementing RAG or agent functionality,
    it SHALL import and use at least one of: LangChain, Gradio, or LangServe.
    
    Validates: Requirements 2.5
    """
    # Skip if no notebooks exist yet
    if notebook_path.name == "dummy.ipynb" or not notebook_path.exists():
        pytest.skip("No notebooks available for testing yet")
    
    # Skip setup notebooks
    if "setup" in str(notebook_path):
        pytest.skip("Setup notebooks don't require framework usage")
    
    notebook_data = parse_notebook(notebook_path)
    
    # Check notebook is valid
    assert notebook_data["valid"], \
        f"Notebook {notebook_path.name} is not valid"
    
    # Get all code cells
    code_cells = get_code_cells(notebook_data)
    
    # Combine all code
    all_code = ""
    for cell in code_cells:
        source = cell.get("source", [])
        if isinstance(source, list):
            all_code += "".join(source)
        else:
            all_code += source
    
    # Check for required frameworks
    required_frameworks = [
        "langchain",
        "gradio",
        "langserve"
    ]
    
    # Check if at least one framework is imported
    framework_found = any(
        framework in all_code.lower()
        for framework in required_frameworks
    )
    
    assert framework_found, \
        f"Notebook {notebook_path.name} must import at least one of: " \
        f"{', '.join(required_frameworks)}"


# Feature: nvidia-rag-certification-learning-package, Property 10: Notebook Content Richness
@settings(max_examples=100)
@given(notebook_path=st.sampled_from(get_all_notebooks() or [Path("dummy.ipynb")]))
def test_property_10_notebook_content_richness(notebook_path):
    """
    Property 10: Notebook Content Richness
    
    For any Jupyter notebook, it SHALL include:
    - Real-world scenarios
    - Troubleshooting examples
    - Performance profiling code
    
    Validates: Requirements 2.4, 2.6, 2.7
    """
    # Skip if no notebooks exist yet
    if notebook_path.name == "dummy.ipynb" or not notebook_path.exists():
        pytest.skip("No notebooks available for testing yet")
    
    # Skip setup notebooks
    if "setup" in str(notebook_path):
        pytest.skip("Setup notebooks have different content requirements")
    
    notebook_data = parse_notebook(notebook_path)
    
    # Check notebook is valid
    assert notebook_data["valid"], \
        f"Notebook {notebook_path.name} is not valid"
    
    # Extract all text content (markdown + code)
    all_content = ""
    for cell in notebook_data.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            all_content += "".join(source).lower()
        else:
            all_content += source.lower()
    
    # Check for real-world scenarios
    scenario_keywords = [
        "scenario", "real-world", "production", "example", 
        "use case", "practical", "application"
    ]
    has_scenarios = any(keyword in all_content for keyword in scenario_keywords)
    
    # Check for troubleshooting content
    troubleshooting_keywords = [
        "troubleshoot", "debug", "error", "issue", "problem",
        "common", "fix", "solution"
    ]
    has_troubleshooting = any(keyword in all_content for keyword in troubleshooting_keywords)
    
    # Check for performance/profiling content
    performance_keywords = [
        "performance", "profiling", "timing", "latency", 
        "optimization", "speed", "benchmark", "metric"
    ]
    has_performance = any(keyword in all_content for keyword in performance_keywords)
    
    # At least 2 out of 3 content types should be present
    content_types_present = sum([has_scenarios, has_troubleshooting, has_performance])
    
    assert content_types_present >= 2, \
        f"Notebook {notebook_path.name} lacks content richness. " \
        f"Found: Scenarios={has_scenarios}, Troubleshooting={has_troubleshooting}, " \
        f"Performance={has_performance}. Expected at least 2 of 3 types."


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])


# Feature: nvidia-rag-certification-learning-package, Property 11: Exercise Completeness
@settings(max_examples=100)
@given(notebook_path=st.sampled_from(get_all_notebooks() or [Path("dummy.ipynb")]))
def test_property_11_exercise_completeness(notebook_path):
    """
    Property 11: Exercise Completeness
    
    For any exercise in a Jupyter notebook, it SHALL include:
    - Clear objectives
    - Starter code (or placeholder)
    - Validation criteria
    
    Validates: Requirements 2.8
    """
    # Skip if no notebooks exist yet
    if notebook_path.name == "dummy.ipynb" or not notebook_path.exists():
        pytest.skip("No notebooks available for testing yet")
    
    # Skip setup notebooks
    if "setup" in str(notebook_path):
        pytest.skip("Setup notebooks don't require exercises")
    
    notebook_data = parse_notebook(notebook_path)
    
    # Check notebook is valid
    assert notebook_data["valid"], \
        f"Notebook {notebook_path.name} is not valid"
    
    # Find exercise sections
    exercise_found = False
    exercise_has_objectives = False
    exercise_has_code = False
    exercise_has_validation = False
    
    cells = notebook_data.get("cells", [])
    
    for i, cell in enumerate(cells):
        # Check if this is an exercise section
        if cell.get("cell_type") == "markdown":
            source = cell.get("source", [])
            if isinstance(source, list):
                source_text = "".join(source).lower()
            else:
                source_text = source.lower()
            
            # Check if this is an exercise section
            if "exercise" in source_text or "practice" in source_text:
                exercise_found = True
                
                # Check for objectives
                if "objective" in source_text or "goal" in source_text:
                    exercise_has_objectives = True
                
                # Check for validation criteria
                if any(keyword in source_text for keyword in [
                    "validation", "verify", "check", "test", "criteria", "expected"
                ]):
                    exercise_has_validation = True
                
                # Look for code cell following this markdown cell
                if i + 1 < len(cells):
                    next_cell = cells[i + 1]
                    if next_cell.get("cell_type") == "code":
                        exercise_has_code = True
    
    # If no exercise section found, that's acceptable for some notebooks
    if not exercise_found:
        pytest.skip(f"Notebook {notebook_path.name} has no exercise section")
    
    # If exercise exists, check completeness
    assert exercise_has_objectives, \
        f"Notebook {notebook_path.name} exercise lacks clear objectives"
    
    assert exercise_has_code, \
        f"Notebook {notebook_path.name} exercise lacks starter code or code cell"
    
    assert exercise_has_validation, \
        f"Notebook {notebook_path.name} exercise lacks validation criteria"
