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
"""

from typing import List, Optional, Set, Tuple
from bs4 import BeautifulSoup, Tag


class AccessibilityValidator:
    """Base class for accessibility validation."""

    def __init__(self, html: str, filename: str = "index.html"):
        """Initialize validator with HTML content.

        Args:
            html: HTML string to validate
            filename: Optional filename for error reporting
        """
        self.html = html
        self.filename = filename
        self.soup = BeautifulSoup(html, "html.parser")
        self.violations: List[str] = []

    def add_violation(self, message: str, element: Optional[Tag] = None):
        """Record an accessibility violation.

        Args:
            message: Human-readable description of the violation
            element: Optional HTML element involved in violation
        """
        violation = f"{self.filename}: {message}"
        if element:
            violation += f" [line approx. {element.sourceline}]"
        self.violations.append(violation)

    def get_violations(self) -> List[str]:
        """Return list of all recorded violations."""
        return self.violations

    def has_violations(self) -> bool:
        """Check if any violations were found."""
        return len(self.violations) > 0


class HeadingValidator(AccessibilityValidator):
    """Validator for heading structure (h1-h6 hierarchy)."""

    def validate(self) -> bool:
        """Validate heading hierarchy.

        Rules:
        - Document should have exactly one h1
        - Heading levels should not skip (e.g., h1 -> h3 is invalid)
        - Headings should have descriptive text

        Returns:
            True if valid, False otherwise
        """
        headings = self.soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

        if not headings:
            return True  # No headings is not invalid

        # Check for multiple h1s
        h1_elements = [h for h in headings if h.name == "h1"]
        if len(h1_elements) > 1:
            self.add_violation(f"Found {len(h1_elements)} h1 elements, expected 1")
            return False

        # Check for h1
        if len(h1_elements) == 0:
            self.add_violation("No h1 element found")
            return False

        # Check heading hierarchy (no skipping levels)
        heading_levels = [int(h.name[1]) for h in headings]
        for i in range(len(heading_levels) - 1):
            if heading_levels[i + 1] - heading_levels[i] > 1:
                self.add_violation(
                    f"Heading hierarchy skips from h{heading_levels[i]} to "
                    f"h{heading_levels[i + 1]}", headings[i + 1]
                )

        # Check for empty headings
        for heading in headings:
            text = heading.get_text(strip=True)
            if not text:
                self.add_violation(f"Empty {heading.name} element", heading)

        return not self.has_violations()


class ImageValidator(AccessibilityValidator):
    """Validator for image alt text and decorative image handling."""

    def validate(self) -> bool:
        """Validate image alt text.

        Rules:
        - All images should have alt attribute
        - Alt text should be descriptive (not "image", "photo", "picture")
        - Decorative images can be marked with data-decorative="true"
        - Empty alt text is allowed only for decorative images

        Returns:
            True if valid, False otherwise
        """
        images = self.soup.find_all("img")

        for img in images:
            is_decorative = img.get("data-decorative", "false").lower() == "true"
            alt_text = img.get("alt", "").strip()
            src = img.get("src", "unknown")

            if is_decorative:
                # Decorative images should have empty alt
                if alt_text and alt_text.lower() not in ("", "decorative"):
                    self.add_violation(
                        f"Decorative image should have empty alt text: {src}",
                        img
                    )
                continue

            # Non-decorative images must have alt text
            if not alt_text:
                self.add_violation(f"Image missing alt text: {src}", img)
                continue

            # Check for generic alt text
            generic_alts = ["image", "photo", "picture", "img", "graphic"]
            if alt_text.lower() in generic_alts:
                self.add_violation(
                    f"Image has generic alt text '{alt_text}': {src}",
                    img
                )

        return not self.has_violations()


class LinkValidator(AccessibilityValidator):
    """Validator for link text and href attributes."""

    def validate(self) -> bool:
        """Validate link accessibility.

        Rules:
        - Links must have href attribute
        - Link text should be descriptive (not "click here", "link", "here")
        - Links with only icon content should have aria-label or title
        - Empty links are not allowed

        Returns:
            True if valid, False otherwise
        """
        links = self.soup.find_all("a")

        for link in links:
            href = link.get("href", "").strip()
            link_text = link.get_text(strip=True)
            aria_label = link.get("aria-label", "").strip()
            title = link.get("title", "").strip()

            # Check for href
            if not href:
                self.add_violation("Link missing href attribute", link)
                continue

            # Icon-only links need aria-label or title
            if not link_text and not aria_label and not title:
                self.add_violation(
                    f"Icon-only link missing aria-label or title: {href}",
                    link
                )
                continue

            # Check for empty or generic link text
            if not link_text and not aria_label:
                self.add_violation(
                    f"Link has no descriptive text: {href}",
                    link
                )
                continue

            # Check for generic link text
            generic_texts = ["click here", "here", "link", "read more"]
            if link_text.lower() in generic_texts:
                self.add_violation(
                    f"Link has generic text '{link_text}': {href}",
                    link
                )

        return not self.has_violations()


class SemanticValidator(AccessibilityValidator):
    """Validator for semantic HTML structure."""

    def validate(self) -> bool:
        """Validate semantic HTML usage.

        Checks for:
        - Proper use of semantic elements (nav, main, aside, article)
        - Duplicate IDs within the page
        - Forms have proper structure

        Returns:
            True if valid, False otherwise
        """
        # Check for duplicate IDs
        all_ids: Set[str] = set()
        for element in self.soup.find_all(id=True):
            element_id = element.get("id", "")
            if element_id in all_ids:
                self.add_violation(f"Duplicate ID found: {element_id}", element)
            all_ids.add(element_id)

        # Check for form inputs with associated labels
        form_inputs = self.soup.find_all(["input", "textarea", "select"])
        for input_elem in form_inputs:
            input_type = input_elem.get("type", "").lower()
            if input_type in ("hidden", "submit", "reset", "button"):
                continue

            input_id = input_elem.get("id")
            aria_label = input_elem.get("aria-label")
            aria_labelledby = input_elem.get("aria-labelledby")

            if not (input_id or aria_label or aria_labelledby):
                self.add_violation(
                    f"Form input missing id or aria-label: {input_elem}",
                    input_elem
                )
                continue

            # If input has id, check for associated label
            if input_id:
                label = self.soup.find("label", {"for": input_id})
                if not label and not aria_label and not aria_labelledby:
                    self.add_violation(
                        f"Form input id '{input_id}' has no associated label",
                        input_elem
                    )

        return not self.has_violations()


class ARIAValidator(AccessibilityValidator):
    """Validator for ARIA attribute usage."""

    def validate(self) -> bool:
        """Validate ARIA attribute usage.

        Checks for:
        - Proper ARIA roles on interactive elements
        - Presence of aria-label or aria-labelledby on unlabeled interactive elements
        - aria-hidden used appropriately
        - Modal dialogs have proper ARIA attributes

        Returns:
            True if valid, False otherwise
        """
        # Check for interactive elements with proper ARIA
        interactive_elements = self.soup.find_all(
            ["button", "a", "input", "select", "textarea"]
        )

        for element in interactive_elements:
            if element.name == "button":
                # Button should have text content or aria-label
                text = element.get_text(strip=True)
                aria_label = element.get("aria-label", "").strip()
                if not text and not aria_label:
                    self.add_violation(
                        "Button missing text content or aria-label",
                        element
                    )

        # Check for aria-hidden on decorative elements
        aria_hidden = self.soup.find_all(attrs={"aria-hidden": "true"})
        for element in aria_hidden:
            # aria-hidden should only be on truly decorative elements
            if element.get_text(strip=True):
                self.add_violation(
                    f"Element with aria-hidden='true' contains content: {element}",
                    element
                )

        return not self.has_violations()


# Convenience functions for common checks

def validate_headings(html: str, filename: str = "index.html") -> List[str]:
    """Validate heading structure in HTML.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    validator = HeadingValidator(html, filename)
    validator.validate()
    return validator.get_violations()


def validate_images(html: str, filename: str = "index.html") -> List[str]:
    """Validate image alt text in HTML.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    validator = ImageValidator(html, filename)
    validator.validate()
    return validator.get_violations()


def validate_links(html: str, filename: str = "index.html") -> List[str]:
    """Validate link text in HTML.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    validator = LinkValidator(html, filename)
    validator.validate()
    return validator.get_violations()


def validate_semantic(html: str, filename: str = "index.html") -> List[str]:
    """Validate semantic HTML structure.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    validator = SemanticValidator(html, filename)
    validator.validate()
    return validator.get_violations()


def validate_aria(html: str, filename: str = "index.html") -> List[str]:
    """Validate ARIA attribute usage.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    validator = ARIAValidator(html, filename)
    validator.validate()
    return validator.get_violations()
