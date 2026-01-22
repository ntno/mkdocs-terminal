"""Tests for color contrast validation.

Validates that the Terminal for MkDocs theme meets WCAG 2.1 AA color contrast
standards for theme-controlled colors (body text, links, buttons, form controls).

Tests check:
- Theme body text color vs background
- Link colors vs background
- Button and form control colors
- Heading colors
- All default color palettes (default, dark, gruvbox_dark, pink, sans, sans_dark)
- CSS class loading and variable extraction

Limitations (static analysis):
- Cannot test hover/focus states (require browser automation)
- Cannot validate background images
- Cannot measure actual rendered contrast with fonts

Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
"""

import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from tests.accessibility.utils import _extract_css_variables, validate_color_contrast
from tests.interface.theme_features import DEFAULT_PALETTES


# Expected color values for each palette (used to verify CSS loading)
# These are resolved from the actual palette CSS files, including variable references
PALETTE_COLORS = {
    "default": {
        "font-color": "#151515",  # from terminal.css
        "background-color": "#fff",
    },
    "dark": {
        "font-color": "#e8e9ed",  # from dark.css
        "background-color": "#222225",
    },
    "gruvbox_dark": {
        "font-color": "#ebdbb2",  # from gruvbox_dark.css: var(--gb-dm-fg1)
        "background-color": "#282828",
    },
    "pink": {
        "font-color": "#190910",  # from pink.css
        "background-color": "#ffffff",
    },
    "sans": {
        "font-color": "#151515",  # inherits from terminal.css
        "background-color": "#fff",
    },
    "sans_dark": {
        "font-color": "#e8e9ed",  # from sans_dark.css
        "background-color": "#222225",
    },
}


def _load_css_from_site(site_path: Path, html_content: str) -> str:
    """Load CSS files referenced in HTML head element and matching palette CSS.
    
    Extracts the <link href="..."> CSS file references from the HTML head
    and loads them in order. Detects which palette was used and only loads
    that specific palette CSS (not all palettes) to avoid CSS variable conflicts.
    
    Args:
        site_path: Path to built site directory
        html_content: HTML content of the page (to extract <link> tags from head)
        
    Returns:
        Concatenated CSS content from all theme CSS files plus the active palette
    """
    from bs4 import BeautifulSoup
    import re
    
    css_content = ""
    loaded_paths = set()
    active_palette = None
    
    # Parse HTML to find CSS links in head element
    soup = BeautifulSoup(html_content, 'html.parser')
    head = soup.find('head')
    
    if head:
        # Find all <link> tags in head that reference CSS files
        link_tags = head.find_all('link', rel='stylesheet')
        
        for link in link_tags:
            href = link.get('href')
            if href and href.endswith('.css'):
                # Remove any query parameters or URL encoding
                css_file = href.split('?')[0]
                
                # Check if this is a palette CSS file
                palette_match = re.match(r'.*/css/palettes/([^/]+)\.css$', css_file)
                if palette_match:
                    active_palette = palette_match.group(1)
                
                # Convert relative URL to file path
                if css_file.startswith('/'):
                    css_path = site_path / css_file.lstrip('/')
                else:
                    css_path = site_path / css_file
                
                # Read the CSS file if it exists
                if css_path.exists():
                    try:
                        with open(css_path, 'r', encoding='utf-8') as f:
                            css_content += f.read() + "\n"
                        loaded_paths.add(css_path.resolve())
                    except Exception:
                        pass
    
    # Load the active palette CSS if identified, but don't load all palette files
    # This prevents CSS variable conflicts from later palettes overriding earlier ones
    if active_palette:
        palette_css_path = site_path / 'css' / 'palettes' / f'{active_palette}.css'
        resolved_path = palette_css_path.resolve()
        
        # Only load if not already loaded from head links
        if palette_css_path.exists() and resolved_path not in loaded_paths:
            try:
                with open(palette_css_path, 'r', encoding='utf-8') as f:
                    css_content += f.read() + "\n"
            except Exception:
                pass
    
    return css_content


class TestColorContrast:
    """Tests for WCAG 2.1 AA color contrast compliance in theme."""

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_theme_body_text_contrast_meets_wcag_aa(self, built_example_site_with_palette):
        """Verify theme body text color meets WCAG AA contrast against background.

        Theme-controlled text colors (default body text, paragraphs) must meet
        WCAG 2.1 AA minimum contrast ratio of 4.5:1 for normal text.

        Tests all default color palettes to ensure accessibility across themes.

        Validates: Default text color has sufficient contrast with background.
        """
        
        # Load built site
        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"

        # Read all HTML files from built site
        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, f"No HTML files found in {site_path}"

        all_violations = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Load CSS from site using actual <link> tags in HTML head
            css_content = _load_css_from_site(site_path, html_content)

            violations = validate_color_contrast(html_content, filename=str(html_file.relative_to(site_path)), css_content=css_content)
            all_violations.extend(violations)

        # Report any contrast violations found
        if all_violations:
            violation_report = "\n".join(all_violations)
            pytest.fail(f"Color contrast violations found:\n{violation_report}")

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_theme_link_colors_meet_wcag_aa(self, built_example_site_with_palette):
        """Verify theme link colors meet WCAG AA contrast.

        Theme link colors (visited, unvisited, etc.) must meet WCAG 2.1 AA
        minimum contrast ratio of 4.5:1.

        Tests all default color palettes to ensure accessibility across themes.

        Note: Focus/hover states require browser testing and are out of scope.
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast

        Validates: Link colors have sufficient contrast with background.
        """

        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"

        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found"

        all_violations = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Load CSS from site using actual <link> tags in HTML head
            css_content = _load_css_from_site(site_path, html_content)

            violations = validate_color_contrast(html_content, filename=str(html_file.relative_to(site_path)), css_content=css_content)
            # Filter for link-related violations
            link_violations = [v for v in violations if 'link' in v.lower()]
            all_violations.extend(link_violations)

        if all_violations:
            violation_report = "\n".join(all_violations)
            pytest.fail(f"Link color contrast violations found:\n{violation_report}")

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_theme_button_and_form_contrast_meets_wcag_aa(self, built_example_site_with_palette):
        """Verify theme button and form control colors meet WCAG AA contrast.

        Theme-provided button and form control colors must meet WCAG 2.1 AA
        minimum contrast ratio of 3:1 for UI components.

        Tests all default color palettes to ensure accessibility across themes.

        Validates: Button and form element colors have sufficient contrast.
        """

        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"

        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found"

        all_violations = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Load CSS from site using actual <link> tags in HTML head
            css_content = _load_css_from_site(site_path, html_content)

            violations = validate_color_contrast(html_content, filename=str(html_file.relative_to(site_path)), css_content=css_content)
            # Filter for button/form violations
            form_violations = [v for v in violations if any(term in v.lower() for term in ['button', 'input', 'form', 'label'])]
            all_violations.extend(form_violations)

        if all_violations:
            violation_report = "\n".join(all_violations)
            pytest.fail(f"Button/form color contrast violations found:\n{violation_report}")

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_css_classes_loaded_correctly(self, built_example_site_with_palette):
        """Verify that CSS classes and variables are loaded correctly for each palette.

        This test ensures that the CSS loading mechanism properly extracts palette-specific
        CSS variables and that the correct colors are being used for each palette.

        The test validates:
        - CSS files are found and loaded from the built site
        - CSS variables are correctly extracted from :root blocks
        - Expected palette colors are present in the extracted variables
        - No CSS variable cross-contamination between palettes

        This is critical for ensuring the color contrast validation tests are using
        the actual colors that would be rendered in each palette.
        """

        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"

        # Load the HTML
        html_file = site_path / 'index.html'
        assert html_file.exists(), f"HTML file not found at {html_file}"

        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Load CSS from site
        css_content = _load_css_from_site(site_path, html_content)
        assert len(css_content) > 0, "No CSS content loaded from site"

        # Extract CSS variables
        css_variables = _extract_css_variables(html_content, css_content)
        assert len(css_variables) > 0, "No CSS variables extracted"

        # Determine which palette was used by checking HTML or site path
        # The site path format is: built_{example_name}_{palette_name}_site{N}
        # Sort by length descending to match longest names first (e.g., 'gruvbox_dark' before 'dark')
        palette_name = None
        for palette in sorted(DEFAULT_PALETTES, key=len, reverse=True):
            if f"_{palette}_site" in str(site_path):
                palette_name = palette
                break

        assert palette_name is not None, f"Could not determine palette from site path: {site_path}"

        # Get expected colors for this palette
        expected_colors = PALETTE_COLORS.get(palette_name)
        assert expected_colors is not None, f"No expected colors defined for palette: {palette_name}"

        # Verify that CSS variables contain the expected colors
        actual_font_color = css_variables.get('--font-color')
        actual_bg_color = css_variables.get('--background-color')

        assert actual_font_color is not None, \
            f"Palette '{palette_name}': CSS variable --font-color not found. Variables: {list(css_variables.keys())}"
        assert actual_bg_color is not None, \
            f"Palette '{palette_name}': CSS variable --background-color not found. Variables: {list(css_variables.keys())}"

        # Normalize colors for comparison (lowercase, trim whitespace)
        actual_font_normalized = actual_font_color.lower().strip()
        expected_font_normalized = expected_colors['font-color'].lower().strip()
        actual_bg_normalized = actual_bg_color.lower().strip()
        expected_bg_normalized = expected_colors['background-color'].lower().strip()

        assert actual_font_normalized == expected_font_normalized, \
            f"Palette '{palette_name}': Expected font color {expected_font_normalized}, got {actual_font_normalized}"
        assert actual_bg_normalized == expected_bg_normalized, \
            f"Palette '{palette_name}': Expected background color {expected_bg_normalized}, got {actual_bg_normalized}"

        # Verify that CSS has multiple palettes available but only the correct one is used
        palette_dir = site_path / 'css' / 'palettes'
        if palette_dir.exists():
            palette_files = list(palette_dir.glob('*.css'))
            assert len(palette_files) > 0, f"No palette CSS files found in {palette_dir}"



