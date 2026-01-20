"""Utility functions for accessibility testing.

This module provides helper functions for common accessibility validation checks
using BeautifulSoup4 for HTML parsing and HTML Tidy (via tidylib) for structural validation.

Design Decision: Using BeautifulSoup4 + tidylib instead of external accessibility
libraries (axe-core-python, pytest-a11y) because:
- BeautifulSoup4 is already available as a transitive dependency
- tidylib provides standards-based HTML5 validation without extra dependencies
- Provides fine-grained control over what we validate
- Allows project-specific accessibility standards
- Simpler to debug and maintain custom validators
- Lighter weight than external a11y checking libraries

Tool Selection:
- BeautifulSoup4: Used for semantic analysis (duplicate IDs, element relationships,
  ARIA attributes). It parses HTML leniently and auto-corrects malformed HTML,
  making it perfect for analyzing the DOM structure and content.
  - validate_duplicate_ids(): Finds all ID attributes and checks for duplicates
  - validate_semantic_html(): Validates correct use of <main>, <nav>, <header>, <footer>
  - validate_aria(): Checks ARIA attributes on interactive elements

- tidylib (HTML Tidy): Used for structural HTML5 validation. It strictly validates
  against HTML5 spec and detects nesting errors that BeautifulSoup would auto-correct.
  - validate_html_structure(): Detects invalid nesting, unclosed tags, content in wrong locations

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


def validate_duplicate_ids(html: str, filename: str = "index.html") -> List[str]:
    """Validate that no duplicate IDs exist in HTML.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages (empty if no duplicates found)
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    all_ids: Set[str] = set()
    for element in soup.find_all(id=True):
        element_id = element.get("id", "")
        if element_id in all_ids:
            violations.append(_format_violation(f"Duplicate ID found: {element_id}", filename, element))
        all_ids.add(element_id)

    return violations


def validate_semantic_html(html: str, filename: str = "index.html") -> List[str]:
    """Validate semantic HTML structure of theme.

    Theme-focused checks:
    - Exactly one <main> element, direct child of <body>
    - Multiple <nav> elements have aria-label to distinguish them
    - <header> and <footer> not nested inside <main>
    - Proper use of semantic elements in theme template

    Note: Duplicate ID checking is handled separately by validate_duplicate_ids()

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
            'unexpected',  # unexpected element in wrong context
            'missing </',  # missing closing tag
            'previously',  # element already opened (nesting issue)
            'discarding',  # invalid nesting being ignored
            'occurs after end'  # content in wrong place
        ])

        if is_structural_issue:
            violations.append(_format_violation(error, filename))

    return violations



def validate_aria_buttons(html: str, filename: str = "index.html") -> List[str]:
    """Check that all <button> elements have text content or aria-label."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.find_all("button"):
        text = element.get_text(strip=True)
        aria_label = element.get("aria-label", "").strip()
        if not text and not aria_label:
            violations.append(_format_violation(
                "Button missing text content or aria-label",
                filename,
                element
            ))
    return violations

def validate_aria_hidden(html: str, filename: str = "index.html") -> List[str]:
    """Check that aria-hidden is only used on truly decorative elements (no text content)."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    aria_hidden = soup.find_all(attrs={"aria-hidden": "true"})
    for element in aria_hidden:
        if element.get_text(strip=True):
            violations.append(_format_violation(
                f"Element with aria-hidden='true' contains content: {element}",
                filename,
                element
            ))
    return violations

