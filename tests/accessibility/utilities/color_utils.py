"""Color utility functions for WCAG contrast validation.

This module provides color parsing and contrast ratio calculation functions
for validating WCAG 2.1 AA color contrast compliance.

Design Decision: Using Python's standard library colorsys instead of external
libraries like wcag-contrast-ratio (last updated 2015) or colour (last updated 2017)
because these PyPI packages are no longer actively maintained. The relative luminance
formula is straightforward and well-documented by W3C, making a custom implementation
both maintainable and reliable.

Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
"""

import re
from typing import Tuple, Optional
import colorsys


# CSS named colors mapping (subset of most common colors in themes)
CSS_NAMED_COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "gray": "#808080",
    "grey": "#808080",
    "silver": "#c0c0c0",
    "maroon": "#800000",
    "olive": "#808000",
    "lime": "#00ff00",
    "aqua": "#00ffff",
    "teal": "#008080",
    "navy": "#000080",
    "fuchsia": "#ff00ff",
    "purple": "#800080",
    "orange": "#ffa500",
    "transparent": None,
}


def normalize_color(color_str: str) -> Optional[Tuple[float, float, float]]:
    """Convert a CSS color string to an RGB tuple on the 0.0-1.0 scale.

    Supports multiple color formats:
    - Hex: #fff, #ffffff, #FFF, #FFFFFF
    - RGB: rgb(255, 0, 0), rgb(100%, 0%, 0%)
    - HSL: hsl(0, 100%, 50%), hsl(0deg, 100%, 50%)
    - Named colors: white, black, red, etc.

    Args:
        color_str: Color string in any supported format (hex/rgb/hsl/named value).

    Returns:
        Tuple of `(red, green, blue)` with float values 0.0-1.0, or `None` if the
        color represents transparency or cannot be parsed. Example: `"#ff0000"`
        returns `(1.0, 0.0, 0.0)`.
    """
    if not color_str or not isinstance(color_str, str):
        return None

    color_str = color_str.strip().lower()

    # Handle transparent
    if color_str in ("transparent", "rgba(0,0,0,0)"):
        return None

    # Handle hex colors
    hex_match = re.match(r"^#([0-9a-f]{3}|[0-9a-f]{6})$", color_str)
    if hex_match:
        hex_value = hex_match.group(1)
        # Expand 3-digit hex to 6-digit
        if len(hex_value) == 3:
            hex_value = "".join([c * 2 for c in hex_value])
        r = int(hex_value[0:2], 16) / 255.0
        g = int(hex_value[2:4], 16) / 255.0
        b = int(hex_value[4:6], 16) / 255.0
        return (r, g, b)

    # Handle rgb() notation
    rgb_match = re.match(r"^rgba?\s*\(\s*(\d+(?:\.\d+)?%?)\s*,\s*(\d+(?:\.\d+)?%?)\s*,\s*(\d+(?:\.\d+)?%?)\s*(?:,\s*[\d.]+)?\s*\)$", color_str)
    if rgb_match:
        r_str, g_str, b_str = rgb_match.groups()
        r = parse_color_value(r_str)
        g = parse_color_value(g_str)
        b = parse_color_value(b_str)
        if r is not None and g is not None and b is not None:
            return (r, g, b)

    # Handle hsl() notation
    hsl_match = re.match(r"^hsla?\s*\(\s*([\d.]+)(?:deg)?\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*(?:,\s*[\d.]+)?\s*\)$", color_str)
    if hsl_match:
        h_str, s_str, l_str = hsl_match.groups()
        h = float(h_str) / 360.0  # Convert to 0-1 range
        s = float(s_str) / 100.0
        l = float(l_str) / 100.0
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (r, g, b)

    # Handle named colors
    if color_str in CSS_NAMED_COLORS:
        named_color = CSS_NAMED_COLORS[color_str]
        if named_color is None:
            return None
        return normalize_color(named_color)

    # Unknown color format
    return None


def parse_color_value(value_str: str) -> Optional[float]:
    """Parse a numeric RGB component from decimal or percentage notation.

    Args:
        value_str: Raw component value such as "255", "100%", or "50".

    Returns:
        Float between 0.0 and 1.0 when the value is valid, or `None` if parsing
        fails. Example: `"128"` returns approximately `0.50196`.
    """
    value_str = value_str.strip()
    try:
        if "%" in value_str:
            return float(value_str.rstrip("%")) / 100.0
        else:
            return float(value_str) / 255.0
    except ValueError:
        return None


def get_relative_luminance(rgb: Tuple[float, float, float]) -> float:
    """Calculate relative luminance per the WCAG 2.1 definition.

    The relative luminance of a color is defined as:
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B

    where R, G, and B are defined as:
    - if RsRGB <= 0.03928 then R = RsRGB/12.92 else R = ((RsRGB+0.055)/1.055) ^ 2.4

    Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html

    Args:
        rgb: Tuple of `(red, green, blue)` values already normalized to 0.0-1.0.

    Returns:
        Relative luminance value between 0.0 and 1.0. Example: `(1.0, 1.0, 1.0)`
        returns `1.0`, while `(0.0, 0.0, 0.0)` returns `0.0`.
    """
    r, g, b = rgb

    # Apply gamma correction
    r = linearize_color_component(r)
    g = linearize_color_component(g)
    b = linearize_color_component(b)

    # Calculate relative luminance
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance


def linearize_color_component(value: float) -> float:
    """Apply WCAG gamma correction to a single color component.

    Args:
        value: Component value between 0.0 and 1.0 in sRGB space.

    Returns:
        Gamma-corrected component value suitable for luminance calculations.
        Example: an input of `0.02` returns approximately `0.00154`.
    """
    if value <= 0.03928:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4


def get_contrast_ratio(color1: str, color2: str) -> Optional[float]:
    """Calculate the WCAG 2.1 contrast ratio for two CSS color strings.

    The contrast ratio is defined as:
    (L1 + 0.05) / (L2 + 0.05)

    where L1 is the relative luminance of the lighter color and
    L2 is the relative luminance of the darker color.

    Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html

    Args:
        color1: First color string (hex, rgb, hsl, named, etc.).
        color2: Second color string in any supported format.

    Returns:
        Float contrast ratio (e.g., `4.5` for a 4.5:1 ratio), or `None` if either
        color cannot be parsed. Example: `("#000000", "#ffffff")` returns `21.0`.
    """
    rgb1 = normalize_color(color1)
    rgb2 = normalize_color(color2)

    if rgb1 is None or rgb2 is None:
        return None

    l1 = get_relative_luminance(rgb1)
    l2 = get_relative_luminance(rgb2)

    # Ensure L1 is the lighter color
    if l1 < l2:
        l1, l2 = l2, l1

    return (l1 + 0.05) / (l2 + 0.05)


def meets_wcag_aa(ratio: Optional[float], text_size: int = 14, is_bold: bool = False) -> bool:
    """Check whether a contrast ratio satisfies the WCAG 2.1 AA thresholds.

    WCAG 2.1 AA standards:
    - Normal text (< 18pt or < 14pt bold): Minimum 4.5:1
    - Large text (≥ 18pt or ≥ 14pt bold): Minimum 3:1
    - UI components (buttons, form fields): Minimum 3:1

    Args:
        ratio: Contrast ratio (e.g., `4.5`), or `None` when calculation failed.
        text_size: Font size in pixels (defaults to 14px for normal body text).
        is_bold: Indicates whether the text uses bold weight (defaults to False).

    Returns:
        True when the ratio meets the appropriate WCAG AA threshold for the font
        size/weight combination, otherwise False. Example: `ratio=4.5,
        text_size=14` returns `True`, while `ratio=3.0, text_size=14` returns
        `False`.
    """
    if ratio is None:
        return False

    # Determine if this is "large text"
    # 18pt ≈ 24px, 14pt ≈ 18.67px
    # Using: 18pt = 24px, 14pt bold = 18.67px (approximately)
    is_large_text = (text_size >= 24) or (is_bold and text_size >= 18.67)

    if is_large_text:
        return ratio >= 3.0
    else:
        return ratio >= 4.5
