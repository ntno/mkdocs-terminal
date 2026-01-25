"""Accessibility validator helpers exposed for tests."""

from .aria_validator import (
    validate_aria_buttons,
    validate_aria_hidden,
    validate_form_labels,
    validate_link_text,
    validate_search_modal_accessibility,
)
from .contrast_validator import (
    PaletteColors,
    assert_contrast_meets_wcag_aa,
    get_palette_colors,
    validate_color_contrast,
)
from .helpers import format_violation
from .html_validator import (
    validate_duplicate_ids,
    validate_html_structure,
    validate_semantic_html,
)

__all__ = [
    "format_violation",
    "validate_color_contrast",
    "PaletteColors",
    "assert_contrast_meets_wcag_aa",
    "get_palette_colors",
    "validate_duplicate_ids",
    "validate_html_structure",
    "validate_semantic_html",
    "validate_aria_buttons",
    "validate_aria_hidden",
    "validate_form_labels",
    "validate_link_text",
    "validate_search_modal_accessibility",
]
