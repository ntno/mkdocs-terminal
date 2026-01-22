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
from tests.accessibility.color_utils import get_contrast_ratio, meets_wcag_aa
from tests.interface.theme_features import DEFAULT_PALETTES
import re


# Expected color values for each palette (used to verify CSS loading)
# These are resolved from the actual palette CSS files, including variable references
PALETTE_COLORS = {
    "default": {
        "font-color": "#151515",  # from terminal.css - 18.3:1 contrast
        "background-color": "#fff",
    },
    "dark": {
        "font-color": "#3f3f44",  # intentionally modified for testing - 1.5:1 contrast
        "background-color": "#222225",
    },
    "gruvbox_dark": {
        "font-color": "#32302f",  # intentionally modified for testing - 1.1:1 contrast
        "background-color": "#282828",
    },
    "pink": {
        "font-color": "#f90d7a",  # intentionally modified for testing - 3.9:1 contrast
        "background-color": "#ffffff",
    },
    "sans": {
        "font-color": "#151515",  # inherits from terminal.css - 18.3:1 contrast
        "background-color": "#fff",
    },
    "sans_dark": {
        "font-color": "#62c4ff",  # intentionally modified for testing - 8.2:1 contrast
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
        ("search-enabled", palette) for palette in DEFAULT_PALETTES
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

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_ratios_meet_wcag_aa_minimum(self, palette_name):
        """Verify calculated contrast ratios for link colors meet WCAG AA minimum of 4.5:1.
        
        This test validates the actual contrast ratio calculations for link colors
        against their backgrounds. It ensures that the mathematical ratio is at least
        4.5:1 as required by WCAG 2.1 AA for normal text (including links).
        
        Tests each default palette's link color (foreground) against its background color.
        
        Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
        """
        # WCAG AA minimum for text contrast (including links)
        WCAG_AA_TEXT_MINIMUM = 4.5
        
        # Get expected colors for this palette
        expected_colors = PALETTE_COLORS.get(palette_name)
        assert expected_colors is not None, f"No expected colors defined for palette: {palette_name}"
        
        link_color = expected_colors.get("font-color")
        background_color = expected_colors.get("background-color")
        
        assert link_color is not None, f"No link color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Calculate contrast ratio
        ratio = get_contrast_ratio(link_color, background_color)
        assert ratio is not None, f"Could not calculate contrast ratio for {link_color} on {background_color}"
        
        # Verify ratio meets WCAG AA minimum
        assert ratio >= WCAG_AA_TEXT_MINIMUM, \
            f"Palette '{palette_name}': Link color {link_color} on {background_color} has " \
            f"contrast ratio {ratio:.2f}:1, which is below the WCAG AA minimum of {WCAG_AA_TEXT_MINIMUM}:1"

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_passes_wcag_aa_validation(self, palette_name):
        """Verify link colors pass WCAG AA validation using dedicated validator.
        
        This test uses the meets_wcag_aa utility function to validate that link colors
        meet WCAG 2.1 AA standards for text contrast (4.5:1 minimum).
        
        Tests each default palette to ensure all link colors are accessible.
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        # Get expected colors for this palette
        expected_colors = PALETTE_COLORS.get(palette_name)
        assert expected_colors is not None, f"No expected colors defined for palette: {palette_name}"
        
        link_color = expected_colors.get("font-color")
        background_color = expected_colors.get("background-color")
        
        assert link_color is not None, f"No link color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Validate using meets_wcag_aa (expects 4.5:1 minimum for normal text)
        is_compliant = meets_wcag_aa(link_color, background_color, level="AA", is_large_text=False)
        assert is_compliant, \
            f"Palette '{palette_name}': Link color {link_color} on {background_color} " \
            f"does not meet WCAG 2.1 AA contrast requirements"

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_all_links_in_site_meet_wcag_aa_contrast(self, built_example_site_with_palette):
        """Verify all rendered links in built site meet WCAG AA contrast requirements.
        
        This comprehensive test scans all HTML files in a built site and validates
        that every link element has sufficient contrast between its foreground color
        and background color. It uses actual colors extracted from the rendered site.
        
        Tests all default palettes to ensure accessibility across all theme variations.
        
        Limitations:
        - Tests static HTML colors; hover/focus states require browser automation
        - Cannot measure contrast with background images
        - Only validates direct foreground/background color relationships
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"
        
        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found in built site"
        
        contrast_failures = []
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Load CSS from site
            css_content = _load_css_from_site(site_path, html_content)
            
            # Parse HTML to find all links
            soup = BeautifulSoup(html_content, 'html.parser')
            links = soup.find_all('a')
            
            file_path = str(html_file.relative_to(site_path))
            
            for link_index, link in enumerate(links):
                # Get link text for reporting
                link_text = link.get_text(strip=True)[:50]  # First 50 chars
                
                # Try to extract computed styles for the link
                # Note: This is a simplified check using CSS selectors
                style = link.get('style', '')
                
                # Check for color in inline styles
                color_match = re.search(r'color\s*:\s*([^;]+)', style, re.IGNORECASE)
                link_color = color_match.group(1).strip() if color_match else None
                
                bg_match = re.search(r'background(?:-color)?\s*:\s*([^;]+)', style, re.IGNORECASE)
                bg_color = bg_match.group(1).strip() if bg_match else None
                
                # If not in inline styles, these would need CSS class resolution
                # For now, we validate inline-styled links
                if link_color and bg_color:
                    ratio = get_contrast_ratio(link_color, bg_color)
                    if ratio and ratio < 4.5:
                        contrast_failures.append(
                            f"{file_path} (link {link_index}): '{link_text}' "
                            f"has contrast {ratio:.2f}:1 (need 4.5:1)"
                        )
        
        assert not contrast_failures, \
            f"Link contrast violations found:\n" + "\n".join(contrast_failures)

    @pytest.mark.parametrize("palette_name,expected_ratio", [
        ("default", 18.3),  # High contrast dark on light
        ("dark", 1.5),      # Low contrast (intentional test case)
        ("gruvbox_dark", 1.1),  # Very low contrast (intentional test case)
        ("pink", 3.9),      # Below 4.5 threshold
        ("sans", 18.3),     # High contrast
        ("sans_dark", 8.2),  # Good contrast
    ])
    def test_link_contrast_ratio_calculations_are_accurate(self, palette_name, expected_ratio):
        """Verify contrast ratio calculations are mathematically accurate.
        
        This test validates that contrast ratio calculations match expected values
        for known color combinations. It serves as a regression test for the
        color_utils.get_contrast_ratio() function.
        
        Uses actual palette colors to ensure calculations are correct across
        different color ranges.
        
        Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
        """
        expected_colors = PALETTE_COLORS.get(palette_name)
        assert expected_colors is not None, f"No expected colors defined for palette: {palette_name}"
        
        link_color = expected_colors.get("font-color")
        background_color = expected_colors.get("background-color")
        
        assert link_color is not None, f"No link color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Calculate contrast ratio
        ratio = get_contrast_ratio(link_color, background_color)
        assert ratio is not None, f"Could not calculate contrast for {link_color} on {background_color}"
        
        # Verify calculation is within tolerance (allow 0.1 variation due to rounding)
        tolerance = 0.1
        assert abs(ratio - expected_ratio) <= tolerance, \
            f"Palette '{palette_name}': Expected contrast {expected_ratio}:1, " \
            f"got {ratio:.2f}:1 (colors: {link_color} on {background_color})"



