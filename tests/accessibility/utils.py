"""Shared accessibility helpers and compatibility re-exports.

This module now acts as a thin facade that re-exports validator and utility
functions from their dedicated modules. Tests that previously imported helpers
from ``tests.accessibility.utils`` can continue to do so while we gradually
refactor the internal structure.
"""

from __future__ import annotations

from typing import List

from bs4 import BeautifulSoup

from tests.accessibility.utilities import (
    _extract_css_variables,
    _get_element_computed_styles,
    extract_css_attributes as _extract_css_attributes_public,
)
from tests.accessibility.utilities.color_utils import get_contrast_ratio, meets_wcag_aa
from tests.accessibility.validators import (
    _format_violation,
    validate_aria_buttons as _validate_aria_buttons,
    validate_aria_hidden as _validate_aria_hidden,
    validate_duplicate_ids as _validate_duplicate_ids,
    validate_form_labels as _validate_form_labels,
    validate_html_structure as _validate_html_structure,
    validate_link_text as _validate_link_text,
    validate_modal_accessibility as _validate_modal_accessibility,
    validate_semantic_html as _validate_semantic_html,
)

__all__ = [
    "validate_duplicate_ids",
    "validate_semantic_html",
    "validate_html_structure",
    "validate_aria_buttons",
    "validate_aria_hidden",
    "validate_modal_accessibility",
    "validate_form_labels",
    "validate_link_text",
    "extract_css_attributes",
    "validate_color_contrast",
]


validate_duplicate_ids = _validate_duplicate_ids
validate_semantic_html = _validate_semantic_html
validate_html_structure = _validate_html_structure
validate_aria_buttons = _validate_aria_buttons
validate_aria_hidden = _validate_aria_hidden
validate_modal_accessibility = _validate_modal_accessibility
validate_form_labels = _validate_form_labels
validate_link_text = _validate_link_text
extract_css_attributes = _extract_css_attributes_public


# Existing color contrast validation ------------------------------------------------------
def validate_color_contrast(html: str, filename: str = "index.html", css_content: str = "") -> List[str]:
    """Validate color contrast meets WCAG 2.1 AA standards for theme elements."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    css_variables = _extract_css_variables(html, css_content)

    body = soup.find("body")
    body_styles = _get_element_computed_styles(body, css_variables) if body else {}
    body_bg_color = body_styles.get("background-color")

    if not body_bg_color:
        return violations

    elements_to_check = soup.find_all([
        "body",
        "p",
        "a",
        "button",
        "input",
        "label",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
    ])

    for element in elements_to_check:
        text_content = element.get_text(strip=True)
        if not text_content:
            continue

        element_styles = _get_element_computed_styles(element, css_variables)
        fg_color = element_styles.get("color")
        if not fg_color:
            continue

        bg_color = element_styles.get("background-color") or body_bg_color

        ratio = get_contrast_ratio(fg_color, bg_color)

        is_large_text = element.name in ["h1", "h2", "h3"]
        text_size = 24 if is_large_text else 14

        if ratio is not None and not meets_wcag_aa(ratio, text_size=text_size):
            element_desc = element.name
            if element_desc == "a":
                element_desc = f"link (text: {text_content[:30]})"
            elif element_desc in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                element_desc = f"{element_desc} heading"
            elif element_desc in ["button", "input", "label"]:
                element_desc = f"{element_desc} element"

            violations.append(
                _format_violation(
                    f"Insufficient color contrast on {element_desc}: {ratio:.2f}:1 "
                    f"(need {4.5 if not is_large_text else 3.0}:1 for WCAG AA). "
                    f"Color: {fg_color}, Background: {bg_color}",
                    filename,
                    element,
                )
            )

    return violations



