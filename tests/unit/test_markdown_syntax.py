"""
Unit tests for Markdown syntax validation.

Tests that all Markdown files have valid syntax and proper structure.
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


class TestMarkdownSyntax:
    """Test Markdown syntax validity"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_markdown_file_not_empty(self, md_file):
        """Test that Markdown files are not empty"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, f"{md_file} is empty"
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_markdown_starts_with_heading(self, md_file):
        """Test that Markdown files start with a heading"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if file is empty
        if not content.strip():
            pytest.skip(f"{md_file} is empty")
        
        # Check if first non-empty line is a heading
        lines = content.split('\n')
        first_line = next((line for line in lines if line.strip()), None)
        
        assert first_line and first_line.startswith('#'), \
            f"{md_file} should start with a heading"
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_code_blocks_properly_closed(self, md_file):
        """Test that code blocks are properly closed"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count code block markers
        code_block_count = content.count('```')
        
        assert code_block_count % 2 == 0, \
            f"{md_file} has unclosed code block (odd number of ``` markers)"
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_no_empty_headings(self, md_file):
        """Test that there are no empty headings"""
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            if re.match(r'^#+\s*$', line):
                pytest.fail(f"{md_file} has empty heading at line {i}")
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_heading_hierarchy(self, md_file):
        """Test that heading hierarchy is reasonable (no skipping levels)"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all headings with their levels
        headings = []
        for line in content.split('\n'):
            if line.startswith('#'):
                level = len(re.match(r'^#+', line).group())
                headings.append(level)
        
        # Check that we don't skip more than 1 level
        for i in range(len(headings) - 1):
            level_jump = headings[i + 1] - headings[i]
            assert level_jump <= 2, \
                f"{md_file} has heading hierarchy issue: jumped from level {headings[i]} to {headings[i + 1]}"


class TestMarkdownLinks:
    """Test Markdown links"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_no_broken_internal_links(self, md_file):
        """Test that internal links (to other files) are valid"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all markdown links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # Skip external links (http/https)
            if link_url.startswith('http://') or link_url.startswith('https://'):
                continue
            
            # Skip anchors
            if link_url.startswith('#'):
                continue
            
            # Check if file exists (relative to md_file location)
            link_path = md_file.parent / link_url
            
            # Remove anchor if present
            if '#' in link_url:
                link_path = md_file.parent / link_url.split('#')[0]
            
            # Only check if it looks like a file path (has extension or is a directory)
            if '.' in link_url or link_url.endswith('/'):
                assert link_path.exists(), \
                    f"{md_file} has broken internal link: {link_url}"


class TestMarkdownTables:
    """Test Markdown tables"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_tables_have_proper_structure(self, md_file):
        """Test that tables have proper structure (header separator)"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find table headers (lines with | ... | ... |)
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Check if this looks like a table header
            if '|' in line and i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # If next line has dashes and pipes, it's a table separator
                if '|' in next_line and '-' in next_line:
                    # Count pipes in header and separator
                    header_pipes = line.count('|')
                    separator_pipes = next_line.count('|')
                    
                    # They should match
                    assert header_pipes == separator_pipes, \
                        f"{md_file} line {i + 1}: table header and separator have different column counts"


class TestCodeBlocks:
    """Test code blocks"""
    
    @pytest.mark.parametrize("md_file", get_all_markdown_files())
    def test_code_blocks_have_language_hint(self, md_file):
        """Test that code blocks have language hints (recommended)"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find code blocks
        code_blocks = re.findall(r'```(\w*)\n', content)
        
        # Count blocks with and without language hints
        total_blocks = len(code_blocks)
        blocks_with_lang = sum(1 for lang in code_blocks if lang)
        
        # At least 70% should have language hints (not strict requirement)
        if total_blocks > 0:
            ratio = blocks_with_lang / total_blocks
            if ratio < 0.7:
                print(f"Warning: {md_file} has {blocks_with_lang}/{total_blocks} code blocks with language hints ({ratio:.0%})")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
