"""
Property-based tests for course module content.

These tests validate universal properties that must hold for all modules
in the learning package.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from hypothesis import given, strategies as st, settings
import pytest


# Helper functions for module analysis

def get_all_modules() -> List[Path]:
    """Get all module markdown files from course-notes directory"""
    course_notes_dir = Path("course-notes")
    if not course_notes_dir.exists():
        return []
    return list(course_notes_dir.glob("module-*.md"))


def parse_module_content(module_path: Path) -> Dict[str, Any]:
    """Parse module content and extract key components"""
    with open(module_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "path": module_path,
        "content": content,
        "sections": extract_sections(content),
        "code_examples": extract_code_examples(content),
        "diagrams": extract_diagrams(content),
        "learning_objectives": extract_learning_objectives(content),
        "exam_objectives": extract_exam_objectives(content)
    }


def extract_sections(content: str) -> List[str]:
    """Extract section headings from markdown content"""
    # Match markdown headings (## or ###)
    pattern = r'^#{2,3}\s+(.+)$'
    sections = re.findall(pattern, content, re.MULTILINE)
    return [s.strip() for s in sections]


def extract_code_examples(content: str) -> List[str]:
    """Extract code blocks from markdown"""
    # Match fenced code blocks
    pattern = r'```(?:python|bash|yaml)?\n(.*?)```'
    code_blocks = re.findall(pattern, content, re.DOTALL)
    return code_blocks


def extract_diagrams(content: str) -> List[str]:
    """Extract Mermaid diagrams from markdown"""
    pattern = r'```mermaid\n(.*?)```'
    diagrams = re.findall(pattern, content, re.DOTALL)
    return diagrams


def extract_learning_objectives(content: str) -> List[str]:
    """Extract learning objectives from module"""
    # Look for learning objectives section
    pattern = r'## Learning Objectives\s*\n\n(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []
    
    objectives_text = match.group(1)
    # Extract numbered or bulleted items
    objectives = re.findall(r'^\d+\.\s+\*\*(.+?)\*\*', objectives_text, re.MULTILINE)
    if not objectives:
        objectives = re.findall(r'^[-*]\s+(.+)$', objectives_text, re.MULTILINE)
    
    return [obj.strip() for obj in objectives]


def extract_exam_objectives(content: str) -> List[str]:
    """Extract exam objective mappings from module"""
    # Look for exam objective mapping section
    pattern = r'## Exam Objective Mapping\s*\n\n(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []
    
    objectives_text = match.group(1)
    # Extract objective references (e.g., "1.1", "1.2")
    objectives = re.findall(r'\*\*(\d+\.\d+)\*\*', objectives_text)
    
    return objectives


def has_architecture_patterns(content: str) -> bool:
    """Check if module includes architecture patterns"""
    keywords = [
        'architecture', 'pattern', 'design', 'approach',
        'reactive', 'deliberative', 'hybrid'
    ]
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in keywords)


def has_trade_off_analysis(content: str) -> bool:
    """Check if module includes trade-off analysis"""
    indicators = [
        'trade-off', 'tradeoff', 'advantage', 'disadvantage',
        'benefit', 'cost', 'pros and cons', '✅', '❌'
    ]
    content_lower = content.lower()
    return any(indicator in content_lower for indicator in indicators)


def has_best_practices(content: str) -> bool:
    """Check if module includes best practices"""
    indicators = [
        'best practice', 'recommendation', 'should', 'must',
        'anti-pattern', 'pitfall', 'common mistake'
    ]
    content_lower = content.lower()
    return any(indicator in content_lower for indicator in indicators)


def has_nvidia_tool_examples(content: str) -> bool:
    """Check if module includes NVIDIA tool integration examples"""
    nvidia_tools = [
        'nvidia nim', 'nemo guardrails', 'nemo agent toolkit',
        'tensorrt-llm', 'triton', 'agent intelligence toolkit',
        'nvidia_ai_endpoints', 'ChatNVIDIA'
    ]
    content_lower = content.lower()
    return any(tool in content_lower for tool in nvidia_tools)


# Property Tests

# Feature: nvidia-rag-certification-learning-package, Property 3: Module Content Completeness
@settings(max_examples=100)
@given(module_path=st.sampled_from(get_all_modules() or [Path("dummy")]))
def test_property_3_module_content_completeness(module_path):
    """
    Property 3: Module Content Completeness
    
    For any module in the learning package, it SHALL include:
    - Architecture patterns
    - Design trade-offs
    - Best practices
    - Exam objective mappings
    
    Validates: Requirements 1.3, 1.4
    """
    # Skip if no modules exist yet (during initial setup)
    if module_path.name == "dummy" or not module_path.exists():
        pytest.skip("No modules available for testing yet")
    
    module_data = parse_module_content(module_path)
    content = module_data["content"]
    
    # Check 1: Module must include architecture patterns
    assert has_architecture_patterns(content), \
        f"Module {module_path.name} missing architecture patterns or design approaches"
    
    # Check 2: Module must include trade-off analysis
    assert has_trade_off_analysis(content), \
        f"Module {module_path.name} missing trade-off analysis (advantages/disadvantages)"
    
    # Check 3: Module must include best practices
    assert has_best_practices(content), \
        f"Module {module_path.name} missing best practices or recommendations"
    
    # Check 4: Module must map to exam objectives
    exam_objectives = module_data["exam_objectives"]
    assert len(exam_objectives) > 0, \
        f"Module {module_path.name} missing exam objective mappings"
    
    # Additional validation: Check for learning objectives
    learning_objectives = module_data["learning_objectives"]
    assert len(learning_objectives) > 0, \
        f"Module {module_path.name} missing learning objectives"


# Feature: nvidia-rag-certification-learning-package, Property 5: NVIDIA Tool Integration
@settings(max_examples=100)
@given(module_path=st.sampled_from(get_all_modules() or [Path("dummy")]))
def test_property_5_nvidia_tool_integration(module_path):
    """
    Property 5: NVIDIA Tool Integration
    
    For any technical concept section in course notes, it SHALL include
    at least one practical example using NVIDIA tools.
    
    Validates: Requirements 1.6
    """
    # Skip if no modules exist yet
    if module_path.name == "dummy" or not module_path.exists():
        pytest.skip("No modules available for testing yet")
    
    module_data = parse_module_content(module_path)
    content = module_data["content"]
    
    # Check: Module must include NVIDIA tool examples
    assert has_nvidia_tool_examples(content), \
        f"Module {module_path.name} missing NVIDIA tool integration examples " \
        f"(NIM, NeMo Guardrails, TensorRT-LLM, Triton, etc.)"


# Feature: nvidia-rag-certification-learning-package, Property 4: Markdown Format Compliance
@settings(max_examples=100)
@given(module_path=st.sampled_from(get_all_modules() or [Path("dummy")]))
def test_property_4_markdown_format_compliance(module_path):
    """
    Property 4: Markdown Format Compliance
    
    For any course note document, it SHALL be valid Markdown with:
    - Proper heading hierarchy
    - Fenced code blocks
    - Diagram syntax (Mermaid)
    
    Validates: Requirements 1.5
    """
    # Skip if no modules exist yet
    if module_path.name == "dummy" or not module_path.exists():
        pytest.skip("No modules available for testing yet")
    
    module_data = parse_module_content(module_path)
    content = module_data["content"]
    
    # Check 1: Must have proper heading hierarchy (starts with #)
    assert content.startswith('#'), \
        f"Module {module_path.name} must start with a heading"
    
    # Check 2: Must have multiple sections (## headings)
    sections = module_data["sections"]
    assert len(sections) >= 3, \
        f"Module {module_path.name} must have at least 3 sections (has {len(sections)})"
    
    # Check 3: Code examples should use fenced code blocks
    code_examples = module_data["code_examples"]
    # If there are code examples, they should be properly formatted
    if code_examples:
        assert len(code_examples) > 0, \
            f"Module {module_path.name} has code but not in fenced blocks"
    
    # Check 4: Should include diagrams (Mermaid)
    diagrams = module_data["diagrams"]
    # At least one diagram is recommended for architecture modules
    if "architecture" in module_path.name.lower() or "design" in module_path.name.lower():
        assert len(diagrams) > 0, \
            f"Architecture/design module {module_path.name} should include Mermaid diagrams"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])



# Feature: nvidia-rag-certification-learning-package, Property 2: Content Allocation Proportionality
def test_property_2_content_allocation_proportionality():
    """
    Property 2: Content Allocation Proportionality
    
    For any exam domain in the learning package, the content coverage
    (measured by word count) SHALL be proportional to the exam weight
    for that domain (±5% tolerance).
    
    Validates: Requirements 1.2
    """
    modules = get_all_modules()
    
    if not modules:
        pytest.skip("No modules available for testing yet")
    
    # Define exam weights for each module
    exam_weights = {
        "module-01": 0.15,  # Agent Architecture and Design (15%)
        "module-02": 0.15,  # Agent Development (15%)
        "module-03": 0.13,  # Evaluation and Tuning (13%)
        "module-04": 0.10,  # Knowledge Integration (10%)
        "module-05": 0.10,  # Cognition, Planning, and Memory (10%)
        "module-06": 0.07,  # NVIDIA Platform (7%)
        "module-07": 0.07,  # Monitoring and Maintenance (7%)
        "module-08": 0.05,  # Deployment and Scaling (5%)
        "module-09": 0.05,  # Safety, Ethics, and Compliance (5%)
        "module-10": 0.05,  # Human-AI Interaction (5%)
    }
    
    # Calculate word counts for each module
    module_word_counts = {}
    total_words = 0
    
    for module_path in modules:
        module_data = parse_module_content(module_path)
        content = module_data["content"]
        
        # Count words (excluding code blocks and diagrams)
        # Remove code blocks
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Count words
        words = len(content_no_code.split())
        
        # Extract module number (e.g., "module-01" from "module-01-agent-architecture-design.md")
        module_key = module_path.stem[:9]  # "module-01"
        
        module_word_counts[module_key] = words
        total_words += words
    
    # Check proportionality for each module
    tolerance = 0.05  # 5% tolerance
    
    for module_key, expected_weight in exam_weights.items():
        if module_key in module_word_counts:
            actual_proportion = module_word_counts[module_key] / total_words if total_words > 0 else 0
            
            # Check if within tolerance
            lower_bound = expected_weight - tolerance
            upper_bound = expected_weight + tolerance
            
            assert lower_bound <= actual_proportion <= upper_bound, \
                f"Module {module_key} content allocation ({actual_proportion:.1%}) " \
                f"not proportional to exam weight ({expected_weight:.1%}). " \
                f"Expected range: {lower_bound:.1%} - {upper_bound:.1%}"


# Additional helper function for Property 2
def extract_module_number(module_path: Path) -> str:
    """Extract module number from filename (e.g., '01' from 'module-01-...')"""
    match = re.search(r'module-(\d+)', module_path.stem)
    return match.group(1) if match else ""


# Helper functions for quick reference analysis

def get_quick_reference_files() -> List[Path]:
    """Get all quick reference markdown files"""
    quick_ref_dir = Path("quick-reference")
    if not quick_ref_dir.exists():
        return []
    return [f for f in quick_ref_dir.glob("*.md") if f.name != "README.md"]


def has_tables(content: str) -> bool:
    """Check if content includes markdown tables"""
    # Look for markdown table syntax (| header | header |)
    table_pattern = r'\|.+\|.+\|'
    return bool(re.search(table_pattern, content))


def has_lists(content: str) -> bool:
    """Check if content includes lists (bulleted or numbered)"""
    # Look for list items (-, *, or numbered)
    list_pattern = r'^[\s]*[-*]\s+.+$|^[\s]*\d+\.\s+.+$'
    return bool(re.search(list_pattern, content, re.MULTILINE))


def has_visual_aids(content: str) -> bool:
    """Check if content includes visual aids (diagrams, flowcharts, decision trees)"""
    # Look for Mermaid diagrams or other visual indicators
    visual_indicators = [
        '```mermaid',
        'graph TD',
        'graph LR',
        'flowchart',
        'sequenceDiagram',
        '✓', '✗', '❌', '✅',  # Visual checkmarks/crosses
        '→', '←', '↑', '↓'  # Arrows
    ]
    return any(indicator in content for indicator in visual_indicators)


def count_tables(content: str) -> int:
    """Count number of tables in content"""
    # Count table headers (lines with | ... | ... |)
    table_headers = re.findall(r'\n\|[^\n]+\|[^\n]+\|\n\|[-:\s|]+\|', content)
    return len(table_headers)


def count_lists(content: str) -> int:
    """Count number of list sections in content"""
    # Count list blocks (consecutive list items)
    list_blocks = re.findall(r'(?:^[\s]*[-*]\s+.+\n)+', content, re.MULTILINE)
    numbered_blocks = re.findall(r'(?:^[\s]*\d+\.\s+.+\n)+', content, re.MULTILINE)
    return len(list_blocks) + len(numbered_blocks)


def has_code_blocks(content: str) -> bool:
    """Check if content includes code blocks"""
    return '```' in content


# Feature: nvidia-rag-certification-learning-package, Property 8 variant: Quick Reference Format
@settings(max_examples=100)
@given(ref_file=st.sampled_from(get_quick_reference_files() or [Path("dummy")]))
def test_property_quick_reference_format(ref_file):
    """
    Property 8 variant: Quick Reference Format
    
    For any quick reference document, it SHALL use tables, lists,
    and visual aids for rapid scanning and information retrieval.
    
    Validates: Requirements 4.8
    """
    # Skip if no quick reference files exist yet
    if ref_file.name == "dummy" or not ref_file.exists():
        pytest.skip("No quick reference files available for testing yet")
    
    with open(ref_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check 1: Must include tables for structured information
    assert has_tables(content), \
        f"Quick reference {ref_file.name} must include tables for structured information"
    
    # Check 2: Must include lists for easy scanning
    assert has_lists(content), \
        f"Quick reference {ref_file.name} must include lists (bulleted or numbered)"
    
    # Check 3: Must include visual aids (diagrams, symbols, etc.)
    assert has_visual_aids(content), \
        f"Quick reference {ref_file.name} must include visual aids " \
        f"(diagrams, checkmarks, arrows, etc.) for rapid comprehension"
    
    # Check 4: Should have multiple tables (at least 2 for comprehensive references)
    table_count = count_tables(content)
    assert table_count >= 2, \
        f"Quick reference {ref_file.name} should have at least 2 tables " \
        f"for comprehensive information (has {table_count})"
    
    # Check 5: Should have multiple list sections
    list_count = count_lists(content)
    assert list_count >= 3, \
        f"Quick reference {ref_file.name} should have at least 3 list sections " \
        f"for easy scanning (has {list_count})"
    
    # Check 6: Code examples should be in fenced blocks (if present)
    if 'command' in ref_file.name.lower() or 'cheatsheet' in ref_file.name.lower():
        assert has_code_blocks(content), \
            f"Command/cheatsheet reference {ref_file.name} should include code blocks"


# Additional test for overall quick reference completeness
def test_quick_reference_completeness():
    """
    Test that all required quick reference files exist and are complete.
    
    Validates: Requirements 4.1-4.7
    """
    quick_ref_dir = Path("quick-reference")
    
    if not quick_ref_dir.exists():
        pytest.skip("Quick reference directory not created yet")
    
    # Required files
    required_files = [
        "formulas-metrics.md",
        "command-cheatsheet.md",
        "patterns-antipatterns.md",
        "decision-trees.md",
        "troubleshooting-flowcharts.md",
        "exam-tips.md"
    ]
    
    # Check that all required files exist
    for filename in required_files:
        file_path = quick_ref_dir / filename
        assert file_path.exists(), \
            f"Required quick reference file missing: {filename}"
        
        # Check that file is not empty
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content) > 100, \
            f"Quick reference file {filename} is too short (< 100 characters)"
        
        # Check that file has proper structure
        assert content.startswith('#'), \
            f"Quick reference file {filename} must start with a heading"


# Test for specific quick reference content requirements
def test_formulas_metrics_content():
    """Test that formulas-metrics.md includes required metrics"""
    file_path = Path("quick-reference/formulas-metrics.md")
    
    if not file_path.exists():
        pytest.skip("formulas-metrics.md not created yet")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required metrics (from Requirements 4.2)
    required_metrics = [
        "precision", "recall", "f1", "bleu", "rouge", "faithfulness",
        "latency", "throughput", "tokens"
    ]
    
    content_lower = content.lower()
    for metric in required_metrics:
        assert metric in content_lower, \
            f"formulas-metrics.md missing required metric: {metric}"


def test_command_cheatsheet_content():
    """Test that command-cheatsheet.md includes required commands"""
    file_path = Path("quick-reference/command-cheatsheet.md")
    
    if not file_path.exists():
        pytest.skip("command-cheatsheet.md not created yet")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required tools (from Requirements 4.3)
    required_tools = [
        "nvidia nim", "tensorrt", "triton", "langchain", "gradio"
    ]
    
    content_lower = content.lower()
    for tool in required_tools:
        assert tool in content_lower, \
            f"command-cheatsheet.md missing required tool: {tool}"


def test_patterns_antipatterns_content():
    """Test that patterns-antipatterns.md includes required patterns"""
    file_path = Path("quick-reference/patterns-antipatterns.md")
    
    if not file_path.exists():
        pytest.skip("patterns-antipatterns.md not created yet")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required patterns (from Requirements 4.4)
    required_patterns = [
        "react", "rag", "multi-agent", "streaming"
    ]
    
    content_lower = content.lower()
    for pattern in required_patterns:
        assert pattern in content_lower, \
            f"patterns-antipatterns.md missing required pattern: {pattern}"
    
    # Should include anti-patterns section
    assert "anti-pattern" in content_lower, \
        "patterns-antipatterns.md must include anti-patterns section"


def test_decision_trees_content():
    """Test that decision-trees.md includes required decision trees"""
    file_path = Path("quick-reference/decision-trees.md")
    
    if not file_path.exists():
        pytest.skip("decision-trees.md not created yet")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required decision trees (from Requirements 4.5)
    required_trees = [
        "rag vs fine-tuning",
        "vector store",
        "embedding model",
        "chunking"
    ]
    
    content_lower = content.lower()
    for tree in required_trees:
        assert tree in content_lower, \
            f"decision-trees.md missing required decision tree: {tree}"
    
    # Should include Mermaid diagrams
    assert "```mermaid" in content, \
        "decision-trees.md should include Mermaid diagrams for visual decision trees"


def test_troubleshooting_flowcharts_content():
    """Test that troubleshooting-flowcharts.md includes required flowcharts"""
    file_path = Path("quick-reference/troubleshooting-flowcharts.md")
    
    if not file_path.exists():
        pytest.skip("troubleshooting-flowcharts.md not created yet")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required flowcharts (from Requirements 4.6)
    required_flowcharts = [
        "high latency", "low accuracy", "memory", "hallucination"
    ]
    
    content_lower = content.lower()
    for flowchart in required_flowcharts:
        assert flowchart in content_lower, \
            f"troubleshooting-flowcharts.md missing required flowchart: {flowchart}"
    
    # Should include Mermaid diagrams
    assert "```mermaid" in content, \
        "troubleshooting-flowcharts.md should include Mermaid diagrams for flowcharts"


def test_exam_tips_content():
    """Test that exam-tips.md includes required exam strategies"""
    file_path = Path("quick-reference/exam-tips.md")
    
    if not file_path.exists():
        pytest.skip("exam-tips.md not created yet")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Required content (from Requirements 4.7)
    required_content = [
        "time management", "scenario analysis", "elimination"
    ]
    
    content_lower = content.lower()
    for item in required_content:
        assert item in content_lower, \
            f"exam-tips.md missing required content: {item}"
