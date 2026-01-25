"""HTML structure and semantic validation helpers for accessibility tests."""

from __future__ import annotations

from typing import List, Set

from bs4 import BeautifulSoup, Tag
from tidylib import tidy_document

from .helpers import format_violation


def validate_duplicate_ids(html: str, filename: str = "index.html") -> List[str]:
    """Validate that no duplicate IDs exist in the provided HTML."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    all_ids: Set[str] = set()
    for element in soup.find_all(id=True):
        element_id = element.get("id", "")
        if element_id in all_ids:
            violations.append(format_violation(f"Duplicate ID found: {element_id}", filename, element))
        all_ids.add(element_id)

    return violations


def validate_semantic_html(html: str, filename: str = "index.html") -> List[str]:
    """Validate semantic HTML structure for the theme output."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    main_elements = soup.find_all("main")
    if len(main_elements) != 1:
        violations.append(
            format_violation(
                f"Expected exactly 1 <main> element, found {len(main_elements)}",
                filename,
            )
        )

    if main_elements:
        main_elem = main_elements[0]
        if main_elem.parent.name != "body":
            violations.append(
                format_violation(
                    f"<main> should be direct child of <body>, found parent: {main_elem.parent.name}",
                    filename,
                    main_elem,
                )
            )

    nav_elements = soup.find_all("nav")
    if len(nav_elements) > 1:
        for nav in nav_elements:
            if not nav.get("aria-label"):
                violations.append(
                    format_violation(
                        "Multiple <nav> elements should have aria-label to distinguish them",
                        filename,
                        nav,
                    )
                )

    if main_elements:
        main_elem = main_elements[0]

        header_in_main = main_elem.find("header")
        if header_in_main:
            violations.append(
                format_violation(
                    "<header> should not be nested inside <main> (should be theme header outside main content)",
                    filename,
                    header_in_main,
                )
            )

        footer_in_main = main_elem.find("footer")
        if footer_in_main:
            violations.append(
                format_violation(
                    "<footer> should not be nested inside <main> (should be theme footer outside main content)",
                    filename,
                    footer_in_main,
                )
            )

    return violations


def validate_html_structure(html: str, filename: str = "index.html") -> List[str]:
    """Validate HTML5 structure and element nesting using HTML Tidy."""
    violations: List[str] = []

    tidy_options = {
        "doctype": "html5",
    }

    _, errors = tidy_document(html, options=tidy_options)
    error_lines = errors.strip().split("\n") if errors.strip() else []
    for error in error_lines:
        if not error:
            continue

        is_structural_issue = any(
            keyword in error.lower()
            for keyword in [
                "unexpected",
                "missing </",
                "previously",
                "discarding",
                "occurs after end",
            ]
        )

        if is_structural_issue:
            violations.append(format_violation(error, filename))

    return violations
