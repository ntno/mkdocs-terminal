"""CSS parsing and variable resolution helpers used by accessibility tests."""

from __future__ import annotations

import re
from typing import Dict, Optional

from bs4 import BeautifulSoup, Tag


def extract_css_variables(html: str, css_content: str = "") -> Dict[str, str]:
    """Extract CSS custom properties (variables) from HTML and CSS text.

    Args:
        html: Raw HTML string that may include inline ``<style>`` tags.
        css_content: Optional external CSS text to merge with inline styles.

    Returns:
        Dictionary mapping CSS variable names to their resolved values. Example
        return: ``{"--font-color": "#1a1a1a", "--background-color": "#ffffff"}``.
    """
    variables: Dict[str, str] = {}

    soup = BeautifulSoup(html, "html.parser")
    for style_tag in soup.find_all("style"):
        if style_tag.string:
            variables.update(parse_css_variables(style_tag.string))

    if css_content:
        variables.update(parse_css_variables(css_content))

    resolved: Dict[str, str] = {}
    for var_name, var_value in variables.items():
        resolved[var_name] = resolve_css_variable(var_value, variables)

    return resolved


def parse_css_variables(css_text: str) -> Dict[str, str]:
    """Parse CSS variable definitions from a block of CSS text.

    Args:
        css_text: String containing one or more ``:root`` declarations.

    Returns:
        Dictionary of discovered variables without resolving references.
        Example return: ``{"--font-color": "var(--secondary-color)", "--secondary-color": "#222"}``.
    """
    variables: Dict[str, str] = {}
    root_pattern = r":root\s*\{([^{}]*(?:\{[^}]*\}[^{}]*)*)\}"

    for root_match in re.finditer(root_pattern, css_text, re.DOTALL):
        root_content = root_match.group(1)
        var_pattern = r"--([a-z0-9-]+)\s*:\s*([^;]+);"
        for match in re.finditer(var_pattern, root_content):
            var_name = f"--{match.group(1)}"
            var_value = match.group(2).strip()
            variables[var_name] = var_value

    return variables


def get_element_computed_styles(element: Optional[Tag], css_variables: Dict[str, str]) -> Dict[str, str]:
    """Return basic computed styles for ``color`` and ``background-color``.

    Args:
        element: BeautifulSoup ``Tag`` to inspect. When ``None`` an empty dict is returned.
        css_variables: Map of CSS custom properties used to resolve ``var()`` references.

    Returns:
        Dictionary containing any discovered ``color`` / ``background-color`` values.
        Example return: ``{"color": "#111111", "background-color": "#ffffff"}``.
    """
    styles: Dict[str, str] = {}

    if not element:
        return styles

    style_attr = element.get("style", "")

    if "color:" in style_attr:
        match = re.search(r"(?<!background-)color:\s*([^;]+)", style_attr)
        if match:
            color_value = match.group(1).strip()
            color_value = resolve_css_variable(color_value, css_variables)
            if color_value:
                styles["color"] = color_value

    if "background-color:" in style_attr:
        match = re.search(r"background-color:\s*([^;]+)", style_attr)
        if match:
            bg_value = match.group(1).strip()
            bg_value = resolve_css_variable(bg_value, css_variables)
            if bg_value:
                styles["background-color"] = bg_value

    if "color" not in styles and "--font-color" in css_variables:
        color_value = resolve_css_variable("var(--font-color)", css_variables)
        if color_value:
            styles["color"] = color_value

    if "background-color" not in styles and "--background-color" in css_variables:
        bg_value = resolve_css_variable("var(--background-color)", css_variables)
        if bg_value:
            styles["background-color"] = bg_value

    return styles


def resolve_css_variable(value: str, css_variables: Dict[str, str], max_depth: int = 10) -> Optional[str]:
    """Resolve nested ``var()`` references to their concrete values.

    Args:
        value: Either a raw CSS value (e.g., ``"#fff"``) or ``var(--token)``.
        css_variables: Dictionary of available variable definitions.
        max_depth: Safety ceiling for recursive resolution (defaults to 10).

    Returns:
        Resolved string value or ``None`` when the reference cannot be satisfied.
        Example return: passing ``"var(--font-color)"`` with ``{"--font-color": "#000"}``
        yields ``"#000"``.
    """
    if max_depth <= 0:
        return None

    value = value.strip()
    var_match = re.match(r"var\(--([a-z0-9-]+)\)", value)
    if var_match:
        var_name = f"--{var_match.group(1)}"
        if var_name in css_variables:
            return resolve_css_variable(css_variables[var_name].strip(), css_variables, max_depth - 1)
        return None

    return value


def extract_css_attributes(css_content: str, fallback_css_content: str = "") -> Dict[str, str]:
    """Resolve theme CSS attributes (font/color tokens) from CSS content.

    Args:
        css_content: Palette-specific CSS text that may override defaults.
        fallback_css_content: Base theme CSS used when an attribute is missing.

    Returns:
        Dictionary keyed by attribute name (no leading ``--``) with resolved values.
        Example return: ``{"background-color": "#0d1117", "font-color": "#e6edf3"}``.
    """
    attributes_to_extract = [
        "global-font-size",
        "global-line-height",
        "global-space",
        "font-stack",
        "mono-font-stack",
        "background-color",
        "page-width",
        "font-color",
        "invert-font-color",
        "secondary-color",
        "tertiary-color",
        "primary-color",
        "error-color",
        "progress-bar-background",
        "progress-bar-fill",
        "code-bg-color",
        "code-font-color",
        "block-background-color",
        "input-style",
        "display-h1-decoration",
    ]

    all_variables: Dict[str, str] = {}
    var_pattern = r"--([a-z0-9\-]+):\s*([^;]+);"
    for match in re.finditer(var_pattern, css_content, re.IGNORECASE):
        var_name = match.group(1)
        var_value = match.group(2).strip()
        all_variables[f"--{var_name}"] = var_value

    fallback_variables: Dict[str, str] = {}
    if fallback_css_content:
        for match in re.finditer(var_pattern, fallback_css_content, re.IGNORECASE):
            var_name = match.group(1)
            var_value = match.group(2).strip()
            fallback_variables[f"--{var_name}"] = var_value

    result: Dict[str, str] = {}

    combined_variables: Dict[str, str] = dict(fallback_variables)
    combined_variables.update(all_variables)
    for attr in attributes_to_extract:
        var_name = f"--{attr}"
        if var_name in all_variables:
            resolved_value = resolve_css_variable(all_variables[var_name], combined_variables)
            if resolved_value:
                result[attr] = resolved_value
                continue

        if var_name in fallback_variables:
            resolved_value = resolve_css_variable(fallback_variables[var_name], combined_variables)
            if resolved_value:
                result[attr] = resolved_value

    return result


__all__ = [
    "extract_css_variables",
    "parse_css_variables",
    "get_element_computed_styles",
    "resolve_css_variable",
    "extract_css_attributes",
]
