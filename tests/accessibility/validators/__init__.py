"""Accessibility validator helpers exposed for tests."""

from .html_validator import (
    validate_duplicate_ids,
    validate_semantic_html,
    validate_html_structure,
)
from .aria_validator import (
    validate_aria_buttons,
    validate_aria_hidden,
    validate_modal_accessibility,
    validate_form_labels,
    validate_link_text,
)
from .helpers import _format_violation

__all__ = [
    "_format_violation",
    "validate_duplicate_ids",
    "validate_semantic_html",
    "validate_html_structure",
    "validate_aria_buttons",
    "validate_aria_hidden",
    "validate_modal_accessibility",
    "validate_form_labels",
    "validate_link_text",
]
