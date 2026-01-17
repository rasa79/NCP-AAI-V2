#!/usr/bin/env python3
"""
Script to add exam-relevant concept highlighting.

This script adds:
- Callout boxes for exam tips in course notes
- Exam focus sections in notebooks
- Exam objective badges in questions
"""

import json
import os
import re
from pathlib import Path


def add_exam_callouts_to_notes():
    """Add exam tip callout boxes to course notes."""
    print("Adding exam tip callouts to course notes...")
    
    # Pattern to find existing exam tips
    exam_tip_pattern = r'> \*\*Exam Tip:\*\*'
    
    # Enhanced callout format
    def enhance_exam_tip(match_text):
        """Convert simple exam tips to callout boxes."""
        # Extract the tip content
        tip_content = match_text.replace('> **Exam Tip:**', '').strip()
        
        # Create enhanced callout box
        callout = f"""
> 📝 **EXAM TIP**
> 
> {tip_content}
"""
        return callout
    
    course_notes_dir = "course-notes"
    if not os.path.exists(course_notes_dir):
        print(f"  ⚠️  Directory not found: {course_notes_dir}")
        return
    
    for note_file in Path(course_notes_dir).glob("module-*.md"):
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already enhanced
        if "📝 **EXAM TIP**" in content:
            print(f"  ℹ️  Exam tips already enhanced in {note_file.name}")
            continue
        
        # Find and enhance exam tips
        original_tips = re.findall(r'> \*\*Exam Tip:\*\* [^\n]+', content)
        
        if not original_tips:
            print(f"  ℹ️  No exam tips found in {note_file.name}")
            continue
        
        # Replace each tip with enhanced version
        for tip in original_tips:
            enhanced = enhance_exam_tip(tip)
            content = content.replace(tip, enhanced.strip())
        
        # Write back
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Enhanced {len(original_tips)} exam tips in {note_file.name}")


def add_exam_focus_to_notebooks():
    """Add exam focus sections to notebooks."""
    print("\nAdding exam focus sections to notebooks...")
    
    # Exam focus content by module
    exam_focus_content = {
        "module-01": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ Architecture selection (reactive vs deliberative vs hybrid)
- ⭐⭐⭐ Trade-offs between architectures
- ⭐⭐ When to use each architecture pattern
- ⭐⭐ Scalability considerations

**Common Exam Scenarios:**
- Choosing architecture based on latency requirements
- Selecting architecture for different complexity levels
- Balancing speed vs sophistication

**Key Concepts to Master:**
- Reactive: Fast, rule-based, limited flexibility
- Deliberative: Complex reasoning, slower, goal-oriented
- Hybrid: Production-ready, balances both approaches
""",
        "module-02": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ Error handling patterns (retry logic, circuit breakers)
- ⭐⭐⭐ Prompt engineering techniques
- ⭐⭐ Tool integration best practices
- ⭐⭐ Streaming responses

**Common Exam Scenarios:**
- Implementing retry logic for API failures
- Designing prompts for complex tasks
- Handling tool execution errors

**Key Concepts to Master:**
- Exponential backoff for retries
- Circuit breaker pattern
- Dynamic prompt chains
- Graceful degradation
""",
        "module-03": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ Evaluation metrics (precision, recall, F1, faithfulness)
- ⭐⭐⭐ A/B testing frameworks
- ⭐⭐ Parameter tuning trade-offs
- ⭐⭐ Cost-performance optimization

**Common Exam Scenarios:**
- Selecting appropriate metrics for different agent types
- Designing A/B tests for agent improvements
- Balancing accuracy vs latency vs cost

**Key Concepts to Master:**
- RAG-specific metrics (faithfulness, relevance)
- Statistical significance in A/B testing
- Accuracy-latency trade-offs
""",
        "module-04": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ RAG pipeline components
- ⭐⭐⭐ Vector database selection
- ⭐⭐ Chunking strategies
- ⭐⭐ Retrieval optimization

**Common Exam Scenarios:**
- Designing RAG systems for specific domains
- Choosing vector database based on requirements
- Optimizing retrieval quality

**Key Concepts to Master:**
- Semantic search vs keyword search vs hybrid
- Chunk size and overlap trade-offs
- Embedding model selection
""",
        "module-05": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ Memory management (short-term vs long-term)
- ⭐⭐⭐ Chain-of-thought reasoning
- ⭐⭐ Task decomposition strategies
- ⭐⭐ Context window management

**Common Exam Scenarios:**
- Choosing memory architecture for different use cases
- Implementing chain-of-thought for complex problems
- Managing context window limitations

**Key Concepts to Master:**
- Sliding window vs summarization vs vector store
- Multi-hop reasoning
- Stateful orchestration
""",
        "module-06": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ NVIDIA NIM deployment
- ⭐⭐⭐ NeMo Guardrails configuration
- ⭐⭐ TensorRT-LLM optimization
- ⭐⭐ Triton Inference Server

**Common Exam Scenarios:**
- Implementing guardrails for safety
- Optimizing inference latency
- Deploying NIM microservices

**Key Concepts to Master:**
- NIM benefits and use cases
- Guardrails for compliance
- TensorRT-LLM optimization techniques
""",
        "module-07": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ Monitoring dashboards and metrics
- ⭐⭐ Logging and tracing
- ⭐⭐ Root cause analysis
- ⭐ Performance profiling

**Common Exam Scenarios:**
- Designing observability systems
- Troubleshooting agent failures
- Implementing automated alerts

**Key Concepts to Master:**
- Key metrics to monitor
- Distributed tracing
- Log aggregation
""",
        "module-08": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐ Containerization with Docker
- ⭐⭐ Kubernetes deployment
- ⭐⭐ Scaling strategies
- ⭐ CI/CD pipelines

**Common Exam Scenarios:**
- Containerizing agent workflows
- Load balancing strategies
- Cost optimization while maintaining SLAs

**Key Concepts to Master:**
- Docker best practices
- Kubernetes manifests
- Horizontal vs vertical scaling
""",
        "module-09": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐⭐ Guardrails implementation
- ⭐⭐ Bias detection and mitigation
- ⭐⭐ Privacy preservation
- ⭐ Compliance requirements

**Common Exam Scenarios:**
- Implementing bias detection
- Designing audit trails
- Building escalation protocols

**Key Concepts to Master:**
- NeMo Guardrails configuration
- Bias metrics
- Privacy-preserving techniques
""",
        "module-10": """
## 🎯 Exam Focus

This notebook covers concepts that appear frequently on the NCP-AAI exam:

**High-Priority Topics:**
- ⭐⭐ Human-in-the-loop workflows
- ⭐⭐ Feedback collection systems
- ⭐ Explainable AI
- ⭐ UI design for agents

**Common Exam Scenarios:**
- Designing human oversight mechanisms
- Implementing feedback loops
- Balancing automation with human control

**Key Concepts to Master:**
- Human-in-the-loop patterns
- Feedback integration
- Explainability techniques
"""
    }
    
    for module_dir, focus_content in exam_focus_content.items():
        notebook_dir = f"notebooks/{module_dir}"
        if not os.path.exists(notebook_dir):
            print(f"  ⚠️  Directory not found: {notebook_dir}")
            continue
        
        for notebook_file in Path(notebook_dir).glob("*.ipynb"):
            try:
                with open(notebook_file, 'r', encoding='utf-8') as f:
                    notebook = json.load(f)
                
                # Check if exam focus already exists
                has_exam_focus = False
                for cell in notebook.get('cells', []):
                    if cell.get('cell_type') == 'markdown':
                        source = ''.join(cell.get('source', []))
                        if '🎯 Exam Focus' in source:
                            has_exam_focus = True
                            break
                
                if has_exam_focus:
                    print(f"  ℹ️  Exam focus already exists in {notebook_file.name}")
                    continue
                
                # Find the position after "Overview" or at the beginning
                insert_position = 1  # After title cell
                for i, cell in enumerate(notebook.get('cells', [])):
                    if cell.get('cell_type') == 'markdown':
                        source = ''.join(cell.get('source', []))
                        if '## Overview' in source or '## Learning Objectives' in source:
                            insert_position = i + 1
                            break
                
                # Create exam focus cell
                exam_focus_cell = {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": focus_content.strip()
                }
                
                # Insert the cell
                notebook['cells'].insert(insert_position, exam_focus_cell)
                
                # Write back
                with open(notebook_file, 'w', encoding='utf-8') as f:
                    json.dump(notebook, f, indent=1, ensure_ascii=False)
                
                print(f"  ✅ Added exam focus to {notebook_file.name}")
                
            except Exception as e:
                print(f"  ❌ Error processing {notebook_file.name}: {e}")


def add_exam_badges_to_questions():
    """Add exam objective badges to question files."""
    print("\nAdding exam objective badges to questions...")
    
    question_files = list(Path("exam-questions").glob("domain-*.md"))
    
    for question_file in question_files:
        with open(question_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if badges already exist
        if "🎯 **Exam Objective" in content:
            print(f"  ℹ️  Exam badges already exist in {question_file.name}")
            continue
        
        # Find exam mapping sections and enhance them
        pattern = r'\*\*Exam Mapping:\*\*\n- Domain: ([^\n]+)\n- Objectives: ([^\n]+)\n- Weight: ([^\n]+)'
        
        def enhance_mapping(match):
            domain = match.group(1)
            objectives = match.group(2)
            weight = match.group(3)
            
            enhanced = f"""**Exam Mapping:**
🎯 **Exam Objective:** {objectives}
📊 **Domain:** {domain}
⚖️ **Weight:** {weight}
🔑 **Difficulty:** Scenario-based analysis required"""
            
            return enhanced
        
        # Replace mappings
        enhanced_content = re.sub(pattern, enhance_mapping, content)
        
        if enhanced_content != content:
            with open(question_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            print(f"  ✅ Added exam badges to {question_file.name}")
        else:
            print(f"  ℹ️  No exam mappings found in {question_file.name}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Adding Exam-Relevant Concept Highlighting")
    print("=" * 60)
    
    add_exam_callouts_to_notes()
    add_exam_focus_to_notebooks()
    add_exam_badges_to_questions()
    
    print("\n" + "=" * 60)
    print("Exam highlighting addition complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
