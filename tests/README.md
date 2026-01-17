# NVIDIA RAG Certification Learning Package - Tests

This directory contains comprehensive validation tests for the learning package content.

## Test Structure

```
tests/
├── unit/                  # Unit tests (specific examples and edge cases)
│   ├── test_file_structure.py
│   ├── test_markdown_syntax.py
│   ├── test_python_syntax.py
│   └── test_link_validation.py
├── property/              # Property-based tests (universal properties)
│   ├── test_module_properties.py
│   ├── test_notebook_properties.py
│   ├── test_question_properties.py
│   ├── test_lab_properties.py
│   └── test_additional_properties.py
├── integration/           # Integration tests (end-to-end workflows)
│   ├── test_notebook_execution.py
│   ├── test_lab_solutions.py
│   └── test_end_to_end_learning_path.py
├── validate_*.py          # Basic validation scripts
├── run_unit_tests.py      # Unit test runner
├── run_property_tests.py  # Property test runner
├── run_integration_tests.py # Integration test runner
├── run_all_validations.py # Complete validation pipeline
└── generate_test_report.py # Test report generator
```

## Test Types

### 1. Unit Tests

Unit tests validate **specific examples, edge cases, and error conditions**:

- **File Structure Tests**: Verify all required directories and files exist
- **Markdown Syntax Tests**: Validate Markdown syntax and structure
- **Python Syntax Tests**: Check Python code compiles and has valid syntax
- **Link Validation Tests**: Verify internal links point to existing files

**Run unit tests:**
```bash
python3 tests/run_unit_tests.py
```

Or with pytest directly:
```bash
python3 -m pytest tests/unit/ -v
```

### 2. Property-Based Tests

Property tests validate **universal properties** that must hold for all content:

#### Module Properties (test_module_properties.py)
- **Property 1:** Exam Domain Coverage Completeness - All 10 exam domains represented
- **Property 2:** Content Allocation Proportionality - Content proportional to exam weights
- **Property 3:** Module Content Completeness - Includes patterns, trade-offs, best practices
- **Property 4:** Markdown Format Compliance - Valid Markdown with proper structure
- **Property 5:** NVIDIA Tool Integration - Includes NVIDIA tool examples

#### Notebook Properties (test_notebook_properties.py)
- **Property 6:** Notebook Module Coverage - Each module has notebooks
- **Property 7:** Notebook Structure Completeness - Includes setup, theory, implementation, exercises
- **Property 8:** Code Executability - Code cells compile without errors
- **Property 9:** Framework Usage Compliance - Uses LangChain, Gradio, or LangServe
- **Property 10:** Notebook Content Richness - Includes scenarios, troubleshooting, profiling
- **Property 11:** Exercise Completeness - Exercises have objectives and validation
- **Property 23:** Code Comment Density - At least 15% comment density

#### Question Properties (test_question_properties.py)
- **Property 12:** Question Quantity Threshold - At least 50 questions
- **Property 13:** Question Distribution Proportionality - Questions proportional to exam weights
- **Property 14:** Question Structure Completeness - Includes scenario, options, explanation
- **Property 15:** Question Traceability - Maps to exam objectives
- **Property 16:** Question Explanation Quality - References NVIDIA tools and trade-offs

#### Lab Properties (test_lab_properties.py)
- **Property 17:** Lab Exercise Count - Exactly 5 labs
- **Property 18:** Lab Complexity Progression - Complexity increases monotonically
- **Property 19:** Lab Structure Completeness - Includes README, starter code, solution, rubric
- **Property 20:** Lab Solution Quality - Includes error handling and documentation

#### Additional Properties (test_additional_properties.py)
- **Property 21:** Concept Explanation Richness - Includes code examples and visualizations
- **Property 22:** Demonstration Completeness - Demonstrations include working code
- **Property 24:** Code Error Handling - I/O operations include error handling
- **Property 25:** Code Style Compliance - Follows PEP 8 guidelines
- **Property 26:** Exercise Validation Presence - Exercises have validation code
- **Property 27:** Module Metadata Completeness - Includes objectives, time estimates
- **Property 28:** Content Complexity Progression - Complexity increases across modules
- **Property 29:** Cross-Reference Presence - Includes cross-references to related materials
- **Property 30:** Exam Objective Mapping Completeness - Maps to exam objectives
- **Property 31:** Domain Weight Documentation - Documents exam weights
- **Property 32:** Exam Concept Highlighting - Uses callouts and highlighting

**Configuration:**
- Minimum 100 iterations per property test (configured via Hypothesis)
- Each property test references its design document property
- Tag format: **Feature: nvidia-rag-certification-learning-package, Property {number}: {property_text}**

**Run property tests:**
```bash
python3 tests/run_property_tests.py
```

Or with pytest directly:
```bash
python3 -m pytest tests/property/ -v --hypothesis-show-statistics
```

### 3. Integration Tests

Integration tests validate **end-to-end workflows** and component interactions:

- **Notebook Execution Tests**: Verify notebooks can be executed sequentially
- **Lab Solution Tests**: Validate lab solutions execute successfully
- **End-to-End Learning Path Tests**: Verify complete learning path flows correctly

**Run integration tests:**
```bash
python3 tests/run_integration_tests.py
```

Or with pytest directly:
```bash
python3 -m pytest tests/integration/ -v -m "not slow"
```

## Running Tests

### Quick Start

Run all validations (recommended):
```bash
python3 tests/run_all_validations.py
```

This runs:
1. Basic validation scripts (structure, markdown, notebooks)
2. Unit tests
3. Property-based tests (100+ iterations each)
4. Integration tests

### Individual Test Suites

Run specific test suites:
```bash
# Unit tests only
python3 tests/run_unit_tests.py

# Property tests only
python3 tests/run_property_tests.py

# Integration tests only
python3 tests/run_integration_tests.py
```

### Using pytest Directly

Run tests with pytest for more control:
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/property/test_module_properties.py -v

# Run specific test
python3 -m pytest tests/property/test_module_properties.py::test_property_3_module_content_completeness -v

# Run with Hypothesis statistics
python3 -m pytest tests/property/ -v --hypothesis-show-statistics

# Run including slow tests (notebook execution)
python3 -m pytest tests/integration/ -v
```

### Generate Test Report

Generate a comprehensive test report:
```bash
python3 tests/generate_test_report.py
```

## Prerequisites

Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pytest >= 8.0
- hypothesis >= 6.0
- jupyter (for notebook execution tests)
- nbconvert (for notebook execution tests)

## Test Configuration

### Pytest Configuration

Tests use pytest markers:
- `@pytest.mark.slow` - Marks slow tests (notebook execution)
- `@pytest.mark.parametrize` - Parameterized tests for multiple inputs

### Hypothesis Configuration

Property tests use Hypothesis with:
- `@settings(max_examples=100)` - Minimum 100 iterations per test
- Automatic shrinking of failing examples
- Deterministic test execution (seeded)

## Interpreting Results

### Successful Test Run

```
tests/property/test_module_properties.py::test_property_3_module_content_completeness PASSED [100%]
tests/property/test_module_properties.py::test_property_4_markdown_format_compliance PASSED [100%]
tests/property/test_module_properties.py::test_property_5_nvidia_tool_integration PASSED [100%]

====== 3 passed in 2.34s ======
```

### Failed Test Run

```
tests/property/test_module_properties.py::test_property_3_module_content_completeness FAILED

AssertionError: Module module-02-agent-development.md missing best practices or recommendations
```

**Action:** Update the module to include the missing element.

### Property Test Failure

When a property test fails, Hypothesis provides a minimal failing example:

```
Falsifying example: test_property_7_notebook_structure_completeness(
    notebook_path=PosixPath('notebooks/module-01/01-agent-architectures.ipynb')
)
AssertionError: Notebook 01-agent-architectures.ipynb missing required section: exercises
```

**Action:** Add the missing section to the notebook.

## Continuous Integration

Property tests should run:
- On every commit (pre-commit hook)
- On pull requests
- Before releases
- Nightly for comprehensive validation

## Troubleshooting

### "No modules available for testing yet"

This is expected during initial setup. Tests will skip until content is created.

### "Module missing X"

Update the module content to include the missing element. Refer to the design document for requirements.

### "pytest not found"

Install pytest:
```bash
pip install pytest hypothesis
```

### Hypothesis finds edge case

If Hypothesis discovers a failing case, it will provide a minimal example. Use this to fix the issue:

1. Review the failing example
2. Understand why it fails
3. Fix the code or adjust the property
4. Re-run the test to verify

### Test timeouts

Some integration tests (notebook execution) may take time. Increase timeout:
```bash
python3 -m pytest tests/integration/ -v --timeout=600
```

## Adding New Tests

### Adding Unit Tests

1. Create test file in `tests/unit/`
2. Use pytest conventions (`test_*.py`, `Test*` classes, `test_*` methods)
3. Add descriptive docstrings
4. Run tests to verify

Example:
```python
def test_specific_requirement():
    """Test that specific requirement is met"""
    assert condition, "Failure message"
```

### Adding Property Tests

1. Add test function to appropriate file in `tests/property/`
2. Use `@given` decorator with Hypothesis strategies
3. Set `@settings(max_examples=100)` for 100+ iterations
4. Include property tag in docstring: `Property {number}: {name}`
5. Reference validated requirements in docstring

Example:
```python
from hypothesis import given, strategies as st, settings

@settings(max_examples=100)
@given(module_path=st.sampled_from(get_all_modules()))
def test_property_X_description(module_path):
    """
    Property X: Description
    
    For any module, it SHALL meet condition.
    
    Validates: Requirements X.Y
    """
    # Test implementation
    assert condition, "Failure message"
```

### Adding Integration Tests

1. Create test file in `tests/integration/`
2. Test end-to-end workflows
3. Use `@pytest.mark.slow` for long-running tests
4. Include setup and teardown as needed

## Test Coverage Goals

- **Code Coverage:** 90%+ for validation scripts
- **Property Coverage:** 100% of properties tested (32 properties)
- **Content Coverage:** 100% of modules, notebooks, questions, labs validated
- **Execution Coverage:** 100% of code examples executable

## References

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- Design Document: `.kiro/specs/nvidia-rag-certification-learning-package/design.md`
- Requirements Document: `.kiro/specs/nvidia-rag-certification-learning-package/requirements.md`

## Test Results Summary

Current test status:
- ✓ Basic validation scripts: PASSING
- ⚠ Unit tests: Some failures (expected during development)
- ⚠ Property tests: Some failures (expected during development)
- ⚠ Integration tests: Some failures (expected during development)

The test infrastructure is complete and functional. Test failures indicate areas where content needs to be updated to meet requirements.
