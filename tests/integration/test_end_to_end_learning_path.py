"""
Integration tests for end-to-end learning path.

Tests that the complete learning path flows correctly from modules to
notebooks to questions to labs.
"""

from pathlib import Path
import pytest


class TestLearningPathCompleteness:
    """Test that all components of the learning path exist"""
    
    def test_all_modules_exist(self):
        """Test that all 10 modules exist"""
        course_notes_dir = Path("course-notes")
        
        assert course_notes_dir.exists(), "course-notes directory missing"
        
        for i in range(1, 11):
            # Find module file (name may vary)
            module_files = list(course_notes_dir.glob(f"module-{i:02d}-*.md"))
            
            assert len(module_files) > 0, f"Module {i:02d} missing"
    
    def test_all_notebook_modules_exist(self):
        """Test that all 10 notebook modules exist"""
        notebooks_dir = Path("notebooks")
        
        assert notebooks_dir.exists(), "notebooks directory missing"
        
        for i in range(1, 11):
            module_dir = notebooks_dir / f"module-{i:02d}"
            
            assert module_dir.exists(), f"Notebook module {i:02d} directory missing"
    
    def test_all_question_domains_exist(self):
        """Test that all 10 question domains exist"""
        questions_dir = Path("exam-questions")
        
        assert questions_dir.exists(), "exam-questions directory missing"
        
        expected_domains = [
            "architecture", "development", "evaluation", "knowledge-integration",
            "cognition-memory", "nvidia-platform", "monitoring", "deployment",
            "safety-ethics", "human-interaction"
        ]
        
        for i, domain in enumerate(expected_domains, 1):
            domain_file = questions_dir / f"domain-{i:02d}-{domain}.md"
            
            assert domain_file.exists(), f"Question domain {domain} missing"
    
    def test_all_labs_exist(self):
        """Test that all 5 labs exist"""
        labs_dir = Path("labs")
        
        assert labs_dir.exists(), "labs directory missing"
        
        expected_labs = [
            "lab-01-basic-rag-agent",
            "lab-02-multi-agent-research",
            "lab-03-production-deployment",
            "lab-04-evaluation-optimization",
            "lab-05-safe-compliant-agent"
        ]
        
        for lab_name in expected_labs:
            lab_dir = labs_dir / lab_name
            
            assert lab_dir.exists(), f"Lab {lab_name} missing"
    
    def test_quick_reference_complete(self):
        """Test that quick reference is complete"""
        quick_ref_dir = Path("quick-reference")
        
        assert quick_ref_dir.exists(), "quick-reference directory missing"
        
        expected_files = [
            "formulas-metrics.md",
            "command-cheatsheet.md",
            "patterns-antipatterns.md",
            "decision-trees.md",
            "troubleshooting-flowcharts.md",
            "exam-tips.md"
        ]
        
        for filename in expected_files:
            file_path = quick_ref_dir / filename
            
            assert file_path.exists(), f"Quick reference {filename} missing"


class TestLearningPathProgression:
    """Test that learning path has proper progression"""
    
    def test_modules_cover_exam_domains(self):
        """Test that modules cover all exam domains"""
        course_notes_dir = Path("course-notes")
        
        # Expected domains in order
        expected_domains = [
            "architecture", "development", "evaluation", "knowledge",
            "cognition", "nvidia", "monitoring", "deployment", "safety", "human"
        ]
        
        for i, domain_keyword in enumerate(expected_domains, 1):
            module_files = list(course_notes_dir.glob(f"module-{i:02d}-*.md"))
            
            assert len(module_files) > 0, f"Module {i:02d} missing"
            
            # Check that module name contains domain keyword
            module_name = module_files[0].stem.lower()
            
            assert domain_keyword in module_name, \
                f"Module {i:02d} should cover {domain_keyword} domain"
    
    def test_notebooks_align_with_modules(self):
        """Test that notebook modules align with course modules"""
        notebooks_dir = Path("notebooks")
        
        for i in range(1, 11):
            module_dir = notebooks_dir / f"module-{i:02d}"
            
            if not module_dir.exists():
                pytest.fail(f"Notebook module {i:02d} missing")
            
            # Check that module has notebooks
            notebooks = list(module_dir.glob("*.ipynb"))
            
            assert len(notebooks) > 0, \
                f"Notebook module {i:02d} has no notebooks"
    
    def test_questions_align_with_modules(self):
        """Test that question domains align with modules"""
        questions_dir = Path("exam-questions")
        
        # Check that we have 10 domain files
        domain_files = list(questions_dir.glob("domain-*.md"))
        
        # Exclude README and answer-key
        domain_files = [f for f in domain_files 
                       if f.name not in ["README.md", "answer-key.md"]]
        
        assert len(domain_files) == 10, \
            f"Expected 10 domain question files, found {len(domain_files)}"
    
    def test_labs_progress_in_complexity(self):
        """Test that labs progress in complexity"""
        labs_dir = Path("labs")
        
        expected_progression = [
            ("lab-01-basic-rag-agent", "beginner"),
            ("lab-02-multi-agent-research", "intermediate"),
            ("lab-03-production-deployment", "intermediate-advanced"),
            ("lab-04-evaluation-optimization", "intermediate"),
            ("lab-05-safe-compliant-agent", "advanced")
        ]
        
        for lab_name, expected_complexity in expected_progression:
            lab_dir = labs_dir / lab_name
            readme = lab_dir / "README.md"
            
            if not readme.exists():
                continue
            
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Check for complexity indicator
            # This is informational, not a strict requirement
            if expected_complexity.lower() not in content:
                print(f"Info: Lab {lab_name} should document complexity as {expected_complexity}")


class TestLearningPathCoverage:
    """Test that learning path provides comprehensive coverage"""
    
    def test_modules_cover_all_exam_weights(self):
        """Test that modules cover all exam weight categories"""
        course_notes_dir = Path("course-notes")
        
        # Expected weights
        expected_weights = {
            "15%": 2,  # Architecture and Development
            "13%": 1,  # Evaluation
            "10%": 2,  # Knowledge Integration and Cognition
            "7%": 2,   # NVIDIA Platform and Monitoring
            "5%": 3    # Deployment, Safety, Human Interaction
        }
        
        # Count modules by weight (approximate check)
        all_content = ""
        
        for module_file in course_notes_dir.glob("module-*.md"):
            with open(module_file, 'r', encoding='utf-8') as f:
                all_content += f.read()
        
        # Check that weight percentages are mentioned
        for weight in expected_weights.keys():
            assert weight in all_content, \
                f"Exam weight {weight} should be documented in modules"
    
    def test_notebooks_cover_key_frameworks(self):
        """Test that notebooks cover key frameworks"""
        notebooks_dir = Path("notebooks")
        
        # Key frameworks that should be covered
        key_frameworks = [
            "langchain", "gradio", "langserve"
        ]
        
        # Collect all notebook content
        all_content = ""
        
        for notebook_file in notebooks_dir.glob("**/*.ipynb"):
            import json
            try:
                with open(notebook_file, 'r', encoding='utf-8') as f:
                    nb_data = json.load(f)
                
                # Extract code from cells
                for cell in nb_data.get('cells', []):
                    if cell.get('cell_type') == 'code':
                        source = cell.get('source', [])
                        if isinstance(source, list):
                            all_content += ''.join(source)
                        else:
                            all_content += source
            except:
                continue
        
        all_content_lower = all_content.lower()
        
        # Check that at least one framework is covered
        frameworks_found = [fw for fw in key_frameworks if fw in all_content_lower]
        
        assert len(frameworks_found) > 0, \
            f"Notebooks should cover at least one key framework: {key_frameworks}"
    
    def test_questions_cover_all_categories(self):
        """Test that questions cover all key categories"""
        questions_dir = Path("exam-questions")
        
        # Key question categories
        key_categories = [
            "architecture", "error handling", "performance", "scaling",
            "evaluation", "safety", "troubleshooting"
        ]
        
        # Collect all question content
        all_content = ""
        
        for question_file in questions_dir.glob("domain-*.md"):
            with open(question_file, 'r', encoding='utf-8') as f:
                all_content += f.read().lower()
        
        # Check that categories are covered
        categories_found = [cat for cat in key_categories if cat in all_content]
        
        # At least 5 out of 7 categories should be covered
        assert len(categories_found) >= 5, \
            f"Questions should cover at least 5 key categories, found {len(categories_found)}"
    
    def test_labs_cover_end_to_end_workflows(self):
        """Test that labs cover end-to-end workflows"""
        labs_dir = Path("labs")
        
        # Key workflows that should be covered
        key_workflows = [
            "rag", "multi-agent", "deployment", "evaluation", "safety"
        ]
        
        # Collect all lab README content
        all_content = ""
        
        for lab_dir in labs_dir.iterdir():
            if not lab_dir.is_dir():
                continue
            
            readme = lab_dir / "README.md"
            if readme.exists():
                with open(readme, 'r', encoding='utf-8') as f:
                    all_content += f.read().lower()
        
        # Check that workflows are covered
        workflows_found = [wf for wf in key_workflows if wf in all_content]
        
        assert len(workflows_found) >= 4, \
            f"Labs should cover at least 4 key workflows, found {len(workflows_found)}"


class TestLearningPathDocumentation:
    """Test that learning path is well documented"""
    
    def test_root_readme_exists(self):
        """Test that root README exists"""
        assert Path("README.md").exists(), "Root README.md missing"
    
    def test_root_readme_has_navigation(self):
        """Test that root README has navigation"""
        with open("README.md", 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Check for navigation elements
        navigation_indicators = [
            "table of contents", "navigation", "getting started",
            "course-notes", "notebooks", "labs"
        ]
        
        has_navigation = any(indicator in content for indicator in navigation_indicators)
        
        assert has_navigation, "Root README should include navigation"
    
    def test_component_readmes_exist(self):
        """Test that component READMEs exist"""
        component_dirs = [
            "course-notes",
            "notebooks",
            "exam-questions",
            "quick-reference",
            "labs"
        ]
        
        for component_dir in component_dirs:
            readme = Path(component_dir) / "README.md"
            
            assert readme.exists(), f"{component_dir}/README.md missing"
    
    def test_requirements_file_complete(self):
        """Test that requirements.txt is complete"""
        with open("requirements.txt", 'r') as f:
            content = f.read().lower()
        
        # Key dependencies
        key_deps = [
            "jupyter", "langchain", "hypothesis", "pytest"
        ]
        
        for dep in key_deps:
            assert dep in content, f"requirements.txt missing {dep}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
