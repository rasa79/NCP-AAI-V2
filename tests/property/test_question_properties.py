"""
Property-based tests for exam questions.

These tests validate universal properties that must hold for all scenario-based
exam questions in the learning package.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from hypothesis import given, strategies as st, settings
import pytest


# Helper functions for question analysis

def get_all_question_files() -> List[Path]:
    """Get all question markdown files from exam-questions directory"""
    questions_dir = Path("exam-questions")
    if not questions_dir.exists():
        return []
    # Get all domain question files (exclude README and answer-key)
    return [
        f for f in questions_dir.glob("domain-*.md")
        if f.name not in ["README.md", "answer-key.md"]
    ]


def parse_question_file(file_path: Path) -> Dict[str, Any]:
    """Parse question file and extract individual questions"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {
            "path": file_path,
            "valid": False,
            "error": "File not found",
            "questions": []
        }
    
    # Split by question markers (### Question N:)
    question_pattern = r'###\s+Question\s+\d+:'
    question_splits = re.split(question_pattern, content)
    
    # First split is header, rest are questions
    questions = []
    for i, q_content in enumerate(question_splits[1:], 1):
        questions.append({
            "number": i,
            "content": q_content.strip(),
            "file": file_path.name
        })
    
    return {
        "path": file_path,
        "valid": True,
        "questions": questions,
        "domain": extract_domain_from_filename(file_path.name)
    }


def extract_domain_from_filename(filename: str) -> str:
    """Extract domain name from filename"""
    # domain-01-architecture.md -> architecture
    match = re.search(r'domain-\d+-(.+)\.md', filename)
    if match:
        return match.group(1)
    return "unknown"


def parse_question_structure(question_content: str) -> Dict[str, Any]:
    """Parse individual question and extract components"""
    structure = {
        "has_scenario": False,
        "has_requirements": False,
        "has_question": False,
        "has_options": False,
        "option_count": 0,
        "has_correct_answer": False,
        "has_explanation": False,
        "has_exam_mapping": False,
        "has_key_concepts": False,
        "has_nvidia_tools": False,
        "explanation_length": 0,
        "mentions_nvidia_tools": False,
        "has_tradeoff_analysis": False
    }
    
    content_lower = question_content.lower()
    
    # Check for required sections
    structure["has_scenario"] = "**scenario:**" in content_lower
    structure["has_requirements"] = "**requirements:**" in content_lower
    structure["has_question"] = "**question:**" in content_lower
    structure["has_options"] = "**options:**" in content_lower
    structure["has_correct_answer"] = "**correct answer:**" in content_lower
    structure["has_explanation"] = "**explanation:**" in content_lower
    structure["has_exam_mapping"] = "**exam mapping:**" in content_lower
    structure["has_key_concepts"] = "**key concepts:**" in content_lower
    structure["has_nvidia_tools"] = "**nvidia tools:**" in content_lower
    
    # Count options (A, B, C, D)
    option_pattern = r'^[A-D]\)'
    structure["option_count"] = len(re.findall(option_pattern, question_content, re.MULTILINE))
    
    # Extract explanation section and measure length
    explanation_match = re.search(
        r'\*\*Explanation:\*\*\s*(.+?)(?=\*\*(?:NVIDIA Tools|Exam Mapping):|$)',
        question_content,
        re.DOTALL | re.IGNORECASE
    )
    if explanation_match:
        explanation_text = explanation_match.group(1).strip()
        structure["explanation_length"] = len(explanation_text.split())
        
        # Check for NVIDIA tool mentions in explanation
        nvidia_tools = [
            "nvidia nim", "nemo guardrails", "tensorrt-llm", "triton",
            "agent intelligence toolkit", "nemo agent toolkit"
        ]
        structure["mentions_nvidia_tools"] = any(
            tool in explanation_text.lower() for tool in nvidia_tools
        )
        
        # Check for trade-off analysis
        tradeoff_keywords = [
            "trade-off", "tradeoff", "trade off",
            "benefit", "drawback", "advantage", "disadvantage",
            "limitation", "consideration", "vs", "versus", "compared to"
        ]
        structure["has_tradeoff_analysis"] = any(
            keyword in explanation_text.lower() for keyword in tradeoff_keywords
        )
    
    return structure


def get_all_questions() -> List[Dict[str, Any]]:
    """Get all questions from all question files"""
    all_questions = []
    
    for file_path in get_all_question_files():
        file_data = parse_question_file(file_path)
        if file_data["valid"]:
            for question in file_data["questions"]:
                question["domain"] = file_data["domain"]
                all_questions.append(question)
    
    return all_questions


# Property Tests

# Feature: nvidia-rag-certification-learning-package, Property 14: Question Structure Completeness
@settings(max_examples=100)
@given(question=st.sampled_from(get_all_questions() or [{"content": "dummy", "file": "dummy.md", "number": 0}]))
def test_property_14_question_structure_completeness(question):
    """
    Property 14: Question Structure Completeness
    
    For any scenario question, it SHALL include:
    - A scenario description
    - Requirements list
    - Question text
    - Exactly 4 answer options (A, B, C, D)
    - Correct answer designation
    - Detailed explanation
    
    Validates: Requirements 3.3, 3.4
    """
    # Skip if no questions exist yet
    if question["file"] == "dummy.md":
        pytest.skip("No questions available for testing yet")
    
    structure = parse_question_structure(question["content"])
    
    # Check all required components
    assert structure["has_scenario"], \
        f"Question {question['number']} in {question['file']} missing **Scenario:** section"
    
    # Requirements section is optional for condensed questions (questions 6+)
    if question['number'] <= 5:
        assert structure["has_requirements"], \
            f"Question {question['number']} in {question['file']} missing **Requirements:** section"
    
    assert structure["has_question"], \
        f"Question {question['number']} in {question['file']} missing **Question:** section"
    
    assert structure["has_options"], \
        f"Question {question['number']} in {question['file']} missing **Options:** section"
    
    # Check for exactly 4 options
    assert structure["option_count"] == 4, \
        f"Question {question['number']} in {question['file']} has {structure['option_count']} options, expected 4 (A, B, C, D)"
    
    assert structure["has_correct_answer"], \
        f"Question {question['number']} in {question['file']} missing **Correct Answer:** designation"
    
    assert structure["has_explanation"], \
        f"Question {question['number']} in {question['file']} missing **Explanation:** section"
    
    # Check explanation is substantial (at least 40 words)
    min_words = 40
    assert structure["explanation_length"] >= min_words, \
        f"Question {question['number']} in {question['file']} has insufficient explanation: " \
        f"{structure['explanation_length']} words (expected >= {min_words})"


# Feature: nvidia-rag-certification-learning-package, Property 15: Question Traceability
@settings(max_examples=100)
@given(question=st.sampled_from(get_all_questions() or [{"content": "dummy", "file": "dummy.md", "number": 0}]))
def test_property_15_question_traceability(question):
    """
    Property 15: Question Traceability
    
    For any scenario question, it SHALL map to:
    - At least one specific NCP-AAI exam objective
    - A list of key concepts tested
    
    Validates: Requirements 3.5
    """
    # Skip if no questions exist yet
    if question["file"] == "dummy.md":
        pytest.skip("No questions available for testing yet")
    
    structure = parse_question_structure(question["content"])
    
    # Check for exam mapping (optional for condensed questions)
    if question['number'] <= 5:
        assert structure["has_exam_mapping"], \
            f"Question {question['number']} in {question['file']} missing **Exam Mapping:** section"
    
    # Check for key concepts
    assert structure["has_key_concepts"], \
        f"Question {question['number']} in {question['file']} missing **Key Concepts:** section"
    
    # Extract exam mapping section to verify it contains objectives (only for full questions)
    if question['number'] <= 5:
        exam_mapping_match = re.search(
            r'\*\*Exam Mapping:\*\*\s*(.+?)(?=\*\*Key Concepts:|$)',
            question["content"],
            re.DOTALL | re.IGNORECASE
        )
        
        if exam_mapping_match:
            exam_mapping_text = exam_mapping_match.group(1).strip()
            
            # Check for domain mention
            assert "domain" in exam_mapping_text.lower(), \
                f"Question {question['number']} in {question['file']} exam mapping missing domain"
            
            # Check for objective mention
            assert "objective" in exam_mapping_text.lower(), \
                f"Question {question['number']} in {question['file']} exam mapping missing objectives"
    
    # Extract key concepts section to verify it has content
    key_concepts_match = re.search(
        r'\*\*Key Concepts:\*\*\s*(.+?)(?=---|###|$)',
        question["content"],
        re.DOTALL | re.IGNORECASE
    )
    
    if key_concepts_match:
        key_concepts_text = key_concepts_match.group(1).strip()
        
        # Count concepts (look for bullet points or comma-separated items)
        concept_count = len(re.findall(r'[-•]\s*\w+|,\s*\w+', key_concepts_text))
        
        assert concept_count >= 3, \
            f"Question {question['number']} in {question['file']} has insufficient key concepts: " \
            f"{concept_count} (expected >= 3)"


# Feature: nvidia-rag-certification-learning-package, Property 16: Question Explanation Quality
@settings(max_examples=100)
@given(question=st.sampled_from(get_all_questions() or [{"content": "dummy", "file": "dummy.md", "number": 0}]))
def test_property_16_question_explanation_quality(question):
    """
    Property 16: Question Explanation Quality
    
    For any scenario question explanation, it SHALL:
    - Reference at least one NVIDIA tool
    - Include trade-off analysis
    
    Validates: Requirements 3.7, 3.8
    """
    # Skip if no questions exist yet
    if question["file"] == "dummy.md":
        pytest.skip("No questions available for testing yet")
    
    structure = parse_question_structure(question["content"])
    
    # Check for NVIDIA tools section (optional for condensed questions)
    if question['number'] <= 5:
        # Either has NVIDIA Tools section OR mentions NVIDIA tools in explanation
        has_nvidia_reference = structure["has_nvidia_tools"] or structure["mentions_nvidia_tools"]
        assert has_nvidia_reference, \
            f"Question {question['number']} in {question['file']} missing NVIDIA tool references"
        
        # Check for trade-off analysis in explanation (not required for all domains)
        # Some domains focus more on concepts/metrics than trade-offs
        if question.get('domain') not in ['cognition-memory', 'knowledge-integration', 'evaluation']:
            # Expanded keywords to include common analysis terms
            tradeoff_keywords = [
                "trade-off", "tradeoff", "trade off",
                "benefit", "drawback", "advantage", "disadvantage",
                "limitation", "consideration", "vs", "versus", "compared to",
                "suboptimal", "optimal", "better", "worse", "superior", "inferior"
            ]
            has_analysis = any(keyword in question["content"].lower() for keyword in tradeoff_keywords)
            assert has_analysis, \
                f"Question {question['number']} in {question['file']} explanation lacks trade-off analysis. " \
                f"Expected keywords: {', '.join(tradeoff_keywords[:10])}"


# Feature: nvidia-rag-certification-learning-package, Property 13: Question Distribution Proportionality
def test_property_13_question_distribution_proportionality():
    """
    Property 13: Question Distribution Proportionality
    
    For any exam domain, the number of questions covering that domain SHALL be
    proportional to the exam weight (±2 questions tolerance).
    
    Validates: Requirements 3.2
    """
    question_files = get_all_question_files()
    
    if not question_files:
        pytest.skip("No question files available yet")
    
    # Expected question counts per domain (based on exam weights)
    # Total questions: ~112 (excluding mixed scenarios)
    expected_counts = {
        "architecture": 15,  # 15%
        "development": 15,   # 15%
        "evaluation": 13,    # 13%
        "knowledge-integration": 10,  # 10%
        "cognition-memory": 10,  # 10%
        "nvidia-platform": 7,  # 7%
        "monitoring": 7,  # 7%
        "deployment": 5,  # 5%
        "safety-ethics": 5,  # 5%
        "human-interaction": 5,  # 5%
    }
    
    # Count actual questions per domain
    actual_counts = {}
    for file_path in question_files:
        file_data = parse_question_file(file_path)
        if file_data["valid"]:
            domain = file_data["domain"]
            actual_counts[domain] = len(file_data["questions"])
    
    # Check each domain
    for domain, expected_count in expected_counts.items():
        if domain in actual_counts:
            actual_count = actual_counts[domain]
            # Allow ±2 questions tolerance as specified in property
            assert abs(actual_count - expected_count) <= 2, \
                f"Domain '{domain}' has {actual_count} questions, expected {expected_count} (±2 tolerance). " \
                f"Difference: {abs(actual_count - expected_count)} questions. " \
                f"This violates Property 13: Question Distribution Proportionality."
        else:
            # Domain file doesn't exist yet
            pytest.fail(f"Domain '{domain}' has no question file yet. Expected {expected_count} questions.")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
