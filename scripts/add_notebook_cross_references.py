#!/usr/bin/env python3
"""
Script to add cross-references to Jupyter notebooks.

This script adds a "References" markdown cell at the end of each notebook
with links to related course notes, exam questions, and labs.
"""

import json
import os
from pathlib import Path

# Define notebook cross-reference mappings
NOTEBOOK_REFS = {
    "notebooks/module-01": {
        "module_name": "Module 1: Agent Architecture and Design",
        "notes": "course-notes/module-01-agent-architecture-design.md",
        "questions": "exam-questions/domain-01-architecture.md",
        "labs": [
            ("Lab 1: Basic RAG Agent", "labs/lab-01-basic-rag-agent/README.md"),
            ("Lab 2: Multi-Agent Research", "labs/lab-02-multi-agent-research/README.md")
        ]
    },
    "notebooks/module-02": {
        "module_name": "Module 2: Agent Development",
        "notes": "course-notes/module-02-agent-development.md",
        "questions": "exam-questions/domain-02-development.md",
        "labs": [
            ("Lab 1: Basic RAG Agent", "labs/lab-01-basic-rag-agent/README.md"),
            ("Lab 2: Multi-Agent Research", "labs/lab-02-multi-agent-research/README.md")
        ]
    },
    "notebooks/module-03": {
        "module_name": "Module 3: Evaluation and Tuning",
        "notes": "course-notes/module-03-evaluation-tuning.md",
        "questions": "exam-questions/domain-03-evaluation.md",
        "labs": [
            ("Lab 4: Evaluation and Optimization", "labs/lab-04-evaluation-optimization/README.md")
        ]
    },
    "notebooks/module-04": {
        "module_name": "Module 4: Knowledge Integration",
        "notes": "course-notes/module-04-knowledge-integration.md",
        "questions": "exam-questions/domain-04-knowledge-integration.md",
        "labs": [
            ("Lab 1: Basic RAG Agent", "labs/lab-01-basic-rag-agent/README.md")
        ]
    },
    "notebooks/module-05": {
        "module_name": "Module 5: Cognition, Planning, and Memory",
        "notes": "course-notes/module-05-cognition-planning-memory.md",
        "questions": "exam-questions/domain-05-cognition-memory.md",
        "labs": [
            ("Lab 2: Multi-Agent Research", "labs/lab-02-multi-agent-research/README.md")
        ]
    },
    "notebooks/module-06": {
        "module_name": "Module 6: NVIDIA Platform",
        "notes": "course-notes/module-06-nvidia-platform.md",
        "questions": "exam-questions/domain-06-nvidia-platform.md",
        "labs": [
            ("Lab 3: Production Deployment", "labs/lab-03-production-deployment/README.md"),
            ("Lab 5: Safe and Compliant Agent", "labs/lab-05-safe-compliant-agent/README.md")
        ]
    },
    "notebooks/module-07": {
        "module_name": "Module 7: Monitoring and Maintenance",
        "notes": "course-notes/module-07-monitoring-maintenance.md",
        "questions": "exam-questions/domain-07-monitoring.md",
        "labs": [
            ("Lab 3: Production Deployment", "labs/lab-03-production-deployment/README.md")
        ]
    },
    "notebooks/module-08": {
        "module_name": "Module 8: Deployment and Scaling",
        "notes": "course-notes/module-08-deployment-scaling.md",
        "questions": "exam-questions/domain-08-deployment.md",
        "labs": [
            ("Lab 3: Production Deployment", "labs/lab-03-production-deployment/README.md")
        ]
    },
    "notebooks/module-09": {
        "module_name": "Module 9: Safety, Ethics, and Compliance",
        "notes": "course-notes/module-09-safety-ethics-compliance.md",
        "questions": "exam-questions/domain-09-safety-ethics.md",
        "labs": [
            ("Lab 5: Safe and Compliant Agent", "labs/lab-05-safe-compliant-agent/README.md")
        ]
    },
    "notebooks/module-10": {
        "module_name": "Module 10: Human-AI Interaction",
        "notes": "course-notes/module-10-human-ai-interaction.md",
        "questions": "exam-questions/domain-10-human-interaction.md",
        "labs": [
            ("Lab 5: Safe and Compliant Agent", "labs/lab-05-safe-compliant-agent/README.md")
        ]
    }
}


def create_references_cell(refs, notebook_path):
    """Create a markdown cell with cross-references."""
    # Calculate relative path depth
    depth = len(Path(notebook_path).parent.parts)
    prefix = "../" * depth
    
    content = "## References\n\n"
    content += "### Course Materials\n\n"
    content += f"**Course Notes:** [{refs['module_name']}]({prefix}{refs['notes']})\n\n"
    content += "### Practice Questions\n\n"
    content += f"**Exam Questions:** [Practice Questions]({prefix}{refs['questions']})\n\n"
    content += "### Hands-On Labs\n\n"
    
    for lab_name, lab_path in refs['labs']:
        content += f"- [{lab_name}]({prefix}{lab_path})\n"
    
    content += "\n### Additional Resources\n\n"
    content += "- [NVIDIA NeMo Documentation](https://docs.nvidia.com/nemo/)\n"
    content += "- [LangChain Documentation](https://python.langchain.com/)\n"
    content += "- [NVIDIA AI Endpoints](https://build.nvidia.com/)\n"
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [content]
    }


def add_references_to_notebook(notebook_path, refs):
    """Add references cell to a notebook if it doesn't exist."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check if references already exist
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if '## References' in source or '## Next Steps' in source:
                    print(f"  ℹ️  References already exist in {notebook_path}")
                    return False
        
        # Add references cell at the end
        references_cell = create_references_cell(refs, notebook_path)
        notebook['cells'].append(references_cell)
        
        # Write back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        print(f"  ✅ Added references to {notebook_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {notebook_path}: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("Adding Cross-References to Notebooks")
    print("=" * 60)
    
    total_processed = 0
    total_updated = 0
    
    for notebook_dir, refs in NOTEBOOK_REFS.items():
        if not os.path.exists(notebook_dir):
            print(f"\n⚠️  Directory not found: {notebook_dir}")
            continue
        
        print(f"\nProcessing {notebook_dir}...")
        
        # Process all notebooks in the directory
        for notebook_file in sorted(Path(notebook_dir).glob("*.ipynb")):
            total_processed += 1
            if add_references_to_notebook(str(notebook_file), refs):
                total_updated += 1
    
    print("\n" + "=" * 60)
    print(f"Notebook cross-reference addition complete!")
    print(f"Processed: {total_processed} notebooks")
    print(f"Updated: {total_updated} notebooks")
    print("=" * 60)


if __name__ == "__main__":
    main()
