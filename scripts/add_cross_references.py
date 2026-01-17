#!/usr/bin/env python3
"""
Script to add cross-references between learning materials.

This script adds links from:
- Course notes to notebooks
- Notebooks to questions
- Questions to course notes
- Labs to relevant modules
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Define cross-reference mappings
CROSS_REFERENCES = {
    "course-notes/module-01-agent-architecture-design.md": {
        "notebooks": [
            "notebooks/module-01/01-agent-architectures.ipynb",
            "notebooks/module-01/02-react-pattern.ipynb",
            "notebooks/module-01/03-multi-agent-systems.ipynb"
        ],
        "questions": ["exam-questions/domain-01-architecture.md"],
        "labs": ["labs/lab-01-basic-rag-agent", "labs/lab-02-multi-agent-research"]
    },
    "course-notes/module-02-agent-development.md": {
        "notebooks": [
            "notebooks/module-02/01-prompt-engineering.ipynb",
            "notebooks/module-02/02-tool-integration.ipynb",
            "notebooks/module-02/03-error-handling-patterns.ipynb",
            "notebooks/module-02/04-streaming-responses.ipynb"
        ],
        "questions": ["exam-questions/domain-02-development.md"],
        "labs": ["labs/lab-01-basic-rag-agent", "labs/lab-02-multi-agent-research"]
    },
    "course-notes/module-03-evaluation-tuning.md": {
        "notebooks": [
            "notebooks/module-03/01-evaluation-metrics.ipynb",
            "notebooks/module-03/02-evaluation-pipelines.ipynb",
            "notebooks/module-03/03-ab-testing.ipynb"
        ],
        "questions": ["exam-questions/domain-03-evaluation.md"],
        "labs": ["labs/lab-04-evaluation-optimization"]
    },
    "course-notes/module-04-knowledge-integration.md": {
        "notebooks": [
            "notebooks/module-04/01-rag-fundamentals.ipynb",
            "notebooks/module-04/02-embedding-models.ipynb",
            "notebooks/module-04/03-vector-stores.ipynb",
            "notebooks/module-04/04-retrieval-optimization.ipynb"
        ],
        "questions": ["exam-questions/domain-04-knowledge-integration.md"],
        "labs": ["labs/lab-01-basic-rag-agent"]
    },
    "course-notes/module-05-cognition-planning-memory.md": {
        "notebooks": [
            "notebooks/module-05/01-memory-mechanisms.ipynb",
            "notebooks/module-05/02-chain-of-thought.ipynb",
            "notebooks/module-05/03-task-decomposition.ipynb"
        ],
        "questions": ["exam-questions/domain-05-cognition-memory.md"],
        "labs": ["labs/lab-02-multi-agent-research"]
    },
    "course-notes/module-06-nvidia-platform.md": {
        "notebooks": [
            "notebooks/module-06/01-nvidia-nim.ipynb",
            "notebooks/module-06/02-nemo-guardrails.ipynb",
            "notebooks/module-06/03-tensorrt-llm.ipynb",
            "notebooks/module-06/04-triton-inference.ipynb"
        ],
        "questions": ["exam-questions/domain-06-nvidia-platform.md"],
        "labs": ["labs/lab-03-production-deployment", "labs/lab-05-safe-compliant-agent"]
    },
    "course-notes/module-07-monitoring-maintenance.md": {
        "notebooks": [
            "notebooks/module-07/01-monitoring-dashboards.ipynb",
            "notebooks/module-07/02-logging-tracing.ipynb",
            "notebooks/module-07/03-performance-profiling.ipynb"
        ],
        "questions": ["exam-questions/domain-07-monitoring.md"],
        "labs": ["labs/lab-03-production-deployment"]
    },
    "course-notes/module-08-deployment-scaling.md": {
        "notebooks": [
            "notebooks/module-08/01-containerization.ipynb",
            "notebooks/module-08/02-kubernetes-deployment.ipynb"
        ],
        "questions": ["exam-questions/domain-08-deployment.md"],
        "labs": ["labs/lab-03-production-deployment"]
    },
    "course-notes/module-09-safety-ethics-compliance.md": {
        "notebooks": [
            "notebooks/module-09/01-guardrails-implementation.ipynb",
            "notebooks/module-09/02-bias-detection.ipynb"
        ],
        "questions": ["exam-questions/domain-09-safety-ethics.md"],
        "labs": ["labs/lab-05-safe-compliant-agent"]
    },
    "course-notes/module-10-human-ai-interaction.md": {
        "notebooks": [
            "notebooks/module-10/01-ui-development.ipynb",
            "notebooks/module-10/02-feedback-loops.ipynb"
        ],
        "questions": ["exam-questions/domain-10-human-interaction.md"],
        "labs": ["labs/lab-05-safe-compliant-agent"]
    }
}


def add_cross_references_to_course_notes():
    """Add cross-references to course notes files."""
    print("Adding cross-references to course notes...")
    
    for note_file, refs in CROSS_REFERENCES.items():
        if not os.path.exists(note_file):
            print(f"  ⚠️  File not found: {note_file}")
            continue
        
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if cross-references section already exists
        if "## Related Materials" in content or "## Cross-References" in content:
            print(f"  ℹ️  Cross-references already exist in {note_file}")
            continue
        
        # Build cross-references section
        cross_ref_section = "\n\n---\n\n## Related Materials\n\n"
        cross_ref_section += "### Hands-On Practice\n\n"
        
        if refs.get("notebooks"):
            cross_ref_section += "**Interactive Notebooks:**\n"
            for notebook in refs["notebooks"]:
                notebook_name = os.path.basename(notebook)
                cross_ref_section += f"- [{notebook_name}](../../{notebook})\n"
            cross_ref_section += "\n"
        
        if refs.get("labs"):
            cross_ref_section += "**Practice Labs:**\n"
            for lab in refs["labs"]:
                lab_name = os.path.basename(lab)
                cross_ref_section += f"- [Lab: {lab_name.replace('-', ' ').title()}](../../{lab}/README.md)\n"
            cross_ref_section += "\n"
        
        cross_ref_section += "### Assessment\n\n"
        if refs.get("questions"):
            cross_ref_section += "**Exam Questions:**\n"
            for questions in refs["questions"]:
                domain_name = os.path.basename(questions).replace('.md', '').replace('domain-', 'Domain ').replace('-', ' ').title()
                cross_ref_section += f"- [{domain_name}](../../{questions})\n"
        
        # Add before the final self-assessment checklist or at the end
        if "## Self-Assessment Checklist" in content:
            content = content.replace("## Self-Assessment Checklist", cross_ref_section + "## Self-Assessment Checklist")
        else:
            content += cross_ref_section
        
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Added cross-references to {note_file}")


def add_cross_references_to_notebooks():
    """Add cross-references to notebook files."""
    print("\nAdding cross-references to notebooks...")
    
    # Map notebooks to their related materials
    notebook_refs = {
        "notebooks/module-01": {
            "notes": "course-notes/module-01-agent-architecture-design.md",
            "questions": "exam-questions/domain-01-architecture.md",
            "labs": ["labs/lab-01-basic-rag-agent", "labs/lab-02-multi-agent-research"]
        },
        "notebooks/module-02": {
            "notes": "course-notes/module-02-agent-development.md",
            "questions": "exam-questions/domain-02-development.md",
            "labs": ["labs/lab-01-basic-rag-agent", "labs/lab-02-multi-agent-research"]
        },
        "notebooks/module-03": {
            "notes": "course-notes/module-03-evaluation-tuning.md",
            "questions": "exam-questions/domain-03-evaluation.md",
            "labs": ["labs/lab-04-evaluation-optimization"]
        },
        "notebooks/module-04": {
            "notes": "course-notes/module-04-knowledge-integration.md",
            "questions": "exam-questions/domain-04-knowledge-integration.md",
            "labs": ["labs/lab-01-basic-rag-agent"]
        },
        "notebooks/module-05": {
            "notes": "course-notes/module-05-cognition-planning-memory.md",
            "questions": "exam-questions/domain-05-cognition-memory.md",
            "labs": ["labs/lab-02-multi-agent-research"]
        },
        "notebooks/module-06": {
            "notes": "course-notes/module-06-nvidia-platform.md",
            "questions": "exam-questions/domain-06-nvidia-platform.md",
            "labs": ["labs/lab-03-production-deployment", "labs/lab-05-safe-compliant-agent"]
        },
        "notebooks/module-07": {
            "notes": "course-notes/module-07-monitoring-maintenance.md",
            "questions": "exam-questions/domain-07-monitoring.md",
            "labs": ["labs/lab-03-production-deployment"]
        },
        "notebooks/module-08": {
            "notes": "course-notes/module-08-deployment-scaling.md",
            "questions": "exam-questions/domain-08-deployment.md",
            "labs": ["labs/lab-03-production-deployment"]
        },
        "notebooks/module-09": {
            "notes": "course-notes/module-09-safety-ethics-compliance.md",
            "questions": "exam-questions/domain-09-safety-ethics.md",
            "labs": ["labs/lab-05-safe-compliant-agent"]
        },
        "notebooks/module-10": {
            "notes": "course-notes/module-10-human-ai-interaction.md",
            "questions": "exam-questions/domain-10-human-interaction.md",
            "labs": ["labs/lab-05-safe-compliant-agent"]
        }
    }
    
    for notebook_dir, refs in notebook_refs.items():
        if not os.path.exists(notebook_dir):
            print(f"  ⚠️  Directory not found: {notebook_dir}")
            continue
        
        # Process all notebooks in the directory
        for notebook_file in Path(notebook_dir).glob("*.ipynb"):
            print(f"  Processing {notebook_file}...")
            # Note: For notebooks, we'll add a markdown cell with references
            # This requires JSON manipulation which we'll handle separately
            print(f"  ℹ️  Notebook cross-references should be added manually or via notebook-specific script")


def add_cross_references_to_questions():
    """Add cross-references to exam question files."""
    print("\nAdding cross-references to exam questions...")
    
    question_refs = {
        "exam-questions/domain-01-architecture.md": {
            "notes": "course-notes/module-01-agent-architecture-design.md",
            "notebooks": ["notebooks/module-01/01-agent-architectures.ipynb", 
                         "notebooks/module-01/02-react-pattern.ipynb",
                         "notebooks/module-01/03-multi-agent-systems.ipynb"]
        },
        "exam-questions/domain-02-development.md": {
            "notes": "course-notes/module-02-agent-development.md",
            "notebooks": ["notebooks/module-02/01-prompt-engineering.ipynb",
                         "notebooks/module-02/02-tool-integration.ipynb"]
        },
        "exam-questions/domain-03-evaluation.md": {
            "notes": "course-notes/module-03-evaluation-tuning.md",
            "notebooks": ["notebooks/module-03/01-evaluation-metrics.ipynb"]
        },
        "exam-questions/domain-04-knowledge-integration.md": {
            "notes": "course-notes/module-04-knowledge-integration.md",
            "notebooks": ["notebooks/module-04/01-rag-fundamentals.ipynb",
                         "notebooks/module-04/03-vector-stores.ipynb"]
        },
        "exam-questions/domain-05-cognition-memory.md": {
            "notes": "course-notes/module-05-cognition-planning-memory.md",
            "notebooks": ["notebooks/module-05/01-memory-mechanisms.ipynb"]
        },
        "exam-questions/domain-06-nvidia-platform.md": {
            "notes": "course-notes/module-06-nvidia-platform.md",
            "notebooks": ["notebooks/module-06/01-nvidia-nim.ipynb",
                         "notebooks/module-06/02-nemo-guardrails.ipynb"]
        },
        "exam-questions/domain-07-monitoring.md": {
            "notes": "course-notes/module-07-monitoring-maintenance.md",
            "notebooks": ["notebooks/module-07/01-monitoring-dashboards.ipynb"]
        },
        "exam-questions/domain-08-deployment.md": {
            "notes": "course-notes/module-08-deployment-scaling.md",
            "notebooks": ["notebooks/module-08/01-containerization.ipynb"]
        },
        "exam-questions/domain-09-safety-ethics.md": {
            "notes": "course-notes/module-09-safety-ethics-compliance.md",
            "notebooks": ["notebooks/module-09/01-guardrails-implementation.ipynb"]
        },
        "exam-questions/domain-10-human-interaction.md": {
            "notes": "course-notes/module-10-human-ai-interaction.md",
            "notebooks": ["notebooks/module-10/01-ui-development.ipynb"]
        }
    }
    
    for question_file, refs in question_refs.items():
        if not os.path.exists(question_file):
            print(f"  ⚠️  File not found: {question_file}")
            continue
        
        with open(question_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if cross-references already exist
        if "## Study Resources" in content or "## Related Materials" in content:
            print(f"  ℹ️  Cross-references already exist in {question_file}")
            continue
        
        # Build cross-references section
        cross_ref_section = "\n\n---\n\n## Study Resources\n\n"
        cross_ref_section += "To prepare for these questions, review:\n\n"
        
        if refs.get("notes"):
            module_name = os.path.basename(refs["notes"]).replace('.md', '').replace('module-', 'Module ').replace('-', ' ').title()
            cross_ref_section += f"**Course Notes:** [{module_name}](../../{refs['notes']})\n\n"
        
        if refs.get("notebooks"):
            cross_ref_section += "**Practice Notebooks:**\n"
            for notebook in refs["notebooks"]:
                notebook_name = os.path.basename(notebook).replace('.ipynb', '').replace('-', ' ').title()
                cross_ref_section += f"- [{notebook_name}](../../{notebook})\n"
        
        # Add at the end of the file
        content += cross_ref_section
        
        with open(question_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Added cross-references to {question_file}")


def add_cross_references_to_labs():
    """Add cross-references to lab README files."""
    print("\nAdding cross-references to labs...")
    
    lab_refs = {
        "labs/lab-01-basic-rag-agent/README.md": {
            "modules": ["module-01", "module-02", "module-04"],
            "notebooks": [
                "notebooks/module-04/01-rag-fundamentals.ipynb",
                "notebooks/module-04/02-embedding-models.ipynb",
                "notebooks/module-04/03-vector-stores.ipynb",
                "notebooks/module-02/03-error-handling-patterns.ipynb"
            ]
        },
        "labs/lab-02-multi-agent-research/README.md": {
            "modules": ["module-01", "module-02", "module-05"],
            "notebooks": [
                "notebooks/module-01/03-multi-agent-systems.ipynb",
                "notebooks/module-05/01-memory-mechanisms.ipynb",
                "notebooks/module-05/03-task-decomposition.ipynb"
            ]
        },
        "labs/lab-03-production-deployment/README.md": {
            "modules": ["module-06", "module-07", "module-08"],
            "notebooks": [
                "notebooks/module-06/01-nvidia-nim.ipynb",
                "notebooks/module-08/01-containerization.ipynb",
                "notebooks/module-08/02-kubernetes-deployment.ipynb",
                "notebooks/module-07/01-monitoring-dashboards.ipynb"
            ]
        },
        "labs/lab-04-evaluation-optimization/README.md": {
            "modules": ["module-03"],
            "notebooks": [
                "notebooks/module-03/01-evaluation-metrics.ipynb",
                "notebooks/module-03/02-evaluation-pipelines.ipynb",
                "notebooks/module-03/03-ab-testing.ipynb"
            ]
        },
        "labs/lab-05-safe-compliant-agent/README.md": {
            "modules": ["module-09", "module-10"],
            "notebooks": [
                "notebooks/module-09/01-guardrails-implementation.ipynb",
                "notebooks/module-09/02-bias-detection.ipynb",
                "notebooks/module-10/02-feedback-loops.ipynb"
            ]
        }
    }
    
    for lab_file, refs in lab_refs.items():
        if not os.path.exists(lab_file):
            print(f"  ⚠️  File not found: {lab_file}")
            continue
        
        with open(lab_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Resources section exists and update it
        if "## Resources" in content:
            # Find the Resources section
            resources_match = re.search(r'## Resources\n\n(.*?)(?=\n## |$)', content, re.DOTALL)
            if resources_match:
                existing_resources = resources_match.group(1)
                
                # Check if cross-references already exist
                if "### Relevant Course Notes" in existing_resources:
                    print(f"  ℹ️  Cross-references already exist in {lab_file}")
                    continue
                
                # Build enhanced resources section
                new_resources = "### Relevant Course Notes\n"
                for module in refs.get("modules", []):
                    module_file = f"course-notes/{module}-*.md"
                    new_resources += f"- [Module {module.split('-')[1].upper()}](../../course-notes/{module}*.md)\n"
                
                new_resources += "\n### Relevant Notebooks\n"
                for notebook in refs.get("notebooks", []):
                    notebook_name = os.path.basename(notebook).replace('.ipynb', '').replace('-', ' ').title()
                    new_resources += f"- [{notebook_name}](../../{notebook})\n"
                
                new_resources += "\n" + existing_resources
                
                # Replace the Resources section
                content = content.replace(existing_resources, new_resources)
                
                with open(lab_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Enhanced cross-references in {lab_file}")
        else:
            print(f"  ⚠️  No Resources section found in {lab_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Adding Cross-References to Learning Materials")
    print("=" * 60)
    
    add_cross_references_to_course_notes()
    add_cross_references_to_questions()
    add_cross_references_to_labs()
    
    print("\n" + "=" * 60)
    print("Cross-reference addition complete!")
    print("=" * 60)
    print("\nNote: Notebook cross-references require manual addition")
    print("or a separate notebook-specific script due to JSON format.")


if __name__ == "__main__":
    main()
