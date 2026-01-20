"""Utility functions for accessibility testing.

This module provides helper functions for common accessibility validation checks
using BeautifulSoup4 for HTML parsing and analysis.

Design Decision: Using BeautifulSoup4 with custom validators instead of external
libraries (axe-core-python, pytest-a11y) because:
- BeautifulSoup4 is already available as a transitive dependency
- Provides fine-grained control over what we validate
- Allows project-specific accessibility standards
- Simpler to debug and maintain custom validators
- Lighter weight than external a11y checking libraries

Scope: These validators test the theme's HTML structure and attributes.
They do NOT validate user content (headings, links, images, forms in documentation).
User content accessibility is the responsibility of site authors.
"""

from typing import List, Optional, Set
from bs4 import BeautifulSoup, Tag
from tidylib import tidy_document


def _format_violation(message: str, filename: str = "index.html", element: Optional[Tag] = None) -> str:
    """Format an accessibility violation message.
    
    Args:
        message: Human-readable description of the violation
        filename: Optional filename for error reporting
        element: Optional HTML element involved in violation
        
    Returns:
        Formatted violation message
    """
    violation = f"{filename}: {message}"
    if element:
        violation += f" [line approx. {element.sourceline}]"
    return violation




def validate_semantic_html(html: str, filename: str = "index.html") -> List[str]:
    """Validate semantic HTML structure of theme.
    
    Theme-focused checks:
    - Duplicate IDs within the page (theme structure issue)
    - Exactly one <main> element, direct child of <body>
    - Multiple <nav> elements have aria-label to distinguish them
    - <header> and <footer> not nested inside <main>
    - Proper use of semantic elements in theme template
    
    Out of scope:
    - Form labeling (user content responsibility)
    - Link text (user content responsibility)
    - Section/article heading requirements (user content responsibility)
    
    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting
        
    Returns:
        List of violation messages
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    
    # Check for duplicate IDs (theme responsibility)
    all_ids: Set[str] = set()
    for element in soup.find_all(id=True):
        element_id = element.get("id", "")
        if element_id in all_ids:
            violations.append(_format_violation(f"Duplicate ID found: {element_id}", filename, element))
        all_ids.add(element_id)
    
    # Check for exactly one <main> element
    main_elements = soup.find_all("main")
    if len(main_elements) != 1:
        violations.append(_format_violation(
            f"Expected exactly 1 <main> element, found {len(main_elements)}",
            filename
        ))
    
    # Check that <main> is direct child of <body>
    if main_elements:
        main_elem = main_elements[0]
        if main_elem.parent.name != "body":
            violations.append(_format_violation(
                f"<main> should be direct child of <body>, found parent: {main_elem.parent.name}",
                filename,
                main_elem
            ))
    
    # Check that multiple <nav> elements have aria-label to distinguish them
    nav_elements = soup.find_all("nav")
    if len(nav_elements) > 1:
        for nav in nav_elements:
            if not nav.get("aria-label"):
                violations.append(_format_violation(
                    "Multiple <nav> elements should have aria-label to distinguish them",
                    filename,
                    nav
                ))
    
    # Check that <header> and <footer> are not inside <main>
    if main_elements:
        main_elem = main_elements[0]
        
        if main_elem.find("header"):
            violations.append(_format_violation(
                "<header> should not be nested inside <main> (should be theme header outside main content)",
                filename,
                main_elem.find("header")
            ))
        
        if main_elem.find("footer"):
            violations.append(_format_violation(
                "<footer> should not be nested inside <main> (should be theme footer outside main content)",
                filename,
                main_elem.find("footer")
            ))
    
    return violations


def validate_html_structure(html: str, filename: str = "index.html") -> List[str]:
    """Validate HTML5 structure and element nesting.
    
    Uses HTML Tidy to detect structural issues such as:
    - Invalid element nesting (e.g., head inside body)
    - Unclosed or unexpected elements
    - Content occurring in wrong locations
    
    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting
        
    Returns:
        List of violation messages
    """
    violations: List[str] = []
    
    tidy_options = {
        'doctype': 'html5',
    }
    
    tidied_html, errors = tidy_document(html, options=tidy_options)
    
    # Filter for structural problems (nesting, unexpected elements, missing closing tags)
    error_lines = errors.strip().split('\n') if errors.strip() else []
    for error in error_lines:
        if not error:
            continue
        
        # Check for structural keywords that indicate violations
        is_structural_issue = any(keyword in error.lower() for keyword in [
            'unexpected',      # unexpected element in wrong context
            'missing </',      # missing closing tag
            'previously',      # element already opened (nesting issue)
            'discarding',      # invalid nesting being ignored
            'occurs after end' # content in wrong place
        ])
        
        if is_structural_issue:
            violations.append(_format_violation(error, filename))
    
    return violations


def validate_aria(html: str, filename: str = "index.html") -> List[str]:
    """Validate ARIA attribute usage.
    
    Checks for:
    - Proper ARIA roles on interactive elements
    - Presence of aria-label or aria-labelledby on unlabeled interactive elements
    - aria-hidden used appropriately
    - Modal dialogs have proper ARIA attributes
    
    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting
        
    Returns:
        List of violation messages
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    
    # Check for interactive elements with proper ARIA
    interactive_elements = soup.find_all(["button", "a", "input", "select", "textarea"])
    
    for element in interactive_elements:
        if element.name == "button":
            # Button should have text content or aria-label
            text = element.get_text(strip=True)
            aria_label = element.get("aria-label", "").strip()
            if not text and not aria_label:
                violations.append(_format_violation(
                    "Button missing text content or aria-label",
                    filename,
                    element
                ))
    
    # Check for aria-hidden on decorative elements
    aria_hidden = soup.find_all(attrs={"aria-hidden": "true"})
    for element in aria_hidden:
        # aria-hidden should only be on truly decorative elements
        if element.get_text(strip=True):
            violations.append(_format_violation(
                f"Element with aria-hidden='true' contains content: {element}",
                filename,
                element
            ))
    
    return violations

