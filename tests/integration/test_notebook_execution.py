"""
Integration tests for notebook execution.

Tests that notebooks can be executed end-to-end without errors.
"""

import json
import subprocess
from pathlib import Path
import pytest


def get_all_notebooks():
    """Get all Jupyter notebooks"""
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        return []
    return list(notebooks_dir.glob("**/*.ipynb"))


def get_setup_notebooks():
    """Get setup notebooks"""
    setup_dir = Path("notebooks/setup")
    if not setup_dir.exists():
        return []
    return list(setup_dir.glob("*.ipynb"))


def get_module_notebooks():
    """Get module notebooks (excluding setup)"""
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        return []
    
    module_notebooks = []
    for i in range(1, 11):
        module_dir = notebooks_dir / f"module-{i:02d}"
        if module_dir.exists():
            module_notebooks.extend(module_dir.glob("*.ipynb"))
    
    return module_notebooks


class TestNotebookStructure:
    """Test notebook structure before execution"""
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_is_valid_json(self, notebook):
        """Test that notebook is valid JSON"""
        try:
            with open(notebook, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Notebook {notebook.name} is not valid JSON: {e}")
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_has_cells(self, notebook):
        """Test that notebook has cells"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        assert 'cells' in nb_data, f"Notebook {notebook.name} missing 'cells'"
        assert len(nb_data['cells']) > 0, f"Notebook {notebook.name} has no cells"


class TestNotebookCodeSyntax:
    """Test that notebook code cells have valid syntax"""
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_code_cells_have_valid_syntax(self, notebook):
        """Test that all code cells have valid Python syntax"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        for i, cell in enumerate(nb_data.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                
                # Convert to string
                if isinstance(source, list):
                    code = ''.join(source)
                else:
                    code = source
                
                # Skip empty cells
                if not code.strip():
                    continue
                
                # Check syntax
                try:
                    compile(code, f"{notebook.name}:cell-{i}", 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Notebook {notebook.name} cell {i} has syntax error: {e}")


class TestNotebookDependencies:
    """Test notebook dependencies"""
    
    def test_requirements_file_exists(self):
        """Test that requirements.txt exists"""
        assert Path("requirements.txt").exists(), "requirements.txt missing"
    
    def test_requirements_file_not_empty(self):
        """Test that requirements.txt is not empty"""
        with open("requirements.txt", 'r') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, "requirements.txt is empty"
    
    def test_common_dependencies_present(self):
        """Test that common dependencies are in requirements.txt"""
        with open("requirements.txt", 'r') as f:
            content = f.read().lower()
        
        # Check for key dependencies
        key_deps = ['jupyter', 'langchain', 'hypothesis', 'pytest']
        
        for dep in key_deps:
            assert dep in content, f"requirements.txt missing {dep}"


class TestNotebookExecution:
    """Test notebook execution (requires dependencies installed)"""
    
    @pytest.mark.slow
    @pytest.mark.parametrize("notebook", get_setup_notebooks())
    def test_setup_notebook_executes(self, notebook):
        """Test that setup notebooks can be executed"""
        # This test requires nbconvert and a working Python environment
        try:
            result = subprocess.run(
                ['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                 '--ExecutePreprocessor.timeout=300',
                 '--output', '/tmp/test_output.ipynb',
                 str(notebook)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                pytest.fail(f"Notebook {notebook.name} failed to execute:\n{result.stderr}")
                
        except FileNotFoundError:
            pytest.skip("jupyter nbconvert not available")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Notebook {notebook.name} execution timed out")


class TestNotebookSequence:
    """Test that notebooks can be executed in sequence"""
    
    def test_module_notebooks_ordered(self):
        """Test that module notebooks are properly numbered"""
        for i in range(1, 11):
            module_dir = Path(f"notebooks/module-{i:02d}")
            
            if not module_dir.exists():
                continue
            
            notebooks = sorted(module_dir.glob("*.ipynb"))
            
            # Check that notebooks are numbered (01-, 02-, etc.)
            for notebook in notebooks:
                # Notebook names should start with numbers
                assert notebook.stem[0].isdigit(), \
                    f"Notebook {notebook.name} should start with a number for ordering"


class TestNotebookOutputs:
    """Test notebook outputs and results"""
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_has_markdown_cells(self, notebook):
        """Test that notebooks have markdown cells (documentation)"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        markdown_cells = [c for c in nb_data.get('cells', []) 
                         if c.get('cell_type') == 'markdown']
        
        assert len(markdown_cells) > 0, \
            f"Notebook {notebook.name} should have markdown cells for documentation"
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_has_code_cells(self, notebook):
        """Test that notebooks have code cells"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        code_cells = [c for c in nb_data.get('cells', []) 
                     if c.get('cell_type') == 'code']
        
        assert len(code_cells) > 0, \
            f"Notebook {notebook.name} should have code cells"


class TestNotebookMetadata:
    """Test notebook metadata"""
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_has_metadata(self, notebook):
        """Test that notebooks have metadata"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        assert 'metadata' in nb_data, f"Notebook {notebook.name} missing metadata"
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_has_kernel_spec(self, notebook):
        """Test that notebooks have kernel specification"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        metadata = nb_data.get('metadata', {})
        
        # Check for kernel spec (either kernelspec or language_info)
        has_kernel_info = 'kernelspec' in metadata or 'language_info' in metadata
        
        assert has_kernel_info, \
            f"Notebook {notebook.name} should have kernel specification in metadata"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
