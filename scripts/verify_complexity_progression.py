#!/usr/bin/env python3
"""
Script to verify progressive complexity in modules and labs.

This script analyzes:
- Module ordering for complexity progression
- Lab ordering for complexity progression
- Provides recommendations for adjustments if needed
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


# Define expected complexity levels
MODULE_COMPLEXITY = {
    "module-01": {"level": 1, "name": "Agent Architecture and Design", "concepts": ["basic architectures", "ReAct pattern"]},
    "module-02": {"level": 2, "name": "Agent Development", "concepts": ["prompt engineering", "tool integration", "error handling"]},
    "module-03": {"level": 3, "name": "Evaluation and Tuning", "concepts": ["metrics", "A/B testing", "optimization"]},
    "module-04": {"level": 2, "name": "Knowledge Integration", "concepts": ["RAG", "embeddings", "vector stores"]},
    "module-05": {"level": 3, "name": "Cognition, Planning, and Memory", "concepts": ["memory management", "chain-of-thought", "task decomposition"]},
    "module-06": {"level": 3, "name": "NVIDIA Platform", "concepts": ["NIM", "Guardrails", "TensorRT-LLM", "Triton"]},
    "module-07": {"level": 3, "name": "Monitoring and Maintenance", "concepts": ["monitoring", "logging", "troubleshooting"]},
    "module-08": {"level": 4, "name": "Deployment and Scaling", "concepts": ["containerization", "Kubernetes", "scaling"]},
    "module-09": {"level": 3, "name": "Safety, Ethics, and Compliance", "concepts": ["guardrails", "bias detection", "compliance"]},
    "module-10": {"level": 3, "name": "Human-AI Interaction", "concepts": ["UI design", "feedback loops", "explainability"]}
}

LAB_COMPLEXITY = {
    "lab-01": {"level": 1, "name": "Basic RAG Agent", "complexity": "Beginner", "time": "3-4 hours"},
    "lab-02": {"level": 2, "name": "Multi-Agent Research System", "complexity": "Intermediate", "time": "4-5 hours"},
    "lab-03": {"level": 3, "name": "Production Deployment", "complexity": "Intermediate-Advanced", "time": "5-6 hours"},
    "lab-04": {"level": 2, "name": "Evaluation and Optimization", "complexity": "Intermediate", "time": "4-5 hours"},
    "lab-05": {"level": 4, "name": "Safe and Compliant Agent", "complexity": "Advanced", "time": "5-6 hours"}
}


def analyze_module_complexity():
    """Analyze module complexity progression."""
    print("Analyzing Module Complexity Progression")
    print("=" * 60)
    
    # Check if modules exist
    course_notes_dir = "course-notes"
    if not os.path.exists(course_notes_dir):
        print(f"⚠️  Directory not found: {course_notes_dir}")
        return
    
    # List modules in order
    modules = sorted([d for d in os.listdir(course_notes_dir) if d.startswith("module-")])
    
    print("\nModule Progression:")
    print("-" * 60)
    
    prev_level = 0
    issues = []
    
    for i, module in enumerate(modules, 1):
        module_key = module.replace(".md", "")
        if module_key in MODULE_COMPLEXITY:
            info = MODULE_COMPLEXITY[module_key]
            level = info["level"]
            name = info["name"]
            concepts = ", ".join(info["concepts"])
            
            # Check progression
            status = "✅"
            if level < prev_level:
                status = "⚠️"
                issues.append(f"{module_key}: Complexity decreased from {prev_level} to {level}")
            
            print(f"{status} {i}. {name}")
            print(f"   Complexity Level: {level}/4")
            print(f"   Key Concepts: {concepts}")
            print()
            
            prev_level = level
    
    # Report issues
    if issues:
        print("\n⚠️  Complexity Progression Issues:")
        print("-" * 60)
        for issue in issues:
            print(f"  - {issue}")
        print("\nRecommendation: Consider reordering modules or adjusting content complexity.")
    else:
        print("✅ Module complexity progression is acceptable.")
        print("   Note: Some variation is expected as modules cover different domains.")
    
    return len(issues) == 0


def analyze_lab_complexity():
    """Analyze lab complexity progression."""
    print("\n\nAnalyzing Lab Complexity Progression")
    print("=" * 60)
    
    # Check if labs exist
    labs_dir = "labs"
    if not os.path.exists(labs_dir):
        print(f"⚠️  Directory not found: {labs_dir}")
        return
    
    # List labs in order
    labs = sorted([d for d in os.listdir(labs_dir) if d.startswith("lab-")])
    
    print("\nLab Progression:")
    print("-" * 60)
    
    prev_level = 0
    issues = []
    
    for i, lab in enumerate(labs, 1):
        if lab in LAB_COMPLEXITY:
            info = LAB_COMPLEXITY[lab]
            level = info["level"]
            name = info["name"]
            complexity = info["complexity"]
            time = info["time"]
            
            # Check progression
            status = "✅"
            if level < prev_level:
                status = "⚠️"
                issues.append(f"{lab}: Complexity decreased from {prev_level} to {level}")
            
            print(f"{status} {i}. {name}")
            print(f"   Complexity Level: {level}/4 ({complexity})")
            print(f"   Estimated Time: {time}")
            print()
            
            prev_level = level
    
    # Report issues
    if issues:
        print("\n⚠️  Lab Complexity Progression Issues:")
        print("-" * 60)
        for issue in issues:
            print(f"  - {issue}")
        print("\nRecommendation: Consider reordering labs to maintain progressive complexity.")
    else:
        print("✅ Lab complexity progression is monotonically non-decreasing.")
    
    return len(issues) == 0


def analyze_content_depth():
    """Analyze content depth indicators in modules."""
    print("\n\nAnalyzing Content Depth Indicators")
    print("=" * 60)
    
    course_notes_dir = "course-notes"
    if not os.path.exists(course_notes_dir):
        return
    
    print("\nContent Depth Analysis:")
    print("-" * 60)
    
    for module_file in sorted(Path(course_notes_dir).glob("module-*.md")):
        with open(module_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count complexity indicators
        code_examples = len(re.findall(r'```python', content))
        diagrams = len(re.findall(r'```mermaid', content))
        exam_tips = len(re.findall(r'Exam Tip', content))
        sections = len(re.findall(r'^## ', content, re.MULTILINE))
        
        module_name = module_file.stem
        
        print(f"\n{module_name}:")
        print(f"  Code Examples: {code_examples}")
        print(f"  Diagrams: {diagrams}")
        print(f"  Exam Tips: {exam_tips}")
        print(f"  Major Sections: {sections}")
        
        # Assess depth
        depth_score = code_examples + diagrams + (exam_tips * 0.5)
        if depth_score < 10:
            print(f"  ⚠️  Depth Score: {depth_score:.1f} (Consider adding more examples)")
        else:
            print(f"  ✅ Depth Score: {depth_score:.1f}")


def generate_complexity_report():
    """Generate a comprehensive complexity report."""
    print("\n\n" + "=" * 60)
    print("COMPLEXITY PROGRESSION REPORT")
    print("=" * 60)
    
    module_ok = analyze_module_complexity()
    lab_ok = analyze_lab_complexity()
    analyze_content_depth()
    
    print("\n\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if module_ok and lab_ok:
        print("\n✅ Overall complexity progression is acceptable.")
        print("\nKey Findings:")
        print("  - Modules progress from foundational to advanced concepts")
        print("  - Labs maintain progressive complexity (beginner → advanced)")
        print("  - Content depth is appropriate for each level")
        print("\nNo adjustments needed.")
    else:
        print("\n⚠️  Some complexity progression issues detected.")
        print("\nRecommendations:")
        if not module_ok:
            print("  - Review module ordering")
            print("  - Consider adjusting content complexity in flagged modules")
        if not lab_ok:
            print("  - Reorder labs to maintain progressive complexity")
            print("  - Adjust lab difficulty levels as needed")
    
    print("\n" + "=" * 60)


def main():
    """Main execution function."""
    generate_complexity_report()


if __name__ == "__main__":
    main()
