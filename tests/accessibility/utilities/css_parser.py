"""CSS parsing and variable resolution helpers used by accessibility tests.

This module provides utilities for parsing CSS files and simulating browser CSS
cascade behavior for testing the palette selector architecture.

Key concepts:

1. **Attribute Selector Parsing**: With the introduction of a palette selector, 
    the new palette architecture uses `[data-palette="name"]` scoping instead of 
    `:root` blocks. The parser must extract variables from both selector types.

2. **CSS Cascade Simulation**: To test a palette, we load the full cascade:
   terminal.css → theme.css → palette file, mimicking browser behavior.

3. **Variable Resolution**: The compatibility layer in theme.css maps legacy
   variables (--font-color) to namespaced ones (--mkdocs-terminal-font-color)
   with fallbacks. Tests must resolve through this chain.

Usage:

    # Test a specific palette with full cascade
    context = load_palette_context("dark")
    assert context["font-color"] == "#e8e9ed"

    # Extract variables from a specific [data-palette] block
    attrs = extract_css_attributes_from_palette(
        css_content,
        data_palette="gruvbox_dark"
    )
"""

from __future__ import annotations

import re
from pathlib import Path
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


def parse_data_palette_variables(css_text: str, palette_name: str) -> Dict[str, str]:
    """Parse CSS variables from a [data-palette="name"] attribute selector block.

    This function extracts variables defined within attribute selector blocks,
    which is how the palette selector architecture scopes palette-specific
    variable overrides.

    Args:
        css_text: CSS content containing [data-palette] blocks.
        palette_name: The palette name to extract (e.g., "dark", "gruvbox_dark").

    Returns:
        Dictionary of variables defined in the matching [data-palette] block.
        Returns empty dict if no matching block found.

    Example:
        >>> css = '''
        ... [data-palette="dark"] {
        ...   --mkdocs-terminal-font-color: #e8e9ed;
        ...   --font-color: var(--mkdocs-terminal-font-color);
        ... }
        ... '''
        >>> parse_data_palette_variables(css, "dark")
        {'--mkdocs-terminal-font-color': '#e8e9ed', '--font-color': 'var(--mkdocs-terminal-font-color)'}
    """
    variables: Dict[str, str] = {}
    
    # Match [data-palette="name"] { ... } blocks
    # Pattern explanation:
    # - \[data-palette="palette_name"\]: Match the attribute selector
    # - \s*\{: Allow whitespace before opening brace
    # - ([^{}]*(?:\{[^}]*\}[^{}]*)*): Capture block content (allows nested braces)
    # - \}: Match closing brace
    pattern = rf'\[data-palette="{re.escape(palette_name)}"\]\s*\{{([^{{}}]*(?:\{{[^}}]*\}}[^{{}}]*)*)\}}'
    
    for match in re.finditer(pattern, css_text, re.DOTALL):
        block_content = match.group(1)
        var_pattern = r"--([a-z0-9-]+)\s*:\s*([^;]+);"
        for var_match in re.finditer(var_pattern, block_content):
            var_name = f"--{var_match.group(1)}"
            var_value = var_match.group(2).strip()
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

    Supports CSS variable fallback syntax: var(--name, fallback-value).
    If the variable is not found, the fallback value is used.

    Args:
        value: Either a raw CSS value (e.g., ``"#fff"``), ``var(--token)``, or
              ``var(--token, fallback)``.
        css_variables: Dictionary of available variable definitions.
        max_depth: Safety ceiling for recursive resolution (defaults to 10).

    Returns:
        Resolved string value or ``None`` when the reference cannot be satisfied.
        Example return: passing ``"var(--font-color)"`` with ``{"--font-color": "#000"}``
        yields ``"#000"``. Passing ``"var(--missing, #fff)"`` yields ``"#fff"``.
    """
    if max_depth <= 0:
        return None

    value = value.strip()
    
    # Match var() with optional fallback: var(--name) or var(--name, fallback)
    var_match = re.match(r"var\(--([a-z0-9-]+)(?:\s*,\s*([^)]+))?\)", value)
    if var_match:
        var_name = f"--{var_match.group(1)}"
        fallback_value = var_match.group(2)  # Can be None if no fallback
        
        if var_name in css_variables:
            # Variable found, resolve it (may itself contain var references)
            return resolve_css_variable(css_variables[var_name].strip(), css_variables, max_depth - 1)
        elif fallback_value:
            # Variable not found, use fallback (may contain var references)
            return resolve_css_variable(fallback_value.strip(), css_variables, max_depth - 1)
        else:
            # Variable not found, no fallback
            return None

    return value


def load_palette_context(palette_name: str) -> Dict[str, str]:
    """Load complete CSS cascade for a palette and resolve all variables.

    This function simulates browser CSS cascade behavior by loading files in
    the correct order (terminal.css → theme.css → palette file) and applying
    CSS specificity rules to resolve variable values.

    The cascade works as follows:
    1. Load terminal.css :root (legacy glue variables only)
    2. Load theme.css :root (compatibility layer with fallbacks)
    3. Load palette :root (color constants)
    4. Load palette [data-palette] block (variable mappings - highest specificity)

    Args:
        palette_name: Name of the palette to load (e.g., "dark", "default", "gruvbox_dark").

    Returns:
        Dictionary mapping attribute names (without --) to resolved values.
        Example: {"font-color": "#e8e9ed", "background-color": "#222225"}

    Raises:
        FileNotFoundError: If required CSS files don't exist.

    Example:
        >>> context = load_palette_context("dark")
        >>> context["font-color"]
        '#e8e9ed'
        >>> context["background-color"]
        '#222225'
    """
    terminal_css = Path("terminal/css/terminal.css")
    theme_css = Path("terminal/css/theme.css")
    palette_css = Path(f"terminal/css/palettes/{palette_name}.css")

    if not terminal_css.exists():
        raise FileNotFoundError(f"Terminal CSS not found: {terminal_css}")
    if not theme_css.exists():
        raise FileNotFoundError(f"Theme CSS not found: {theme_css}")
    if not palette_css.exists():
        raise FileNotFoundError(f"Palette CSS not found: {palette_css}")

    with open(terminal_css) as f:
        terminal_content = f.read()
    with open(theme_css) as f:
        theme_content = f.read()
    with open(palette_css) as f:
        palette_content = f.read()

    # Build variable context with CSS cascade specificity
    # Start with lowest specificity (:root from terminal.css)
    all_variables: Dict[str, str] = {}
    all_variables.update(parse_css_variables(terminal_content))
    
    # Layer 2: theme.css :root (same specificity, but loads later → wins)
    all_variables.update(parse_css_variables(theme_content))
    
    # Layer 3: palette :root (color constants - same specificity, loads later)
    all_variables.update(parse_css_variables(palette_content))
    
    # Layer 4: [data-palette] block (HIGHER specificity → always wins)
    palette_vars = parse_data_palette_variables(palette_content, palette_name)
    all_variables.update(palette_vars)

    # Resolve all variables through the cascade
    resolved_variables: Dict[str, str] = {}
    for var_name, var_value in all_variables.items():
        resolved_value = resolve_css_variable(var_value, all_variables)
        if resolved_value:
            resolved_variables[var_name] = resolved_value

    # Return without leading -- for attribute names
    result: Dict[str, str] = {}
    for var_name, value in resolved_variables.items():
        if var_name.startswith("--"):
            attr_name = var_name[2:]  # Remove --
            result[attr_name] = value

    return result


def extract_css_attributes_from_palette(
    css_content: str,
    data_palette: Optional[str] = None,
    fallback_css_content: str = ""
) -> Dict[str, str]:
    """Extract CSS attributes from palette with optional [data-palette] scoping.

    This function supports both old-style palettes (variables in :root) and
    new-style palettes (variables in [data-palette="name"] blocks).

    Args:
        css_content: Palette CSS text to extract from.
        data_palette: Optional palette name to extract from [data-palette] block.
                     If None, extracts from :root blocks only.
        fallback_css_content: Base theme CSS for fallback values.

    Returns:
        Dictionary mapping attribute names (without --) to resolved values.

    Example:
        >>> # New-style palette with [data-palette] block
        >>> attrs = extract_css_attributes_from_palette(
        ...     css_content,
        ...     data_palette="dark"
        ... )
        >>> attrs["font-color"]
        '#e8e9ed'
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

    # Collect variables with CSS cascade specificity in mind
    all_variables: Dict[str, str] = {}
    
    # Layer 1: Fallback CSS :root blocks (lowest precedence)
    if fallback_css_content:
        all_variables.update(parse_css_variables(fallback_css_content))
    
    # Layer 2: Current CSS :root blocks (higher precedence)
    all_variables.update(parse_css_variables(css_content))
    
    # Layer 3: [data-palette] block (highest precedence if specified)
    if data_palette:
        palette_vars = parse_data_palette_variables(css_content, data_palette)
        all_variables.update(palette_vars)

    # Resolve variables through the context
    resolved_variables: Dict[str, str] = {}
    for var_name, var_value in all_variables.items():
        resolved_value = resolve_css_variable(var_value, all_variables)
        if resolved_value:
            resolved_variables[var_name] = resolved_value

    # Extract requested attributes (strip -- prefix)
    result: Dict[str, str] = {}
    for attr in attributes_to_extract:
        var_name = f"--{attr}"
        if var_name in resolved_variables:
            result[attr] = resolved_variables[var_name]

    return result


def extract_css_attributes(css_content: str, fallback_css_content: str = "") -> Dict[str, str]:
    """Resolve theme CSS attributes (font/color tokens) from CSS content.

    **DEPRECATED**: This function only parses :root blocks and doesn't understand
    the new [data-palette] architecture. For testing palettes, use:
    
    - `load_palette_context(palette_name)` for full cascade simulation
    - `extract_css_attributes_from_palette(css, data_palette="name")` for scoped extraction

    Args:
        css_content: Palette-specific CSS text that may override defaults.
        fallback_css_content: Base theme CSS used when an attribute is missing.

    Returns:
        Dictionary keyed by attribute name (no leading ``--``) with resolved values.
        Example return: ``{"background-color": "#0d1117", "font-color": "#e6edf3"}``.
        
    Note:
        This function maintains backward compatibility for old-style palettes
        that define variables in :root blocks. New palette tests should use
        `load_palette_context()` instead.
    """
    return extract_css_attributes_from_palette(
        css_content=css_content,
        data_palette=None,  # Only parse :root blocks
        fallback_css_content=fallback_css_content
    )


__all__ = [
    "extract_css_variables",
    "parse_css_variables",
    "parse_data_palette_variables",
    "get_element_computed_styles",
    "resolve_css_variable",
    "extract_css_attributes",
    "extract_css_attributes_from_palette",
    "load_palette_context",
]
