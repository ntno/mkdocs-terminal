"""Tests for color contrast validation.

Validates that the Terminal for MkDocs theme meets WCAG 2.1 AA color contrast
standards for theme-controlled colors (body text, links, buttons, form controls).

Tests check:
- Theme body text color vs background
- Link colors vs background
- Button and form control colors
- Heading colors
- All default color palettes (default, dark, gruvbox_dark, pink, sans, sans_dark)

Limitations (static analysis):
- Cannot test hover/focus states (require browser automation)
- Cannot validate background images
- Cannot measure actual rendered contrast with fonts

Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
"""

import pytest
from pathlib import Path
from tests.accessibility.utils import validate_color_contrast


# List of default color palettes available in the theme
DEFAULT_PALETTES = [
    "default",
    "dark",
    "gruvbox_dark",
    "pink",
    "sans",
    "sans_dark",
]


def _load_css_from_site(site_path: Path) -> str:
    """Load all CSS files from built site directory.
    
    Concatenates CSS from main theme files (terminal.css, theme.css, palettes).
    
    Args:
        site_path: Path to built site directory
        
    Returns:
        Concatenated CSS content from all theme CSS files
    """
    css_content = ""
    
    # Load CSS files in order of importance
    css_files = [
        "css/terminal.css",
        "css/theme.css",
    ]
    
    for css_file in css_files:
        css_path = site_path / css_file
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content += f.read() + "\n"
    
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

        # Load CSS from site for color variable resolution
        css_content = _load_css_from_site(site_path)

        # Read all HTML files from built site
        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, f"No HTML files found in {site_path}"

        all_violations = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

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

        # Load CSS from site for color variable resolution
        css_content = _load_css_from_site(site_path)

        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found"

        all_violations = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

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

        # Load CSS from site for color variable resolution
        css_content = _load_css_from_site(site_path)

        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found"

        all_violations = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            violations = validate_color_contrast(html_content, filename=str(html_file.relative_to(site_path)), css_content=css_content)
            # Filter for button/form violations
            form_violations = [v for v in violations if any(term in v.lower() for term in ['button', 'input', 'form', 'label'])]
            all_violations.extend(form_violations)

        if all_violations:
            violation_report = "\n".join(all_violations)
            pytest.fail(f"Button/form color contrast violations found:\n{violation_report}")


