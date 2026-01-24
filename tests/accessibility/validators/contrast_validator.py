"""Contrast validation helpers shared across accessibility tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set, Tuple

from bs4 import BeautifulSoup, Tag

from tests.accessibility.utilities import _extract_css_variables, _get_element_computed_styles
from tests.accessibility.utilities.color_utils import get_contrast_ratio, meets_wcag_aa
from .helpers import _format_violation


@dataclass
class PaletteColors:
    """Normalized palette attributes used throughout contrast tests."""

    palette_name: str
    font_color: str
    background_color: str
    primary_color: Optional[str] = None
    error_color: Optional[str] = None
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

    assert font_color is not None, f"No font-color defined for palette: {palette_name}"
    assert background_color is not None, f"No background-color defined for palette: {palette_name}"

    font_size_str = palette_attributes.get("global-font-size", "14px")
    font_size = float(font_size_str.replace("px", "").strip())

    primary_color = palette_attributes.get("primary-color")
    error_color = palette_attributes.get("error-color")

    if required_attrs:
        for attr in required_attrs:
            assert palette_attributes.get(attr) is not None, f"No {attr} defined for palette: {palette_name}"

    return PaletteColors(
        palette_name=palette_name,
        font_color=font_color,
        background_color=background_color,
        primary_color=primary_color,
        error_color=error_color,
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


class BackgroundColorResolver:
    """Resolves effective background colors for BeautifulSoup elements."""

    def __init__(self, css_variables: Dict[str, str], soup: BeautifulSoup, default: str = "#ffffff") -> None:
        self._css_variables = css_variables
        self._soup = soup
        self._default = default

    def resolve(self, element: Tag) -> Optional[str]:
        bg_color = self._resolve_from_element(element)
        if bg_color and bg_color != "transparent":
            return bg_color

        parent = element.parent
        while parent is not None:
            bg_color = self._resolve_from_element(parent)
            if bg_color and bg_color != "transparent":
                return bg_color
            parent = parent.parent

        body = self._soup.find("body")
        if body:
            body_styles = _get_element_computed_styles(body, self._css_variables)
            body_color = body_styles.get("background-color")
            if body_color:
                return body_color
        return self._default

    def _resolve_from_element(self, element: Optional[Tag]) -> Optional[str]:
        styles = _get_element_computed_styles(element, self._css_variables)
        return styles.get("background-color")


@dataclass
class ColorCombination:
    """Tracks occurrences of fore/back color pairs whilst scanning a site."""

    fg_color: str
    bg_color: str
    count: int = 0
    locations: List[str] = field(default_factory=list)
    element_types: Set[str] = field(default_factory=set)

    def add_occurrence(self, location: str, element_type: Optional[str] = None) -> None:
        self.count += 1
        self.locations.append(location)
        if element_type:
            self.element_types.add(element_type)


class ColorCombinationTracker:
    """Collects unique color combinations and reports those below the threshold."""

    def __init__(self) -> None:
        self._combinations: Dict[Tuple[str, str], ColorCombination] = {}

    def add(self, fg_color: str, bg_color: str, location: str, element_type: Optional[str] = None) -> None:
        key = (fg_color.lower(), bg_color.lower())
        if key not in self._combinations:
            self._combinations[key] = ColorCombination(fg_color=fg_color.lower(), bg_color=bg_color.lower())
        self._combinations[key].add_occurrence(location, element_type)

    def get_failures(self, min_ratio: float = 4.5) -> List[str]:
        failures: List[str] = []
        for combo in self._combinations.values():
            ratio = get_contrast_ratio(combo.fg_color, combo.bg_color)
            if ratio is None or ratio >= min_ratio:
                continue

            locations_preview = ", ".join(combo.locations[:3])
            if len(combo.locations) > 3:
                locations_preview += f" (+{len(combo.locations) - 3} more)"

            message = f"Color {combo.fg_color} on {combo.bg_color} = {ratio:.2f}:1 (need {min_ratio}:1)"
            if combo.element_types:
                message += f" - Elements: {', '.join(sorted(combo.element_types))}"
            message += f" - Found {combo.count} times"
            if locations_preview:
                message += f" - Examples: {locations_preview}"
            failures.append(message)
        return failures


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


__all__ = [
    "BackgroundColorResolver",
    "ColorCombination",
    "ColorCombinationTracker",
    "validate_color_contrast",
    "PaletteColors",
    "assert_contrast_meets_wcag_aa",
    "get_palette_colors",
]
