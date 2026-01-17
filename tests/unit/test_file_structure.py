"""
Unit tests for file structure validation.

Tests that all required directories and files exist with proper structure.
"""

import os
from pathlib import Path
import pytest


class TestDirectoryStructure:
    """Test that all required directories exist"""
    
    def test_course_notes_directory_exists(self):
        """Test that course-notes directory exists"""
        assert Path("course-notes").exists(), "course-notes directory missing"
    
    def test_notebooks_directory_exists(self):
        """Test that notebooks directory exists"""
        assert Path("notebooks").exists(), "notebooks directory missing"
    
    def test_exam_questions_directory_exists(self):
        """Test that exam-questions directory exists"""
        assert Path("exam-questions").exists(), "exam-questions directory missing"
    
    def test_quick_reference_directory_exists(self):
        """Test that quick-reference directory exists"""
        assert Path("quick-reference").exists(), "quick-reference directory missing"
    
    def test_labs_directory_exists(self):
        """Test that labs directory exists"""
        assert Path("labs").exists(), "labs directory missing"
    
    def test_tests_directory_exists(self):
        """Test that tests directory exists"""
        assert Path("tests").exists(), "tests directory missing"


class TestModuleDirectories:
    """Test that all module directories exist"""
    
    def test_notebooks_setup_directory_exists(self):
        """Test that notebooks/setup directory exists"""
        assert Path("notebooks/setup").exists(), "notebooks/setup directory missing"
    
    def test_module_directories_exist(self):
        """Test that all 10 module directories exist"""
        for i in range(1, 11):
            module_dir = Path(f"notebooks/module-{i:02d}")
            assert module_dir.exists(), f"Module directory {module_dir} missing"


class TestLabDirectories:
    """Test that all lab directories exist"""
    
    def test_lab_01_exists(self):
        """Test that lab-01-basic-rag-agent exists"""
        assert Path("labs/lab-01-basic-rag-agent").exists(), "Lab 01 directory missing"
    
    def test_lab_02_exists(self):
        """Test that lab-02-multi-agent-research exists"""
        assert Path("labs/lab-02-multi-agent-research").exists(), "Lab 02 directory missing"
    
    def test_lab_03_exists(self):
        """Test that lab-03-production-deployment exists"""
        assert Path("labs/lab-03-production-deployment").exists(), "Lab 03 directory missing"
    
    def test_lab_04_exists(self):
        """Test that lab-04-evaluation-optimization exists"""
        assert Path("labs/lab-04-evaluation-optimization").exists(), "Lab 04 directory missing"
    
    def test_lab_05_exists(self):
        """Test that lab-05-safe-compliant-agent exists"""
        assert Path("labs/lab-05-safe-compliant-agent").exists(), "Lab 05 directory missing"


class TestRequiredFiles:
    """Test that required files exist"""
    
    def test_root_readme_exists(self):
        """Test that root README.md exists"""
        assert Path("README.md").exists(), "Root README.md missing"
    
    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists"""
        assert Path("requirements.txt").exists(), "requirements.txt missing"
    
    def test_course_notes_readme_exists(self):
        """Test that course-notes README exists"""
        assert Path("course-notes/README.md").exists(), "course-notes/README.md missing"
    
    def test_notebooks_readme_exists(self):
        """Test that notebooks README exists"""
        assert Path("notebooks/README.md").exists(), "notebooks/README.md missing"
    
    def test_exam_questions_readme_exists(self):
        """Test that exam-questions README exists"""
        assert Path("exam-questions/README.md").exists(), "exam-questions/README.md missing"
    
    def test_quick_reference_readme_exists(self):
        """Test that quick-reference README exists"""
        assert Path("quick-reference/README.md").exists(), "quick-reference/README.md missing"
    
    def test_labs_readme_exists(self):
        """Test that labs README exists"""
        assert Path("labs/README.md").exists(), "labs/README.md missing"


class TestModuleFiles:
    """Test that all module files exist"""
    
    def test_all_10_modules_exist(self):
        """Test that all 10 course module files exist"""
        expected_modules = [
            "module-01-agent-architecture-design.md",
            "module-02-agent-development.md",
            "module-03-evaluation-tuning.md",
            "module-04-knowledge-integration.md",
            "module-05-cognition-planning-memory.md",
            "module-06-nvidia-platform.md",
            "module-07-monitoring-maintenance.md",
            "module-08-deployment-scaling.md",
            "module-09-safety-ethics-compliance.md",
            "module-10-human-ai-interaction.md",
        ]
        
        for module_file in expected_modules:
            module_path = Path(f"course-notes/{module_file}")
            assert module_path.exists(), f"Module file {module_file} missing"


class TestQuestionFiles:
    """Test that all question files exist"""
    
    def test_all_domain_question_files_exist(self):
        """Test that all 10 domain question files exist"""
        expected_files = [
            "domain-01-architecture.md",
            "domain-02-development.md",
            "domain-03-evaluation.md",
            "domain-04-knowledge-integration.md",
            "domain-05-cognition-memory.md",
            "domain-06-nvidia-platform.md",
            "domain-07-monitoring.md",
            "domain-08-deployment.md",
            "domain-09-safety-ethics.md",
            "domain-10-human-interaction.md",
        ]
        
        for question_file in expected_files:
            file_path = Path(f"exam-questions/{question_file}")
            assert file_path.exists(), f"Question file {question_file} missing"
    
    def test_mixed_scenarios_file_exists(self):
        """Test that mixed-scenarios.md exists"""
        assert Path("exam-questions/mixed-scenarios.md").exists(), \
            "exam-questions/mixed-scenarios.md missing"


class TestQuickReferenceFiles:
    """Test that all quick reference files exist"""
    
    def test_formulas_metrics_exists(self):
        """Test that formulas-metrics.md exists"""
        assert Path("quick-reference/formulas-metrics.md").exists(), \
            "quick-reference/formulas-metrics.md missing"
    
    def test_command_cheatsheet_exists(self):
        """Test that command-cheatsheet.md exists"""
        assert Path("quick-reference/command-cheatsheet.md").exists(), \
            "quick-reference/command-cheatsheet.md missing"
    
    def test_patterns_antipatterns_exists(self):
        """Test that patterns-antipatterns.md exists"""
        assert Path("quick-reference/patterns-antipatterns.md").exists(), \
            "quick-reference/patterns-antipatterns.md missing"
    
    def test_decision_trees_exists(self):
        """Test that decision-trees.md exists"""
        assert Path("quick-reference/decision-trees.md").exists(), \
            "quick-reference/decision-trees.md missing"
    
    def test_troubleshooting_flowcharts_exists(self):
        """Test that troubleshooting-flowcharts.md exists"""
        assert Path("quick-reference/troubleshooting-flowcharts.md").exists(), \
            "quick-reference/troubleshooting-flowcharts.md missing"
    
    def test_exam_tips_exists(self):
        """Test that exam-tips.md exists"""
        assert Path("quick-reference/exam-tips.md").exists(), \
            "quick-reference/exam-tips.md missing"


class TestLabStructure:
    """Test that labs have proper structure"""
    
    def test_lab_01_structure(self):
        """Test that lab 01 has required subdirectories"""
        lab_path = Path("labs/lab-01-basic-rag-agent")
        assert (lab_path / "README.md").exists(), "Lab 01 README missing"
        assert (lab_path / "requirements.txt").exists(), "Lab 01 requirements.txt missing"
        assert (lab_path / "starter-code").exists(), "Lab 01 starter-code directory missing"
        assert (lab_path / "solution").exists(), "Lab 01 solution directory missing"
        assert (lab_path / "test-data").exists(), "Lab 01 test-data directory missing"
        assert (lab_path / "rubric.md").exists(), "Lab 01 rubric.md missing"
    
    def test_lab_02_structure(self):
        """Test that lab 02 has required subdirectories"""
        lab_path = Path("labs/lab-02-multi-agent-research")
        assert (lab_path / "README.md").exists(), "Lab 02 README missing"
        assert (lab_path / "requirements.txt").exists(), "Lab 02 requirements.txt missing"
        assert (lab_path / "starter-code").exists(), "Lab 02 starter-code directory missing"
        assert (lab_path / "solution").exists(), "Lab 02 solution directory missing"
        assert (lab_path / "rubric.md").exists(), "Lab 02 rubric.md missing"
    
    def test_lab_03_structure(self):
        """Test that lab 03 has required subdirectories"""
        lab_path = Path("labs/lab-03-production-deployment")
        assert (lab_path / "README.md").exists(), "Lab 03 README missing"
        assert (lab_path / "requirements.txt").exists(), "Lab 03 requirements.txt missing"
        assert (lab_path / "starter-code").exists(), "Lab 03 starter-code directory missing"
        assert (lab_path / "rubric.md").exists(), "Lab 03 rubric.md missing"
    
    def test_lab_04_structure(self):
        """Test that lab 04 has required subdirectories"""
        lab_path = Path("labs/lab-04-evaluation-optimization")
        assert (lab_path / "README.md").exists(), "Lab 04 README missing"
        assert (lab_path / "requirements.txt").exists(), "Lab 04 requirements.txt missing"
        assert (lab_path / "starter-code").exists(), "Lab 04 starter-code directory missing"
        assert (lab_path / "rubric.md").exists(), "Lab 04 rubric.md missing"
    
    def test_lab_05_structure(self):
        """Test that lab 05 has required subdirectories"""
        lab_path = Path("labs/lab-05-safe-compliant-agent")
        assert (lab_path / "README.md").exists(), "Lab 05 README missing"
        assert (lab_path / "requirements.txt").exists(), "Lab 05 requirements.txt missing"
        assert (lab_path / "rubric.md").exists(), "Lab 05 rubric.md missing"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
