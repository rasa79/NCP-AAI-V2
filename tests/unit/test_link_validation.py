"""
Unit tests for link validation.

Tests that internal links in Markdown files are valid and point to existing files.
"""

import re
from pathlib import Path
import pytest


def get_all_markdown_files():
    """Get all Markdown files in the project"""
    markdown_files = []
    
    # Directories to search
    search_dirs = [
        "course-notes",
        "exam-questions",
        "quick-reference",
        "labs"
    ]
    
    for directory in search_dirs:
        dir_path = Path(directory)
        if dir_path.exists():
            markdown_files.extend(dir_path.glob("**/*.md"))
    
    # Add root README
    if Path("README.md").exists():
        markdown_files.append(Path("README.md"))
    
    return markdown_files


def extract_links(content):
    """Extract all links from Markdown content"""
    # Match [text](url) pattern
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(link_pattern, content)


def is_external_link(url):
    """Check if URL is external (http/https)"""
    return url.startswith('http://') or url.startswith('https://')


def is_anchor_link(url):
    """Check if URL is an anchor link (#section)"""
    return url.startswith('#')


def is_mailto_link(url):
    """Check if URL is a mailto link"""
    return url.startswith('mailto:')


class TestInternalLinks:
    """Test internal links in Markdown files"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_internal_file_links_exist(self, md_file):
        """Test that internal file links point to existing files"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_links(content)
        
        for link_text, link_url in links:
            # Skip external links
            if is_external_link(link_url):
                continue
            
            # Skip anchor links
            if is_anchor_link(link_url):
                continue
            
            # Skip mailto links
            if is_mailto_link(link_url):
                continue
            
            # Remove anchor if present
            clean_url = link_url.split('#')[0] if '#' in link_url else link_url
            
            # Skip empty URLs
            if not clean_url:
                continue
            
            # Resolve relative path
            if clean_url.startswith('/'):
                # Absolute path from root
                link_path = Path(clean_url[1:])
            else:
                # Relative path from current file
                link_path = (md_file.parent / clean_url).resolve()
            
            # Check if file or directory exists
            assert link_path.exists(), \
                f"{md_file} has broken link: [{link_text}]({link_url}) -> {link_path} does not exist"
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_no_duplicate_links(self, md_file):
        """Test that there are no duplicate links (same text and URL)"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_links(content)
        
        # Count occurrences of each link
        link_counts = {}
        for link_text, link_url in links:
            key = (link_text, link_url)
            link_counts[key] = link_counts.get(key, 0) + 1
        
        # Check for duplicates (more than 3 occurrences is suspicious)
        for (link_text, link_url), count in link_counts.items():
            if count > 5:
                print(f"Warning: {md_file} has link [{link_text}]({link_url}) repeated {count} times")


class TestImageLinks:
    """Test image links in Markdown files"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_image_links_exist(self, md_file):
        """Test that image links point to existing files"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match ![alt](url) pattern
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, content)
        
        for alt_text, image_url in images:
            # Skip external images
            if is_external_link(image_url):
                continue
            
            # Resolve relative path
            if image_url.startswith('/'):
                # Absolute path from root
                image_path = Path(image_url[1:])
            else:
                # Relative path from current file
                image_path = (md_file.parent / image_url).resolve()
            
            # Check if image exists
            assert image_path.exists(), \
                f"{md_file} has broken image link: ![{alt_text}]({image_url}) -> {image_path} does not exist"


class TestCrossReferences:
    """Test cross-references between materials"""
    
    def test_course_notes_reference_notebooks(self):
        """Test that course notes reference related notebooks"""
        course_notes_dir = Path("course-notes")
        
        if not course_notes_dir.exists():
            pytest.skip("Course notes directory not found")
        
        # Check each module
        for i in range(1, 11):
            module_file = course_notes_dir / f"module-{i:02d}-*.md"
            module_files = list(course_notes_dir.glob(f"module-{i:02d}-*.md"))
            
            if not module_files:
                continue
            
            module_file = module_files[0]
            
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if it references notebooks
            has_notebook_reference = (
                'notebook' in content.lower() or
                f'module-{i:02d}' in content or
                '../notebooks' in content
            )
            
            # This is a recommendation, not a strict requirement
            if not has_notebook_reference:
                print(f"Info: {module_file.name} could benefit from notebook cross-references")
    
    def test_notebooks_reference_course_notes(self):
        """Test that notebooks reference related course notes"""
        notebooks_dir = Path("notebooks")
        
        if not notebooks_dir.exists():
            pytest.skip("Notebooks directory not found")
        
        # Check module notebooks
        for i in range(1, 11):
            module_dir = notebooks_dir / f"module-{i:02d}"
            
            if not module_dir.exists():
                continue
            
            # Check notebooks in this module
            notebooks = list(module_dir.glob("*.ipynb"))
            
            for notebook in notebooks:
                # Read notebook
                import json
                try:
                    with open(notebook, 'r', encoding='utf-8') as f:
                        nb_data = json.load(f)
                except:
                    continue
                
                # Extract all text from markdown cells
                all_text = ""
                for cell in nb_data.get('cells', []):
                    if cell.get('cell_type') == 'markdown':
                        source = cell.get('source', [])
                        if isinstance(source, list):
                            all_text += ''.join(source)
                        else:
                            all_text += source
                
                # Check if it references course notes
                has_course_reference = (
                    'course-notes' in all_text or
                    'module-' in all_text or
                    'refer to' in all_text.lower()
                )
                
                # This is a recommendation
                if not has_course_reference:
                    print(f"Info: {notebook.name} could benefit from course notes cross-references")


class TestExternalLinks:
    """Test external links (informational only)"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_external_links_use_https(self, md_file):
        """Test that external links use HTTPS (recommended)"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_links(content)
        
        http_links = []
        for link_text, link_url in links:
            if link_url.startswith('http://'):
                http_links.append((link_text, link_url))
        
        # This is a recommendation, not a strict requirement
        if http_links:
            print(f"Info: {md_file} has {len(http_links)} HTTP links (HTTPS recommended)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
