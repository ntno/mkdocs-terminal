"""Utility functions for accessibility testing.

This module provides helper functions for common accessibility validation checks
using BeautifulSoup4 for HTML parsing and HTML Tidy (via tidylib) for structural validation.

Design Decision: Using BeautifulSoup4 + tidylib instead of external accessibility
libraries (axe-core-python, pytest-a11y) because:
- BeautifulSoup4 is already available as a transitive dependency
- tidylib provides standards-based HTML5 validation without extra dependencies
- Provides fine-grained control over what we validate
- Allows project-specific accessibility standards
- Simpler to debug and maintain custom validators
- Lighter weight than external a11y checking libraries

Tool Selection:
- BeautifulSoup4: Used for semantic analysis (duplicate IDs, element relationships,
  ARIA attributes). It parses HTML leniently and auto-corrects malformed HTML,
  making it perfect for analyzing the DOM structure and content.
  - validate_duplicate_ids(): Finds all ID attributes and checks for duplicates
  - validate_semantic_html(): Validates correct use of <main>, <nav>, <header>, <footer>
  - validate_aria(): Checks ARIA attributes on interactive elements

- tidylib (HTML Tidy): Used for structural HTML5 validation. It strictly validates
  against HTML5 spec and detects nesting errors that BeautifulSoup would auto-correct.
  - validate_html_structure(): Detects invalid nesting, unclosed tags, content in wrong locations

Scope: These validators test the theme's HTML structure and attributes.
They do NOT validate user content (headings, links, images, forms in documentation).
User content accessibility is the responsibility of site authors.
"""

from typing import List, Optional, Set
import re
from bs4 import BeautifulSoup, Tag
from tidylib import tidy_document


def _format_violation(message: str, filename: str = "index.html", element: Optional[Tag] = None) -> str:
    """Format an accessibility violation message.

    Args:
        message: Human-readable description of the violation
        filename: Optional filename for error reporting
        element: Optional HTML element involved in violation

    Returns:
        Formatted violation message
    """
    violation = f"{filename}: {message}"
    if element:
        violation += f" [line approx. {element.sourceline}]"
    return violation


def validate_duplicate_ids(html: str, filename: str = "index.html") -> List[str]:
    """Validate that no duplicate IDs exist in HTML.

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages (empty if no duplicates found)
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    all_ids: Set[str] = set()
    for element in soup.find_all(id=True):
        element_id = element.get("id", "")
        if element_id in all_ids:
            violations.append(_format_violation(f"Duplicate ID found: {element_id}", filename, element))
        all_ids.add(element_id)

    return violations


def validate_semantic_html(html: str, filename: str = "index.html") -> List[str]:
    """Validate semantic HTML structure of theme.

    Theme-focused checks:
    - Exactly one <main> element, direct child of <body>
    - Multiple <nav> elements have aria-label to distinguish them
    - <header> and <footer> not nested inside <main>
    - Proper use of semantic elements in theme template

    Note: Duplicate ID checking is handled separately by validate_duplicate_ids()

    Out of scope:
    - Form labeling (user content responsibility)
    - Link text (user content responsibility)
    - Section/article heading requirements (user content responsibility)

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    # Check for exactly one <main> element
    main_elements = soup.find_all("main")
    if len(main_elements) != 1:
        violations.append(_format_violation(
            f"Expected exactly 1 <main> element, found {len(main_elements)}",
            filename
        ))

    # Check that <main> is direct child of <body>
    if main_elements:
        main_elem = main_elements[0]
        if main_elem.parent.name != "body":
            violations.append(_format_violation(
                f"<main> should be direct child of <body>, found parent: {main_elem.parent.name}",
                filename,
                main_elem
            ))

    # Check that multiple <nav> elements have aria-label to distinguish them
    nav_elements = soup.find_all("nav")
    if len(nav_elements) > 1:
        for nav in nav_elements:
            if not nav.get("aria-label"):
                violations.append(_format_violation(
                    "Multiple <nav> elements should have aria-label to distinguish them",
                    filename,
                    nav
                ))

    # Check that <header> and <footer> are not inside <main>
    if main_elements:
        main_elem = main_elements[0]

        if main_elem.find("header"):
            violations.append(_format_violation(
                "<header> should not be nested inside <main> (should be theme header outside main content)",
                filename,
                main_elem.find("header")
            ))

        if main_elem.find("footer"):
            violations.append(_format_violation(
                "<footer> should not be nested inside <main> (should be theme footer outside main content)",
                filename,
                main_elem.find("footer")
            ))

    return violations


def validate_html_structure(html: str, filename: str = "index.html") -> List[str]:
    """Validate HTML5 structure and element nesting.

    Uses HTML Tidy to detect structural issues such as:
    - Invalid element nesting (e.g., head inside body)
    - Unclosed or unexpected elements
    - Content occurring in wrong locations

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting

    Returns:
        List of violation messages
    """
    violations: List[str] = []

    tidy_options = {
        'doctype': 'html5',
    }

    tidied_html, errors = tidy_document(html, options=tidy_options)

    # Filter for structural problems (nesting, unexpected elements, missing closing tags)
    error_lines = errors.strip().split('\n') if errors.strip() else []
    for error in error_lines:
        if not error:
            continue

        # Check for structural keywords that indicate violations
        is_structural_issue = any(keyword in error.lower() for keyword in [
            'unexpected',  # unexpected element in wrong context
            'missing </',  # missing closing tag
            'previously',  # element already opened (nesting issue)
            'discarding',  # invalid nesting being ignored
            'occurs after end'  # content in wrong place
        ])

        if is_structural_issue:
            violations.append(_format_violation(error, filename))

    return violations



def validate_aria_buttons(html: str, filename: str = "index.html") -> List[str]:
    """Check that all <button> elements have text content or aria-label."""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.find_all("button"):
        text = element.get_text(strip=True)
        aria_label = element.get("aria-label", "").strip()
        if not text and not aria_label:
            violations.append(_format_violation(
                "Button missing text content or aria-label",
                filename,
                element
            ))
    return violations

# https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA14.html
def validate_aria_hidden(html: str, filename: str = "index.html") -> List[str]:
    """Check that aria-hidden is used correctly.

    Valid use case:
    - Genuinely decorative elements (no text content)

    Violations:
    - Elements with aria-hidden="true" that contain text content

    Note: Icon buttons should use aria-label for accessible naming, not aria-hidden.
    Example: <button aria-label="Close">x</button>
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    for element in soup.find_all(attrs={"aria-hidden": "true"}):
        element_text = element.get_text(strip=True)
        
        if element_text:
            # Elements with aria-hidden="true" should not contain text
            violations.append(_format_violation(
                f"Element with aria-hidden='true' contains text. Use aria-label for icon buttons instead.",
                filename,
                element
            ))

    return violations


def validate_modal_accessibility(html: str, filename: str = "index.html") -> List[str]:
    """Validate search modal has proper ARIA attributes for accessibility.

    Checks:
    - Modal has role="alertdialog" or role="dialog"
    - Modal has aria-modal="true"
    - Modal has aria-labelledby pointing to a valid heading
    - Close button has aria-label
    - Search input has associated label (aria-labelledby)
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    # Find the modal dialog
    modal = soup.find(id="mkdocs_search_modal")
    if not modal:
        # Modal may not exist on all pages (e.g., pages without search)
        return violations

    # Check modal role
    modal_role = modal.get("role", "").lower()
    if modal_role not in ("alertdialog", "dialog"):
        violations.append(_format_violation(
            f"Modal should have role='alertdialog' or role='dialog', found role='{modal_role}'",
            filename,
            modal
        ))

    # Check aria-modal
    if modal.get("aria-modal", "").lower() != "true":
        violations.append(_format_violation(
            "Modal missing aria-modal='true'",
            filename,
            modal
        ))

    # Check aria-labelledby
    labelledby = modal.get("aria-labelledby", "").strip()
    if not labelledby:
        violations.append(_format_violation(
            "Modal missing aria-labelledby pointing to modal title",
            filename,
            modal
        ))
    else:
        # Verify the referenced element exists
        label_elem = soup.find(id=labelledby)
        if not label_elem:
            violations.append(_format_violation(
                f"Modal aria-labelledby='{labelledby}' references non-existent element",
                filename,
                modal
            ))

    # Check close button has aria-label
    close_button = modal.find("button", class_="close")
    if close_button:
        if not close_button.get("aria-label", "").strip():
            violations.append(_format_violation(
                "Modal close button missing aria-label",
                filename,
                close_button
            ))

    # Check search input has label association
    search_input = modal.find("input", {"type": "search"})
    if search_input:
        labelledby = search_input.get("aria-labelledby", "").strip()
        if not labelledby:
            violations.append(_format_violation(
                "Search input missing aria-labelledby association",
                filename,
                search_input
            ))
        else:
            # Verify the referenced element exists
            label_elem = soup.find(id=labelledby)
            if not label_elem:
                violations.append(_format_violation(
                    f"Search input aria-labelledby='{labelledby}' references non-existent element",
                    filename,
                    search_input
                ))

    return violations


def validate_form_labels(html: str, filename: str = "index.html") -> List[str]:
    """Validate that form inputs have associated labels.

    Checks:
    - Text inputs have either <label> with for= or aria-labelledby/aria-label
    - All inputs have accessible names
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    # Find all form inputs (excluding submit buttons, hidden fields)
    inputs = soup.find_all(["input", "textarea", "select"])

    for input_elem in inputs:
        input_type = input_elem.get("type", "text").lower()
        
        # Skip certain input types that don't need labels
        if input_type in ("hidden", "submit", "button", "reset", "image"):
            continue

        # Check for explicit label association
        input_id = input_elem.get("id", "")
        has_label = False
        
        if input_id:
            label = soup.find("label", {"for": input_id})
            if label:
                has_label = True

        # Check for aria-label or aria-labelledby
        has_aria_name = bool(
            input_elem.get("aria-label", "").strip() or
            input_elem.get("aria-labelledby", "").strip()
        )

        # Check for title attribute (fallback, less ideal)
        has_title = bool(input_elem.get("title", "").strip())

        if not (has_label or has_aria_name or has_title):
            violations.append(_format_violation(
                f"Form input of type '{input_type}' missing accessible label. "
                f"Use <label for='{input_id}'>, aria-label, or aria-labelledby.",
                filename,
                input_elem
            ))

    return violations


def validate_link_text(html: str, filename: str = "index.html") -> List[str]:
    """Validate that links have descriptive text or aria-label.

    Scope: Theme links only (navigation, footer, etc.)
    Out of scope: User-provided links in documentation content

    Checks:
    - Links have visible text content
    - If empty, links have aria-label
    - Avoid generic link text like "click here" (warning, not violation)
    """
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    # Find all links, excluding those in user content areas
    # Theme links are typically in: nav, header, footer, sidebars
    theme_regions = soup.find_all(["nav", "header", "footer", "aside"])
    links = []
    
    for region in theme_regions:
        links.extend(region.find_all("a"))

    for link in links:
        link_text = link.get_text(strip=True)
        aria_label = link.get("aria-label", "").strip()
        
        if not link_text and not aria_label:
            violations.append(_format_violation(
                "Link missing text content and aria-label",
                filename,
                link
            ))

    return violations


def validate_color_contrast(html: str, filename: str = "index.html", css_content: str = "") -> List[str]:
    """Validate color contrast meets WCAG 2.1 AA standards.

    This function validates that text and interactive elements in the theme
    have sufficient color contrast between foreground and background colors.

    **CRITICAL:** This function requires actual CSS to be provided via css_content
    parameter or parsed from HTML. It does NOT use hardcoded fallback colors, as
    those would hide real contrast issues. If CSS colors cannot be extracted,
    elements are skipped to avoid false positives.

    Scope:
    - Validates theme-provided colors for body text, links, buttons, form controls
    - Checks inline styles and CSS variable definitions
    - Uses WCAG 2.1 AA standard: 4.5:1 for normal text, 3:1 for large text

    Limitations (static analysis only):
    - Cannot compute CSS cascading (uses root :root variables only)
    - Cannot test hover/focus states (dynamic CSS)
    - Cannot validate background images
    - Cannot measure actual rendered contrast (font anti-aliasing varies)
    - Requires CSS to be available for accurate validation

    Args:
        html: HTML string to validate
        filename: Optional filename for error reporting
        css_content: Optional CSS content to parse for color variables

    Returns:
        List of contrast violation messages
    """
    from .color_utils import get_contrast_ratio, meets_wcag_aa
    
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    # Extract CSS variables from root element and css_content
    css_variables = _extract_css_variables(html, css_content)

    # Get computed colors for body element
    body = soup.find('body')
    body_styles = _get_element_computed_styles(body, css_variables) if body else {}
    body_bg_color = body_styles.get('background-color')
    
    if not body_bg_color:
        # If we can't determine background color, skip validation for this file
        # (avoiding false negatives from missing CSS data)
        return violations

    # Elements to validate for contrast
    elements_to_check = soup.find_all(['body', 'p', 'a', 'button', 'input', 'label', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Check each element's text color against background
    for element in elements_to_check:
        # Skip elements without text content
        text_content = element.get_text(strip=True)
        if not text_content or len(text_content) == 0:
            continue

        # Get computed styles for this element
        element_styles = _get_element_computed_styles(element, css_variables)
        fg_color = element_styles.get('color')
        
        # Skip if we can't determine text color from CSS (don't use fallback)
        if not fg_color:
            continue

        # Get background color (element or inherited from body)
        bg_color = element_styles.get('background-color') or body_bg_color

        # Calculate contrast ratio
        ratio = get_contrast_ratio(fg_color, bg_color)

        # Determine if large text (heuristic: headers are large)
        is_large_text = element.name in ['h1', 'h2', 'h3']
        text_size = 24 if is_large_text else 14

        # Check against WCAG AA standard
        if ratio is not None and not meets_wcag_aa(ratio, text_size=text_size):
            element_desc = element.name
            if element_desc == 'a':
                element_desc = f"link (text: {text_content[:30]})"
            elif element_desc in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                element_desc = f"{element_desc} heading"
            elif element_desc in ['button', 'input', 'label']:
                element_desc = f"{element_desc} element"

            violations.append(_format_violation(
                f"Insufficient color contrast on {element_desc}: {ratio:.2f}:1 "
                f"(need {4.5 if not is_large_text else 3.0}:1 for WCAG AA). "
                f"Color: {fg_color}, Background: {bg_color}",
                filename,
                element
            ))

    return violations


def _extract_css_variables(html: str, css_content: str = "") -> dict:
    """Extract CSS custom properties (variables) from HTML and CSS content.
    
    Parses :root { --var-name: value; } definitions to extract CSS variables.
    Also resolves cascading variable references (e.g., --font-color: var(--fg1)).
    
    Args:
        html: HTML string (may contain <style> tags)
        css_content: Optional additional CSS content to parse
        
    Returns:
        Dictionary mapping variable names to their resolved values (e.g., {'--font-color': '#000000'})
    """
    variables = {}
    
    # Extract from HTML <style> tags
    soup = BeautifulSoup(html, "html.parser")
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            variables.update(_parse_css_variables(style_tag.string))
    
    # Extract from provided CSS content
    if css_content:
        variables.update(_parse_css_variables(css_content))
    
    # Resolve cascading variable references
    # Iterate through variables and resolve any var() references
    resolved = {}
    for var_name, var_value in variables.items():
        resolved[var_name] = _resolve_css_variable(var_value, variables)
    
    return resolved


def _parse_css_variables(css_text: str) -> dict:
    """Parse CSS variable definitions from CSS text.
    
    Looks for :root { --var-name: value; } blocks (handles multiple blocks).
    Later definitions override earlier ones (CSS cascade order preserved).
    
    Args:
        css_text: CSS text content
        
    Returns:
        Dictionary of variable definitions
    """
    variables = {}
    
    # Find ALL :root blocks (not just the first one)
    # Use a more careful regex that handles nested content within blocks
    # Match :root { ... } where ... can contain any characters except an unmatched }
    root_pattern = r':root\s*\{([^{}]*(?:\{[^}]*\}[^{}]*)*)\}'
    
    for root_match in re.finditer(root_pattern, css_text, re.DOTALL):
        root_content = root_match.group(1)
        # Extract variable assignments: --name: value;
        var_pattern = r'--([a-z0-9-]+)\s*:\s*([^;]+);'
        for match in re.finditer(var_pattern, root_content):
            var_name = f"--{match.group(1)}"
            var_value = match.group(2).strip()
            variables[var_name] = var_value
    
    return variables


def _get_element_computed_styles(element: Optional[Tag], css_variables: dict) -> dict:
    """Get computed color styles for an element.
    
    Extracts color and background-color from:
    1. Inline styles (highest priority)
    2. CSS variables if defined in :root
    3. Returns empty dict if neither found
    
    Args:
        element: BeautifulSoup Tag element
        css_variables: Dictionary of CSS variables from :root
        
    Returns:
        Dictionary with 'color' and/or 'background-color' keys
    """
    styles = {}
    
    if not element:
        return styles
    
    # Get inline style attribute
    style_attr = element.get("style", "")
    
    # Extract color from inline style
    if "color:" in style_attr:
        match = re.search(r"(?<!background-)color:\s*([^;]+)", style_attr)
        if match:
            color_value = match.group(1).strip()
            # Resolve CSS variables if needed
            color_value = _resolve_css_variable(color_value, css_variables)
            if color_value:
                styles['color'] = color_value
    
    # Extract background-color from inline style
    if "background-color:" in style_attr:
        match = re.search(r"background-color:\s*([^;]+)", style_attr)
        if match:
            bg_value = match.group(1).strip()
            # Resolve CSS variables if needed
            bg_value = _resolve_css_variable(bg_value, css_variables)
            if bg_value:
                styles['background-color'] = bg_value
    
    # If no inline color specified, use CSS variable defaults
    # All text elements inherit font-color from body/root CSS variables
    if not styles.get('color'):
        if '--font-color' in css_variables:
            color_value = _resolve_css_variable('var(--font-color)', css_variables)
            if color_value:
                styles['color'] = color_value
    
    # If no inline background color specified, use CSS variable defaults or inherit from body
    if not styles.get('background-color'):
        if '--background-color' in css_variables:
            bg_value = _resolve_css_variable('var(--background-color)', css_variables)
            if bg_value:
                styles['background-color'] = bg_value
    
    return styles


def _resolve_css_variable(value: str, css_variables: dict, max_depth: int = 10) -> Optional[str]:
    """Resolve CSS variable reference to its value.
    
    Handles var(--variable-name) references, including cascading variable references.
    For example: --font-color: var(--gb-dm-fg1) -> #ebdbb2
    
    Args:
        value: CSS value that may contain var() reference
        css_variables: Dictionary of variable definitions
        max_depth: Maximum recursion depth to prevent infinite loops
        
    Returns:
        Resolved color value, or None if cannot be resolved
    """
    if max_depth <= 0:
        return None
    
    value = value.strip()
    
    # Check if it's a variable reference
    var_match = re.match(r'var\(--([a-z0-9-]+)\)', value)
    if var_match:
        var_name = f"--{var_match.group(1)}"
        if var_name in css_variables:
            # Recursively resolve in case the variable refers to another variable
            resolved = _resolve_css_variable(css_variables[var_name].strip(), css_variables, max_depth - 1)
            return resolved
        return None
    
    # Return as-is if it's a direct color value
    return value


def extract_css_attributes(css_content: str) -> dict:
    """Extract theme CSS attribute variables and return as a map.
    
    Extracts CSS custom properties (variables) from the provided CSS content
    and resolves variable references. Automatically resolves chained variable
    references (e.g., --primary-color references another variable).
    
    Attributes extracted:
    - global-font-size: Base font size
    - global-line-height: Base line height
    - global-space: Base spacing unit
    - font-stack: Primary font family
    - mono-font-stack: Monospace font family
    - background-color: Page background color
    - page-width: Max page width
    - font-color: Primary text color
    - invert-font-color: Inverted text color (for contrast)
    - secondary-color: Secondary color variable
    - tertiary-color: Tertiary color variable
    - primary-color: Primary color for links/accents
    - error-color: Error/alert color
    - progress-bar-background: Progress bar background color
    - progress-bar-fill: Progress bar fill color
    - code-bg-color: Code block background color
    - input-style: Input border style
    - display-h1-decoration: H1 decoration setting
    
    Args:
        css_content: CSS file content as a string
    
    Returns:
        Dictionary mapping attribute names (without '--' prefix) to their resolved values.
        Variables that reference other variables are recursively resolved.
        Variables that cannot be resolved are not included in the output.
    
    Example:
        css_content = '''
            :root {
                --background-color: #fff;
                --font-color: #151515;
                --primary-color: #1a95e0;
                --error-color: #d20962;
            }
        '''
        result = extract_css_attributes(css_content)
        # Returns:
        # {
        #     'background-color': '#fff',
        #     'font-color': '#151515',
        #     'primary-color': '#1a95e0',
        #     'error-color': '#d20962'
        # }
    """
    # List of attributes to extract
    attributes_to_extract = [
        'global-font-size',
        'global-line-height',
        'global-space',
        'font-stack',
        'mono-font-stack',
        'background-color',
        'page-width',
        'font-color',
        'invert-font-color',
        'secondary-color',
        'tertiary-color',
        'primary-color',
        'error-color',
        'progress-bar-background',
        'progress-bar-fill',
        'code-bg-color',
        'input-style',
        'display-h1-decoration',
    ]
    
    # First pass: extract all CSS variables
    all_variables = {}
    var_pattern = r'--([a-z0-9\-]+):\s*([^;]+);'
    for match in re.finditer(var_pattern, css_content, re.IGNORECASE):
        var_name = match.group(1)
        var_value = match.group(2).strip()
        all_variables[f'--{var_name}'] = var_value
    
    # Second pass: extract and resolve requested attributes
    result = {}
    for attr in attributes_to_extract:
        var_name = f'--{attr}'
        if var_name in all_variables:
            # Resolve the variable (in case it references another variable)
            resolved_value = _resolve_css_variable(all_variables[var_name], all_variables)
            if resolved_value:
                result[attr] = resolved_value
    
    return result



