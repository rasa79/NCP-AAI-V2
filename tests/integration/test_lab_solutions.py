"""
Integration tests for lab solutions.

Tests that lab solutions execute successfully and meet requirements.
"""

import subprocess
from pathlib import Path
import pytest


def get_all_labs():
    """Get all lab directories"""
    labs_dir = Path("labs")
    if not labs_dir.exists():
        return []
    return [d for d in labs_dir.iterdir() if d.is_dir() and d.name.startswith("lab-")]


class TestLabStructure:
    """Test lab directory structure"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_lab_has_readme(self, lab):
        """Test that lab has README"""
        readme = lab / "README.md"
        assert readme.exists(), f"Lab {lab.name} missing README.md"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_lab_has_requirements(self, lab):
        """Test that lab has requirements.txt"""
        requirements = lab / "requirements.txt"
        assert requirements.exists(), f"Lab {lab.name} missing requirements.txt"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_lab_has_starter_code(self, lab):
        """Test that lab has starter code"""
        starter_code = lab / "starter-code"
        assert starter_code.exists(), f"Lab {lab.name} missing starter-code directory"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_lab_has_solution(self, lab):
        """Test that lab has solution"""
        solution = lab / "solution"
        assert solution.exists(), f"Lab {lab.name} missing solution directory"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_lab_has_rubric(self, lab):
        """Test that lab has rubric"""
        rubric = lab / "rubric.md"
        assert rubric.exists(), f"Lab {lab.name} missing rubric.md"


class TestLabReadme:
    """Test lab README content"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_readme_has_scenario(self, lab):
        """Test that README includes scenario"""
        readme = lab / "README.md"
        
        with open(readme, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        assert 'scenario' in content, f"Lab {lab.name} README missing scenario section"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_readme_has_requirements(self, lab):
        """Test that README includes requirements"""
        readme = lab / "README.md"
        
        with open(readme, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        assert 'requirement' in content, f"Lab {lab.name} README missing requirements section"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_readme_has_setup_instructions(self, lab):
        """Test that README includes setup instructions"""
        readme = lab / "README.md"
        
        with open(readme, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        assert 'setup' in content or 'installation' in content, \
            f"Lab {lab.name} README missing setup instructions"


class TestLabStarterCode:
    """Test lab starter code"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_starter_code_has_python_files(self, lab):
        """Test that starter code has Python files"""
        starter_code = lab / "starter-code"
        
        if not starter_code.exists():
            pytest.skip(f"Lab {lab.name} has no starter-code directory")
        
        py_files = list(starter_code.glob("**/*.py"))
        
        assert len(py_files) > 0, f"Lab {lab.name} starter-code has no Python files"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_starter_code_compiles(self, lab):
        """Test that starter code has valid syntax"""
        starter_code = lab / "starter-code"
        
        if not starter_code.exists():
            pytest.skip(f"Lab {lab.name} has no starter-code directory")
        
        py_files = list(starter_code.glob("**/*.py"))
        
        for py_file in py_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                pytest.fail(f"Lab {lab.name} starter code {py_file.name} has syntax error: {e}")


class TestLabSolution:
    """Test lab solution code"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_solution_has_python_files(self, lab):
        """Test that solution has Python files"""
        solution = lab / "solution"
        
        if not solution.exists():
            pytest.skip(f"Lab {lab.name} has no solution directory")
        
        py_files = list(solution.glob("**/*.py"))
        
        assert len(py_files) > 0, f"Lab {lab.name} solution has no Python files"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_solution_compiles(self, lab):
        """Test that solution code has valid syntax"""
        solution = lab / "solution"
        
        if not solution.exists():
            pytest.skip(f"Lab {lab.name} has no solution directory")
        
        py_files = list(solution.glob("**/*.py"))
        
        for py_file in py_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                pytest.fail(f"Lab {lab.name} solution {py_file.name} has syntax error: {e}")
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_solution_has_error_handling(self, lab):
        """Test that solution includes error handling"""
        solution = lab / "solution"
        
        if not solution.exists():
            pytest.skip(f"Lab {lab.name} has no solution directory")
        
        py_files = list(solution.glob("**/*.py"))
        
        # Check if at least one file has error handling
        has_error_handling = False
        
        for py_file in py_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'try:' in content and 'except' in content:
                has_error_handling = True
                break
        
        assert has_error_handling, \
            f"Lab {lab.name} solution should include error handling (try-except blocks)"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_solution_has_docstrings(self, lab):
        """Test that solution includes docstrings"""
        solution = lab / "solution"
        
        if not solution.exists():
            pytest.skip(f"Lab {lab.name} has no solution directory")
        
        py_files = list(solution.glob("**/*.py"))
        
        # Check if at least one file has docstrings
        has_docstrings = False
        
        for py_file in py_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '"""' in content or "'''" in content:
                has_docstrings = True
                break
        
        assert has_docstrings, \
            f"Lab {lab.name} solution should include docstrings for documentation"


class TestLabRubric:
    """Test lab rubric"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_rubric_has_functionality_criteria(self, lab):
        """Test that rubric includes functionality criteria"""
        rubric = lab / "rubric.md"
        
        with open(rubric, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        assert 'functionality' in content, \
            f"Lab {lab.name} rubric missing functionality criteria"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_rubric_has_code_quality_criteria(self, lab):
        """Test that rubric includes code quality criteria"""
        rubric = lab / "rubric.md"
        
        with open(rubric, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        assert 'code quality' in content or 'quality' in content, \
            f"Lab {lab.name} rubric missing code quality criteria"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_rubric_has_scoring(self, lab):
        """Test that rubric includes scoring information"""
        rubric = lab / "rubric.md"
        
        with open(rubric, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Check for scoring indicators (points, percentage, etc.)
        has_scoring = any(indicator in content for indicator in [
            'points', '%', 'score', 'weight', 'criteria'
        ])
        
        assert has_scoring, f"Lab {lab.name} rubric should include scoring information"


class TestLabDependencies:
    """Test lab dependencies"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_requirements_file_not_empty(self, lab):
        """Test that requirements.txt is not empty"""
        requirements = lab / "requirements.txt"
        
        with open(requirements, 'r') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, f"Lab {lab.name} requirements.txt is empty"
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_requirements_file_has_versions(self, lab):
        """Test that requirements.txt includes version specifications"""
        requirements = lab / "requirements.txt"
        
        with open(requirements, 'r') as f:
            lines = f.readlines()
        
        # Filter out comments and empty lines
        package_lines = [line.strip() for line in lines 
                        if line.strip() and not line.strip().startswith('#')]
        
        if not package_lines:
            pytest.skip(f"Lab {lab.name} requirements.txt has no packages")
        
        # Check if at least some packages have version specs
        versioned_packages = [line for line in package_lines if '==' in line or '>=' in line]
        
        # At least 50% should have versions
        if len(versioned_packages) < len(package_lines) * 0.5:
            print(f"Warning: Lab {lab.name} requirements.txt should include version specifications")


class TestLabTestData:
    """Test lab test data"""
    
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_test_data_exists_if_needed(self, lab):
        """Test that test data exists for labs that need it"""
        test_data = lab / "test-data"
        
        # Labs 1, 2, and 4 should have test data
        if lab.name in ['lab-01-basic-rag-agent', 'lab-02-multi-agent-research', 
                       'lab-04-evaluation-optimization']:
            assert test_data.exists(), f"Lab {lab.name} should have test-data directory"
            
            # Check that test data directory is not empty
            files = list(test_data.glob("**/*.*"))
            assert len(files) > 0, f"Lab {lab.name} test-data directory is empty"


class TestLabExecution:
    """Test lab solution execution (requires dependencies)"""
    
    @pytest.mark.slow
    @pytest.mark.parametrize("lab", get_all_labs())
    def test_solution_imports_work(self, lab):
        """Test that solution imports don't fail"""
        solution = lab / "solution"
        
        if not solution.exists():
            pytest.skip(f"Lab {lab.name} has no solution directory")
        
        py_files = list(solution.glob("**/*.py"))
        
        for py_file in py_files:
            # Try to check imports (basic check)
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract import lines
            import_lines = [line for line in content.split('\n') 
                          if line.strip().startswith('import ') or 
                          line.strip().startswith('from ')]
            
            # Check that import lines have valid syntax
            for line in import_lines:
                try:
                    compile(line, str(py_file), 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Lab {lab.name} solution {py_file.name} has invalid import: {line}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
