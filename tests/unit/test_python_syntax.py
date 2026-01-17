"""
Unit tests for Python syntax validation.

Tests that all Python files have valid syntax and can be compiled.
"""

import ast
import json
from pathlib import Path
import pytest


def get_all_python_files():
    """Get all Python files in the project"""
    python_files = []
    
    # Directories to search
    search_dirs = [
        "labs",
        "tests",
        "scripts"
    ]
    
    for directory in search_dirs:
        dir_path = Path(directory)
        if dir_path.exists():
            python_files.extend(dir_path.glob("**/*.py"))
    
    return python_files


def get_all_notebooks():
    """Get all Jupyter notebooks"""
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        return []
    return list(notebooks_dir.glob("**/*.ipynb"))


class TestPythonSyntax:
    """Test Python file syntax"""
    
    @pytest.mark.parametrize("py_file", get_all_python_files())
    def test_python_file_compiles(self, py_file):
        """Test that Python files can be compiled"""
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            compile(content, str(py_file), 'exec')
        except SyntaxError as e:
            pytest.fail(f"{py_file} has syntax error: {e}")
    
    @pytest.mark.parametrize("py_file", get_all_python_files())
    def test_python_file_can_be_parsed(self, py_file):
        """Test that Python files can be parsed into AST"""
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            ast.parse(content)
        except SyntaxError as e:
            pytest.fail(f"{py_file} cannot be parsed: {e}")
    
    @pytest.mark.parametrize("py_file", get_all_python_files())
    def test_python_file_not_empty(self, py_file):
        """Test that Python files are not empty"""
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip __init__.py files (can be empty)
        if py_file.name == "__init__.py":
            pytest.skip("__init__.py can be empty")
        
        assert len(content.strip()) > 0, f"{py_file} is empty"
    
    @pytest.mark.parametrize("py_file", get_all_python_files())
    def test_python_file_encoding(self, py_file):
        """Test that Python files can be read with UTF-8 encoding"""
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError as e:
            pytest.fail(f"{py_file} has encoding issue: {e}")


class TestNotebookSyntax:
    """Test Jupyter notebook syntax"""
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_is_valid_json(self, notebook):
        """Test that notebooks are valid JSON"""
        try:
            with open(notebook, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"{notebook} is not valid JSON: {e}")
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_has_cells(self, notebook):
        """Test that notebooks have cells"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        assert 'cells' in nb_data, f"{notebook} missing 'cells' key"
        assert isinstance(nb_data['cells'], list), f"{notebook} 'cells' is not a list"
    
    @pytest.mark.parametrize("notebook", get_all_notebooks())
    def test_notebook_code_cells_compile(self, notebook):
        """Test that code cells in notebooks can be compiled"""
        with open(notebook, 'r', encoding='utf-8') as f:
            nb_data = json.load(f)
        
        for i, cell in enumerate(nb_data.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                
                # Convert source to string
                if isinstance(source, list):
                    code = ''.join(source)
                else:
                    code = source
                
                # Skip empty cells
                if not code.strip():
                    continue
                
                # Try to compile
                try:
                    compile(code, f"{notebook}:cell-{i}", 'exec')
                except SyntaxError as e:
                    pytest.fail(f"{notebook} cell {i} has syntax error: {e}")


class TestPythonCodeQuality:
    """Test Python code quality basics"""
    
    @pytest.mark.parametrize("py_file", get_all_python_files())
    def test_no_syntax_errors_in_imports(self, py_file):
        """Test that import statements are valid"""
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract import lines
        import_lines = [line for line in content.split('\n') 
                       if line.strip().startswith('import ') or line.strip().startswith('from ')]
        
        # Try to compile each import line
        for line in import_lines:
            try:
                compile(line, str(py_file), 'exec')
            except SyntaxError as e:
                pytest.fail(f"{py_file} has invalid import: {line}\nError: {e}")
    
    @pytest.mark.parametrize("py_file", get_all_python_files())
    def test_no_obvious_syntax_issues(self, py_file):
        """Test for obvious syntax issues"""
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for common issues
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for tabs (should use spaces)
            if '\t' in line:
                print(f"Warning: {py_file} line {i} contains tabs (should use spaces)")
            
            # Check for trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                print(f"Warning: {py_file} line {i} has trailing whitespace")


class TestLabPythonFiles:
    """Test Python files in labs"""
    
    def test_lab_starter_code_compiles(self):
        """Test that all lab starter code compiles"""
        labs_dir = Path("labs")
        
        if not labs_dir.exists():
            pytest.skip("Labs directory not found")
        
        for lab_dir in labs_dir.iterdir():
            if not lab_dir.is_dir():
                continue
            
            starter_code_dir = lab_dir / "starter-code"
            if not starter_code_dir.exists():
                continue
            
            # Find all Python files
            py_files = list(starter_code_dir.glob("**/*.py"))
            
            for py_file in py_files:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                try:
                    compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Lab starter code {py_file} has syntax error: {e}")
    
    def test_lab_solution_code_compiles(self):
        """Test that all lab solution code compiles"""
        labs_dir = Path("labs")
        
        if not labs_dir.exists():
            pytest.skip("Labs directory not found")
        
        for lab_dir in labs_dir.iterdir():
            if not lab_dir.is_dir():
                continue
            
            solution_dir = lab_dir / "solution"
            if not solution_dir.exists():
                continue
            
            # Find all Python files
            py_files = list(solution_dir.glob("**/*.py"))
            
            for py_file in py_files:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                try:
                    compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Lab solution {py_file} has syntax error: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
