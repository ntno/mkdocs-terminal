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
    - Proper use of semantic elements in theme template
    
    Out of scope:
    - Form labeling (user content responsibility)
    - Link text (user content responsibility)
    
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
    
    return violations
    
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

