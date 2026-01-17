"""
Property-based tests for practice labs.

These tests validate universal properties that must hold for all labs
in the learning package.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from hypothesis import given, strategies as st, settings
import pytest


# Helper functions for lab analysis

def get_all_labs() -> List[Path]:
    """Get all lab directories from labs directory"""
    labs_dir = Path("labs")
    if not labs_dir.exists():
        return []
    
    # Find all directories that start with "lab-"
    labs = [d for d in labs_dir.iterdir() if d.is_dir() and d.name.startswith("lab-")]
    return sorted(labs)


def analyze_lab_structure(lab_path: Path) -> Dict[str, Any]:
    """Analyze lab directory structure and contents"""
    structure = {
        "path": lab_path,
        "name": lab_path.name,
        "has_readme": (lab_path / "README.md").exists(),
        "has_requirements": (lab_path / "requirements.txt").exists(),
        "has_starter_code": (lab_path / "starter-code").exists(),
        "has_solution": (lab_path / "solution").exists(),
        "has_test_data": (lab_path / "test-data").exists(),
        "has_tests": (lab_path / "tests").exists(),
        "has_rubric": (lab_path / "rubric.md").exists(),
    }
    
    # Count starter code files
    if structure["has_starter_code"]:
        starter_code_dir = lab_path / "starter-code"
        structure["starter_code_files"] = len(list(starter_code_dir.glob("**/*.py")))
    else:
        structure["starter_code_files"] = 0
    
    # Count test data files
    if structure["has_test_data"]:
        test_data_dir = lab_path / "test-data"
        structure["test_data_files"] = len(list(test_data_dir.glob("**/*.*")))
    else:
        structure["test_data_files"] = 0
    
    return structure


def parse_lab_readme(lab_path: Path) -> Dict[str, Any]:
    """Parse lab README and extract key sections"""
    readme_path = lab_path / "README.md"
    
    if not readme_path.exists():
        return {
            "exists": False,
            "sections": [],
            "has_scenario": False,
            "has_requirements": False,
            "has_success_criteria": False
        }
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except Exception as e:
        return {
            "exists": True,
            "error": str(e),
            "sections": []
        }
    
    # Extract sections (lines starting with #)
    import re
    sections = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    
    return {
        "exists": True,
        "sections": sections,
        "has_scenario": "scenario" in content,
        "has_requirements": "requirements" in content or "requirement" in content,
        "has_success_criteria": "success criteria" in content or "success criterion" in content,
        "has_setup": "setup" in content,
        "has_tasks": "task" in content or "implementation" in content,
        "has_testing": "test" in content,
        "has_rubric_ref": "rubric" in content
    }


def check_starter_code_quality(lab_path: Path) -> Dict[str, Any]:
    """Check quality of starter code"""
    starter_code_dir = lab_path / "starter-code"
    
    if not starter_code_dir.exists():
        return {
            "exists": False,
            "has_docstrings": False,
            "has_type_hints": False,
            "has_error_handling": False
        }
    
    # Find all Python files
    py_files = list(starter_code_dir.glob("**/*.py"))
    
    if not py_files:
        return {
            "exists": True,
            "has_files": False
        }
    
    # Analyze first few files for quality indicators
    has_docstrings = False
    has_type_hints = False
    has_error_handling = False
    has_todos = False
    
    for py_file in py_files[:5]:  # Check first 5 files
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '"""' in content or "'''" in content:
                has_docstrings = True
            
            if '->' in content or ': ' in content:  # Type hints
                has_type_hints = True
            
            if 'try:' in content and 'except' in content:
                has_error_handling = True
            
            if 'TODO' in content or 'YOUR CODE HERE' in content:
                has_todos = True
                
        except Exception:
            continue
    
    return {
        "exists": True,
        "has_files": True,
        "has_docstrings": has_docstrings,
        "has_type_hints": has_type_hints,
        "has_error_handling": has_error_handling,
        "has_todos": has_todos
    }


def parse_rubric(lab_path: Path) -> Dict[str, Any]:
    """Parse lab rubric"""
    rubric_path = lab_path / "rubric.md"
    
    if not rubric_path.exists():
        return {
            "exists": False
        }
    
    try:
        with open(rubric_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except Exception:
        return {
            "exists": True,
            "error": "Failed to read rubric"
        }
    
    return {
        "exists": True,
        "has_functionality": "functionality" in content,
        "has_code_quality": "code quality" in content,
        "has_performance": "performance" in content,
        "has_error_handling": "error handling" in content,
        "has_best_practices": "best practices" in content,
        "has_exam_mapping": "exam objective" in content or "exam mapping" in content
    }


# Property Tests

# Feature: nvidia-rag-certification-learning-package, Property 19: Lab Structure Completeness
@settings(max_examples=100)
@given(lab_path=st.sampled_from(get_all_labs() or [Path("labs/dummy-lab")]))
def test_property_19_lab_structure_completeness(lab_path):
    """
    Property 19: Lab Structure Completeness
    
    For any lab exercise, it SHALL include:
    - Problem statement (README)
    - Requirements
    - Success criteria
    - Starter code
    - Reference solution
    - Evaluation rubric
    
    Validates: Requirements 5.3, 5.4, 5.5, 5.6
    """
    # Skip if no labs exist yet
    if lab_path.name == "dummy-lab" or not lab_path.exists():
        pytest.skip("No labs available for testing yet")
    
    # Analyze lab structure
    structure = analyze_lab_structure(lab_path)
    
    # Check 1: README exists
    assert structure["has_readme"], \
        f"Lab {lab_path.name} missing README.md"
    
    # Check 2: README contains required sections
    readme_data = parse_lab_readme(lab_path)
    
    assert readme_data["has_scenario"], \
        f"Lab {lab_path.name} README missing scenario/problem statement"
    
    assert readme_data["has_requirements"], \
        f"Lab {lab_path.name} README missing requirements section"
    
    assert readme_data["has_success_criteria"], \
        f"Lab {lab_path.name} README missing success criteria"
    
    # Check 3: Starter code exists
    assert structure["has_starter_code"], \
        f"Lab {lab_path.name} missing starter-code directory"
    
    assert structure["starter_code_files"] > 0, \
        f"Lab {lab_path.name} starter-code directory is empty"
    
    # Check 4: Solution exists
    assert structure["has_solution"], \
        f"Lab {lab_path.name} missing solution directory"
    
    # Check 5: Test data exists (if applicable)
    # Some labs may not need test data, so this is a warning not assertion
    if not structure["has_test_data"]:
        print(f"Warning: Lab {lab_path.name} has no test-data directory")
    
    # Check 6: Rubric exists
    assert structure["has_rubric"], \
        f"Lab {lab_path.name} missing rubric.md"
    
    # Check 7: Requirements file exists
    assert structure["has_requirements"], \
        f"Lab {lab_path.name} missing requirements.txt"


# Feature: nvidia-rag-certification-learning-package, Property 20: Lab Solution Quality
@settings(max_examples=100)
@given(lab_path=st.sampled_from(get_all_labs() or [Path("labs/dummy-lab")]))
def test_property_20_lab_solution_quality(lab_path):
    """
    Property 20: Lab Solution Quality
    
    For any lab exercise reference solution, it SHALL:
    - Include error handling code (try-except blocks)
    - Execute successfully
    - Include comprehensive documentation
    
    Validates: Requirements 5.5, 5.8
    """
    # Skip if no labs exist yet
    if lab_path.name == "dummy-lab" or not lab_path.exists():
        pytest.skip("No labs available for testing yet")
    
    solution_dir = lab_path / "solution"
    
    # Check solution directory exists
    assert solution_dir.exists(), \
        f"Lab {lab_path.name} missing solution directory"
    
    # Find Python files in solution
    py_files = list(solution_dir.glob("**/*.py"))
    
    # Check 1: Solution has Python files
    assert len(py_files) > 0, \
        f"Lab {lab_path.name} solution directory has no Python files"
    
    # Check 2: Analyze solution code quality
    has_error_handling = False
    has_docstrings = False
    has_type_hints = False
    syntax_errors = []
    
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for error handling
            if 'try:' in content and 'except' in content:
                has_error_handling = True
            
            # Check for docstrings
            if '"""' in content or "'''" in content:
                has_docstrings = True
            
            # Check for type hints
            if '->' in content or ': str' in content or ': int' in content:
                has_type_hints = True
            
            # Check syntax
            try:
                compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file.name}: {e}")
                
        except Exception as e:
            print(f"Warning: Could not analyze {py_file}: {e}")
            continue
    
    # Assertions
    assert has_error_handling, \
        f"Lab {lab_path.name} solution lacks error handling (try-except blocks)"
    
    assert has_docstrings, \
        f"Lab {lab_path.name} solution lacks documentation (docstrings)"
    
    assert len(syntax_errors) == 0, \
        f"Lab {lab_path.name} solution has syntax errors: {syntax_errors}"
    
    # Type hints are recommended but not required
    if not has_type_hints:
        print(f"Warning: Lab {lab_path.name} solution could benefit from type hints")


# Additional property test for starter code quality
@settings(max_examples=100)
@given(lab_path=st.sampled_from(get_all_labs() or [Path("labs/dummy-lab")]))
def test_lab_starter_code_quality(lab_path):
    """
    Validate that starter code provides appropriate scaffolding.
    
    Starter code should:
    - Include docstrings explaining what to implement
    - Include TODO comments or placeholders
    - Include error handling templates
    - Have valid Python syntax
    """
    # Skip if no labs exist yet
    if lab_path.name == "dummy-lab" or not lab_path.exists():
        pytest.skip("No labs available for testing yet")
    
    # Analyze starter code
    starter_quality = check_starter_code_quality(lab_path)
    
    assert starter_quality["exists"], \
        f"Lab {lab_path.name} missing starter-code directory"
    
    assert starter_quality["has_files"], \
        f"Lab {lab_path.name} starter-code directory has no Python files"
    
    assert starter_quality["has_docstrings"], \
        f"Lab {lab_path.name} starter code lacks docstrings"
    
    assert starter_quality["has_todos"], \
        f"Lab {lab_path.name} starter code lacks TODO comments or implementation guidance"


# Additional property test for rubric completeness
@settings(max_examples=100)
@given(lab_path=st.sampled_from(get_all_labs() or [Path("labs/dummy-lab")]))
def test_lab_rubric_completeness(lab_path):
    """
    Validate that rubric covers all evaluation dimensions.
    
    Rubric should include:
    - Functionality criteria
    - Code quality criteria
    - Performance criteria
    - Error handling criteria
    - Best practices criteria
    - Exam objective mapping
    """
    # Skip if no labs exist yet
    if lab_path.name == "dummy-lab" or not lab_path.exists():
        pytest.skip("No labs available for testing yet")
    
    # Parse rubric
    rubric_data = parse_rubric(lab_path)
    
    assert rubric_data["exists"], \
        f"Lab {lab_path.name} missing rubric.md"
    
    assert rubric_data["has_functionality"], \
        f"Lab {lab_path.name} rubric missing functionality criteria"
    
    assert rubric_data["has_code_quality"], \
        f"Lab {lab_path.name} rubric missing code quality criteria"
    
    assert rubric_data["has_performance"], \
        f"Lab {lab_path.name} rubric missing performance criteria"
    
    assert rubric_data["has_error_handling"], \
        f"Lab {lab_path.name} rubric missing error handling criteria"
    
    assert rubric_data["has_best_practices"], \
        f"Lab {lab_path.name} rubric missing best practices criteria"
    
    assert rubric_data["has_exam_mapping"], \
        f"Lab {lab_path.name} rubric missing exam objective mapping"


# Feature: nvidia-rag-certification-learning-package, Property 18: Lab Complexity Progression
def test_property_18_lab_complexity_progression():
    """
    Property 18: Lab Complexity Progression
    
    For any sequence of lab exercises ordered by lab number, the complexity level
    SHALL be monotonically non-decreasing (beginner ≤ intermediate ≤ advanced).
    
    Validates: Requirements 5.2
    """
    labs = get_all_labs()
    
    # Skip if no labs exist yet
    if not labs:
        pytest.skip("No labs available for testing yet")
    
    # Define complexity mapping
    complexity_order = {
        "beginner": 1,
        "intermediate": 2,
        "intermediate-advanced": 2.5,
        "advanced": 3
    }
    
    # Extract complexity from each lab's README
    lab_complexities = []
    
    for lab_path in labs:
        readme_path = lab_path / "README.md"
        
        if not readme_path.exists():
            print(f"Warning: {lab_path.name} missing README.md")
            continue
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Look for complexity indicators in README
            # Common patterns: "Complexity: Beginner", "intermediate lab", etc.
            complexity = None
            
            # Check for explicit complexity statement
            import re
            complexity_match = re.search(r'complexity:\s*(beginner|intermediate|intermediate-advanced|advanced)', content)
            if complexity_match:
                complexity = complexity_match.group(1)
            
            # Check for complexity in overview or description
            if not complexity:
                # Check intermediate-advanced FIRST (before advanced)
                if 'intermediate-advanced' in content:
                    complexity = 'intermediate-advanced'
                elif 'advanced lab' in content or 'this advanced lab' in content:
                    complexity = 'advanced'
                elif 'intermediate lab' in content or 'this intermediate lab' in content:
                    complexity = 'intermediate'
                elif 'beginner lab' in content or 'foundational lab' in content or 'basic lab' in content:
                    complexity = 'beginner'
            
            # Check estimated time as a proxy (longer time often means more complex)
            time_match = re.search(r'estimated time:\s*(\d+)-(\d+)\s*hours', content)
            if time_match and not complexity:
                avg_hours = (int(time_match.group(1)) + int(time_match.group(2))) / 2
                if avg_hours <= 3:
                    complexity = 'beginner'
                elif avg_hours <= 4.5:
                    complexity = 'intermediate'
                else:
                    complexity = 'advanced'
            
            if complexity:
                lab_complexities.append({
                    'lab': lab_path.name,
                    'complexity': complexity,
                    'order': complexity_order.get(complexity, 2)
                })
            else:
                print(f"Warning: Could not determine complexity for {lab_path.name}")
                
        except Exception as e:
            print(f"Warning: Error analyzing {lab_path.name}: {e}")
            continue
    
    # Check monotonic non-decreasing property
    if len(lab_complexities) < 2:
        pytest.skip("Need at least 2 labs to test complexity progression")
    
    # Verify complexity is non-decreasing
    for i in range(len(lab_complexities) - 1):
        current = lab_complexities[i]
        next_lab = lab_complexities[i + 1]
        
        assert current['order'] <= next_lab['order'], \
            f"Lab complexity progression violated: {current['lab']} ({current['complexity']}) " \
            f"should not be more complex than {next_lab['lab']} ({next_lab['complexity']}). " \
            f"Expected monotonically non-decreasing complexity."
    
    # Print progression for verification
    print("\nLab Complexity Progression:")
    for lab_data in lab_complexities:
        print(f"  {lab_data['lab']}: {lab_data['complexity']}")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
