"""Contrast validation helpers shared across accessibility tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from bs4 import BeautifulSoup

from tests.accessibility.utilities import extract_css_variables, get_element_computed_styles
from tests.accessibility.utilities.color_utils import get_contrast_ratio, meets_wcag_aa
from .helpers import format_violation


@dataclass
class PaletteColors:
    """Normalized palette attributes used throughout contrast tests."""

    palette_name: str
    font_color: str
    background_color: str
    invert_font_color: Optional[str] = None
    primary_color: Optional[str] = None
    error_color: Optional[str] = None
    secondary_color: Optional[str] = None
    code_font_color: Optional[str] = None
    code_background_color: Optional[str] = None
    font_size: float = 14.0


def get_palette_colors(
    palette_name: str,
    all_palette_css_attributes: Dict[str, Dict[str, str]],
    required_attrs: Optional[Sequence[str]] = None,
) -> PaletteColors:
    """Resolve palette attributes from the shared CSS attribute fixture."""
    palette_attributes = all_palette_css_attributes.get(palette_name)
    assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"

    font_color = palette_attributes.get("font-color")
    background_color = palette_attributes.get("background-color")
    invert_font_color = palette_attributes.get("invert-font-color")

    assert font_color is not None, f"No font-color defined for palette: {palette_name}"
    assert background_color is not None, f"No background-color defined for palette: {palette_name}"

    font_size_str = palette_attributes.get("global-font-size", "14px")
    font_size = float(font_size_str.replace("px", "").strip())

    primary_color = palette_attributes.get("primary-color")
    error_color = palette_attributes.get("error-color")
    secondary_color = palette_attributes.get("secondary-color")
    code_font_color = palette_attributes.get("code-font-color")
    code_background_color = palette_attributes.get("code-bg-color")

    if required_attrs:
        for attr in required_attrs:
            assert palette_attributes.get(attr) is not None, f"No {attr} defined for palette: {palette_name}"

    return PaletteColors(
        palette_name=palette_name,
        font_color=font_color,
        background_color=background_color,
        invert_font_color=invert_font_color,
        primary_color=primary_color,
        error_color=error_color,
        secondary_color=secondary_color,
        code_font_color=code_font_color,
        code_background_color=code_background_color,
        font_size=font_size,
    )


def assert_contrast_meets_wcag_aa(
    fg_color: str,
    bg_color: str,
    font_size: float,
    context: str,
    is_bold: bool = False,
) -> None:
    """Assert that a foreground/background pair satisfies WCAG AA contrast rules."""
    ratio = get_contrast_ratio(fg_color, bg_color)
    assert ratio is not None, f"Could not calculate contrast ratio for {fg_color} on {bg_color}"

    is_compliant = meets_wcag_aa(ratio, text_size=font_size, is_bold=is_bold)
    required = 3.0 if (font_size >= 24 or (is_bold and font_size >= 18.67)) else 4.5

    assert is_compliant, (
        f"{context} {fg_color} on {bg_color} has contrast {ratio:.2f}:1, "
        f"does not meet WCAG 2.1 AA minimum of {required}:1 for {font_size}px text"
    )


def validate_color_contrast(html: str, filename: str = "index.html", css_content: str = "") -> List[str]:
    """Validate color contrast meets WCAG 2.1 AA standards for theme elements."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    css_variables = extract_css_variables(html, css_content)

    body = soup.find("body")
    body_styles = get_element_computed_styles(body, css_variables) if body else {}
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

        element_styles = get_element_computed_styles(element, css_variables)
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
                format_violation(
                    f"Insufficient color contrast on {element_desc}: {ratio:.2f}:1 "
                    f"(need {4.5 if not is_large_text else 3.0}:1 for WCAG AA). "
                    f"Color: {fg_color}, Background: {bg_color}",
                    filename,
                    element,
                )
            )

    return violations


__all__ = [
    "validate_color_contrast",
    "PaletteColors",
    "assert_contrast_meets_wcag_aa",
    "get_palette_colors",
]
