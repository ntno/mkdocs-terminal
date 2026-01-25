"""ARIA attribute validation helpers for accessibility tests."""

from __future__ import annotations

from typing import List

from bs4 import BeautifulSoup

from .helpers import format_violation


def validate_aria_buttons(html: str, filename: str = "index.html") -> List[str]:
    """Check that all <button> elements have text content or aria-label."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.find_all("button"):
        text = element.get_text(strip=True)
        aria_label = element.get("aria-label", "").strip()
        if not text and not aria_label:
            violations.append(
                format_violation(
                    "Button missing text content or aria-label",
                    filename,
                    element,
                )
            )
    return violations


def validate_aria_hidden(html: str, filename: str = "index.html") -> List[str]:
    """Check that aria-hidden is only used on decorative elements."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    for element in soup.find_all(attrs={"aria-hidden": "true"}):
        element_text = element.get_text(strip=True)
        if element_text:
            violations.append(
                format_violation(
                    "Element with aria-hidden='true' contains text. Use aria-label for icon buttons instead.",
                    filename,
                    element,
                )
            )

    return violations


def validate_modal_accessibility(html: str, filename: str = "index.html") -> List[str]:
    """Validate search modal has proper ARIA attributes for accessibility."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    modal = soup.find(id="mkdocs_search_modal")
    if not modal:
        return violations

    modal_role = modal.get("role", "").lower()
    if modal_role not in ("alertdialog", "dialog"):
        violations.append(
            format_violation(
                f"Modal should have role='alertdialog' or role='dialog', found role='{modal_role}'",
                filename,
                modal,
            )
        )

    if modal.get("aria-modal", "").lower() != "true":
        violations.append(format_violation("Modal missing aria-modal='true'", filename, modal))

    labelledby = modal.get("aria-labelledby", "").strip()
    if not labelledby:
        violations.append(format_violation("Modal missing aria-labelledby pointing to modal title", filename, modal))
    else:
        label_elem = soup.find(id=labelledby)
        if not label_elem:
            violations.append(
                format_violation(
                    f"Modal aria-labelledby='{labelledby}' references non-existent element",
                    filename,
                    modal,
                )
            )

    close_button = modal.find("button", class_="close")
    if close_button and not close_button.get("aria-label", "").strip():
        violations.append(format_violation("Modal close button missing aria-label", filename, close_button))

    search_input = modal.find("input", {"type": "search"})
    if search_input:
        labelledby = search_input.get("aria-labelledby", "").strip()
        if not labelledby:
            violations.append(
                format_violation("Search input missing aria-labelledby association", filename, search_input)
            )
        else:
            label_elem = soup.find(id=labelledby)
            if not label_elem:
                violations.append(
                    format_violation(
                        f"Search input aria-labelledby='{labelledby}' references non-existent element",
                        filename,
                        search_input,
                    )
                )

    return violations


def validate_form_labels(html: str, filename: str = "index.html") -> List[str]:
    """Validate that form inputs have associated labels or accessible names."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    inputs = soup.find_all(["input", "textarea", "select"])
    for input_elem in inputs:
        input_type = input_elem.get("type", "text").lower()
        if input_type in ("hidden", "submit", "button", "reset", "image"):
            continue

        input_id = input_elem.get("id", "")
        has_label = False
        if input_id:
            label = soup.find("label", {"for": input_id})
            if label:
                has_label = True

        aria_label = input_elem.get("aria-label", "").strip()
        aria_labelledby = input_elem.get("aria-labelledby", "").strip()
        has_aria_name = bool(aria_label or aria_labelledby)

        has_title = bool(input_elem.get("title", "").strip())

        if not (has_label or has_aria_name or has_title):
            violations.append(
                format_violation(
                    f"Form input of type '{input_type}' missing accessible label. "
                    f"Use <label for='{input_id}'>, aria-label, or aria-labelledby.",
                    filename,
                    input_elem,
                )
            )

    return violations


def validate_link_text(html: str, filename: str = "index.html") -> List[str]:
    """Validate that navigation/footer links have descriptive text or aria-label."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    theme_regions = soup.find_all(["nav", "header", "footer", "aside"])
    links = []
    for region in theme_regions:
        links.extend(region.find_all("a"))

    for link in links:
        link_text = link.get_text(strip=True)
        aria_label = link.get("aria-label", "").strip()
        if not link_text and not aria_label:
            violations.append(format_violation("Link missing text content and aria-label", filename, link))

    return violations
