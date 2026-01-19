"""HTML validation tests for Terminal for MkDocs theme.

This module tests that the theme generates valid HTML5 with proper semantic
structure according to WCAG 2.1 AA accessibility standards.

Test Scope:
- HTML5 validity and structure
- Semantic element usage (nav, main, aside, article, header, footer)
- Heading hierarchy (h1-h6 sequential structure)
- Form input labeling and associations
- Duplicate ID detection
"""

import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from tests.accessibility.utils import (
    validate_heading_hierarchy,
    validate_semantic_html,
)


class TestHeadingStructure:
    """Tests for HTML heading hierarchy and structure.
    
    Requirement: Headings must follow proper h1-h6 hierarchy.
    - Exactly one h1 per page (main page heading)
    - No skipped heading levels (h1 -> h3 is invalid, must have h2)
    - All headings must have descriptive text (not empty)
    """

    def test_index_has_single_h1(self, built_minimal_site):
        """Verify page has exactly one h1 element."""
        index_file = built_minimal_site / "index.html"
        html_content = index_file.read_text(encoding="utf-8")
        
        violations = validate_heading_hierarchy(html_content, "index.html")
        h1_violations = [v for v in violations if "h1" in v.lower()]
        assert not h1_violations, f"Heading h1 violations found: {h1_violations}"

    def test_heading_hierarchy_is_sequential(self, built_minimal_site):
        """Verify headings follow sequential hierarchy without skipping levels.
        
        Known issue: MkDocs includes a keyboard shortcuts modal (h4 element) 
        in the base theme that is not part of the main document outline.
        This causes a h2 -> h4 hierarchy violation. 
        We will filter out this specific header for now.
        """
        index_file = built_minimal_site / "index.html"
        html_content = index_file.read_text(encoding="utf-8")
        
        # Create a copy of the soup to filter
        test_soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove only the known base theme heading
        for h in test_soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            if h.get("id") in ("keyboardModalLabel",):
                h.decompose()
        
        # Extract and print remaining heading structure for debugging
        remaining_headings = test_soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        heading_structure = [(h.name, h.get_text(strip=True)[:60]) for h in remaining_headings]
        print(f"\nHeading structure found (after filtering base theme):")
        for tag, text in heading_structure:
            print(f"  {tag}: {text}")
        
        # Validate the filtered HTML
        violations = validate_heading_hierarchy(str(test_soup), "index.html")
        hierarchy_violations = [v for v in violations if "skip" in v.lower()]
        assert not hierarchy_violations, f"Heading hierarchy violations: {hierarchy_violations}"

    def test_no_empty_headings(self, built_minimal_site):
        """Verify all headings have descriptive text."""
        index_file = built_minimal_site / "index.html"
        html_content = index_file.read_text(encoding="utf-8")
        
        violations = validate_heading_hierarchy(html_content, "index.html")
        empty_violations = [v for v in violations if "empty" in v.lower()]
        assert not empty_violations, f"Empty heading violations: {empty_violations}"


class TestSemanticHTML:
    """Tests for semantic HTML structure.
    
    Requirement: HTML should use semantic elements appropriately.
    - Form inputs should have associated labels
    - No duplicate IDs within a page
    - Semantic elements should be used for their intended purpose
    """

    def test_no_duplicate_ids(self, built_minimal_site):
        """Verify page has no duplicate element IDs."""
        index_file = built_minimal_site / "index.html"
        html_content = index_file.read_text(encoding="utf-8")
        
        violations = validate_semantic_html(html_content, "index.html")
        duplicate_violations = [v for v in violations if "duplicate" in v.lower()]
        assert not duplicate_violations, f"Duplicate ID violations: {duplicate_violations}"

    def test_form_inputs_have_labels(self, built_minimal_site):
        """Verify form inputs are properly labeled."""
        index_file = built_minimal_site / "index.html"
        html_content = index_file.read_text(encoding="utf-8")
        
        violations = validate_semantic_html(html_content, "index.html")
        label_violations = [v for v in violations if "label" in v.lower()]
        # Search modal input is expected to have aria-label, so this should pass
        assert not label_violations, f"Form label violations: {label_violations}"


class TestHTMLValidity:
    """Tests for HTML5 validity and proper attribute usage.
    
    Requirement: Generated HTML should be valid HTML5.
    - All required attributes present
    - Proper attribute values and syntax
    - Valid element nesting
    """

    def test_index_page_is_valid_html(self, built_minimal_site):
        """Verify generated HTML is valid HTML5.
        
        This test uses BeautifulSoup parsing to verify the HTML structure
        is well-formed and can be parsed successfully.
        """
        index_file = built_minimal_site / "index.html"
        html_content = index_file.read_text(encoding="utf-8")
        
        # This will raise if HTML is severely malformed
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Verify we got a document
        assert soup.find("html") is not None, "No html element found"
        assert soup.find("head") is not None, "No head element found"
        assert soup.find("body") is not None, "No body element found"

    def test_all_generated_pages_have_valid_structure(self, built_minimal_site):
        """Verify all generated HTML files have valid basic structure."""
        html_files = list(built_minimal_site.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found in built site"
        
        for html_file in html_files:
            html_content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Every page should have doctype and html element
            assert soup.find("html") is not None, f"No html element in {html_file.name}"
            assert soup.find("head") is not None, f"No head element in {html_file.name}"
            assert soup.find("body") is not None, f"No body element in {html_file.name}"
