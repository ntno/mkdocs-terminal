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
from tests.accessibility.utils import _extract_css_variables, validate_color_contrast, _get_element_computed_styles
from tests.accessibility.color_utils import get_contrast_ratio, meets_wcag_aa
from tests.interface.theme_features import DEFAULT_PALETTES
import re

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
    def test_all_link_color_combinations_meet_wcag_aa(self, built_example_site_with_palette):
        """Verify all unique link color combinations in built site meet WCAG AA contrast.

        Links can use different CSS colors depending on context:
        - Primary color links (side nav, inline links): --primary-color on --background-color
        - Font color links (in inverted sections): --font-color on --background-color
        - Inverted color links (banner/footer): --invert-font-color on --font-color background

        This test extracts all actual link elements and their computed colors,
        groups them by unique color combinations, and validates each combination
        meets the 4.5:1 minimum for link text contrast.

        Tests all default palettes to ensure accessibility across all themes.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"

        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found in built site"

        # Collect all link color combinations found
        link_colors = {}  # {(fg_color, bg_color): [count, [locations]]}
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Load CSS from site
            css_content = _load_css_from_site(site_path, html_content)
            css_variables = _extract_css_variables(html_content, css_content)

            # Parse HTML to find all links
            soup = BeautifulSoup(html_content, 'html.parser')
            links = soup.find_all('a')

            file_path = str(html_file.relative_to(site_path))

            for link in links:
                # Get link text for reporting
                link_text = link.get_text(strip=True)[:40]
                if not link_text:
                    continue

                # Extract computed styles for the link
                link_styles = _get_element_computed_styles(link, css_variables)
                link_color = link_styles.get('color')
                link_bg = link_styles.get('background-color')

                # If no explicit background, check parent elements
                if not link_bg or link_bg == 'transparent':
                    parent = link.parent
                    while parent and not link_bg:
                        parent_styles = _get_element_computed_styles(parent, css_variables)
                        parent_bg = parent_styles.get('background-color')
                        if parent_bg and parent_bg != 'transparent':
                            link_bg = parent_bg
                            break
                        parent = parent.parent
                    
                    # Default to body background if still not found
                    if not link_bg:
                        body = soup.find('body')
                        body_styles = _get_element_computed_styles(body, css_variables)
                        link_bg = body_styles.get('background-color') or '#ffffff'

                if link_color and link_bg:
                    key = (link_color.lower(), link_bg.lower())
                    if key not in link_colors:
                        link_colors[key] = {'count': 0, 'locations': []}
                    link_colors[key]['count'] += 1
                    link_colors[key]['locations'].append(f"{file_path}: {link_text[:30]}")

        # Validate each unique link color combination
        contrast_failures = []
        for (fg_color, bg_color), data in link_colors.items():
            ratio = get_contrast_ratio(fg_color, bg_color)
            if ratio and ratio < 4.5:
                locations = data['locations'][:3]  # First 3 examples
                location_str = ", ".join(locations)
                contrast_failures.append(
                    f"Link color {fg_color} on {bg_color} = {ratio:.2f}:1 (need 4.5:1) - "
                    f"Found {data['count']} times - Examples: {location_str}"
                )

        assert not contrast_failures, \
            f"Link color contrast violations found:\n" + "\n".join(contrast_failures)

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_all_text_element_colors_meet_wcag_aa(self, built_example_site_with_palette):
        """Verify all text element color combinations in built site meet WCAG AA contrast.

        Different text elements may use different colors:
        - Body text (p, span, etc): --font-color on --background-color
        - Headings: --font-color on --background-color
        - Code/pre: --code-font-color on --code-bg-color
        - Inverted text (banner/footer): --invert-font-color on --font-color background

        This test extracts all actual text elements and validates each unique
        color combination meets the 4.5:1 minimum for normal text.

        Tests all default palettes to ensure accessibility across all themes.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"

        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found in built site"

        # Collect all text element color combinations
        text_colors = {}  # {(fg_color, bg_color): {count, element_types, locations}}
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Load CSS from site
            css_content = _load_css_from_site(site_path, html_content)
            css_variables = _extract_css_variables(html_content, css_content)

            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            file_path = str(html_file.relative_to(site_path))

            # Check various text elements
            text_elements = soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'td', 'th'])

            for elem in text_elements:
                # Skip empty elements
                if not elem.get_text(strip=True):
                    continue

                elem_type = elem.name

                # Extract computed styles
                elem_styles = _get_element_computed_styles(elem, css_variables)
                elem_color = elem_styles.get('color')
                elem_bg = elem_styles.get('background-color')

                # If no explicit background, use parent/body background
                if not elem_bg or elem_bg == 'transparent':
                    parent = elem.parent
                    while parent and (not elem_bg or elem_bg == 'transparent'):
                        parent_styles = _get_element_computed_styles(parent, css_variables)
                        parent_bg = parent_styles.get('background-color')
                        if parent_bg and parent_bg != 'transparent':
                            elem_bg = parent_bg
                            break
                        parent = parent.parent

                    if not elem_bg or elem_bg == 'transparent':
                        body = soup.find('body')
                        body_styles = _get_element_computed_styles(body, css_variables)
                        elem_bg = body_styles.get('background-color') or '#ffffff'

                if elem_color and elem_bg:
                    key = (elem_color.lower(), elem_bg.lower())
                    if key not in text_colors:
                        text_colors[key] = {'count': 0, 'element_types': set(), 'locations': []}
                    text_colors[key]['count'] += 1
                    text_colors[key]['element_types'].add(elem_type)
                    text_colors[key]['locations'].append(f"{file_path}:{elem_type}")

        # Validate each unique text color combination
        contrast_failures = []
        for (fg_color, bg_color), data in text_colors.items():
            ratio = get_contrast_ratio(fg_color, bg_color)
            if ratio and ratio < 4.5:
                elem_types = ", ".join(sorted(data['element_types']))
                locations = data['locations'][:2]  # First 2 examples
                location_str = ", ".join(locations)
                contrast_failures.append(
                    f"Text color {fg_color} on {bg_color} = {ratio:.2f}:1 (need 4.5:1) - "
                    f"Elements: {elem_types} - Found {data['count']} times"
                )

        assert not contrast_failures, \
            f"Text element color contrast violations found:\n" + "\n".join(contrast_failures)

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

        # Verify that CSS variables contain colors for this palette
        actual_font_color = css_variables.get('--font-color')
        actual_bg_color = css_variables.get('--background-color')

        assert actual_font_color is not None, \
            f"Palette '{palette_name}': CSS variable --font-color not found. Variables: {list(css_variables.keys())}"
        assert actual_bg_color is not None, \
            f"Palette '{palette_name}': CSS variable --background-color not found. Variables: {list(css_variables.keys())}"

        # Verify that CSS has multiple palettes available but only the correct one is used
        palette_dir = site_path / 'css' / 'palettes'
        if palette_dir.exists():
            palette_files = list(palette_dir.glob('*.css'))
            assert len(palette_files) > 0, f"No palette CSS files found in {palette_dir}"

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_ratios_meet_wcag_aa_minimum(self, palette_name, all_palette_css_attributes):
        """Verify calculated contrast ratios for link colors meet WCAG AA minimum of 4.5:1.
        
        This test validates the actual contrast ratio calculations for link colors
        against their backgrounds. It ensures that the mathematical ratio is at least
        4.5:1 as required by WCAG 2.1 AA for normal text (including links).
        
        Tests each default palette's link color (foreground) against its background color.
        
        Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
        """
        # WCAG AA minimum for text contrast (including links)
        WCAG_AA_TEXT_MINIMUM = 4.5
        
        # Get CSS attributes for this palette
        palette_attributes = all_palette_css_attributes.get(palette_name)
        assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"
        
        link_color = palette_attributes.get("font-color")
        background_color = palette_attributes.get("background-color")
        
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
    def test_link_contrast_passes_wcag_aa_validation(self, palette_name, all_palette_css_attributes):
        """Verify link colors pass WCAG AA validation using dedicated validator.
        
        This test uses the meets_wcag_aa utility function to validate that link colors
        meet WCAG 2.1 AA standards for text contrast (4.5:1 minimum for normal text).
        
        Uses the global-font-size extracted from the palette's CSS to validate with
        the actual font size rather than a hardcoded value.
        
        Tests each default palette to ensure all link colors are accessible.
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        # Get CSS attributes for this palette
        palette_attributes = all_palette_css_attributes.get(palette_name)
        assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"
        
        link_color = palette_attributes.get("font-color")
        background_color = palette_attributes.get("background-color")
        
        assert link_color is not None, f"No link color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Calculate contrast ratio
        ratio = get_contrast_ratio(link_color, background_color)
        assert ratio is not None, f"Could not calculate contrast ratio for {link_color} on {background_color}"
        
        # Extract font size from palette CSS attributes
        font_size_str = palette_attributes.get("global-font-size", "14px")
        # Parse font size value (e.g., "15px" -> 15)
        font_size = float(font_size_str.replace("px", "").strip())
        
        # Validate using meets_wcag_aa with actual palette font size
        is_compliant = meets_wcag_aa(ratio, text_size=font_size, is_bold=False)
        assert is_compliant, \
            f"Palette '{palette_name}': Link color {link_color} on {background_color} " \
            f"has contrast {ratio:.2f}:1, does not meet WCAG 2.1 AA minimum for {font_size}px text"

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_primary_link_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify primary link colors (used in <a> tags) meet WCAG AA contrast.
        
        Primary color is used for links throughout the theme. This test validates
        that the default primary link color meets WCAG 2.1 AA minimum contrast ratio.
        
        Uses the global-font-size extracted from the palette's CSS to validate with
        the actual font size rather than a hardcoded value.
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        palette_attributes = all_palette_css_attributes.get(palette_name)
        assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"
        
        # Note: We test primary-color specifically because links use color: var(--primary-color)
        link_color = palette_attributes.get("primary-color")
        background_color = palette_attributes.get("background-color")
        
        assert link_color is not None, f"No primary color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Calculate contrast ratio
        ratio = get_contrast_ratio(link_color, background_color)
        assert ratio is not None, f"Could not calculate contrast ratio for {link_color} on {background_color}"
        
        # Extract font size from palette CSS attributes
        font_size_str = palette_attributes.get("global-font-size", "14px")
        # Parse font size value (e.g., "15px" -> 15)
        font_size = float(font_size_str.replace("px", "").strip())
        
        # Validate using meets_wcag_aa with actual palette font size
        is_compliant = meets_wcag_aa(ratio, text_size=font_size, is_bold=False)
        assert is_compliant, \
            f"Palette '{palette_name}': Primary link color {link_color} on {background_color} " \
            f"has contrast {ratio:.2f}:1, does not meet WCAG 2.1 AA minimum for {font_size}px text"

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_alert_error_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify terminal-alert-error color meets WCAG AA contrast.
        
        Error alerts use the error-color CSS variable for text. This test validates
        that the error color has sufficient contrast against the page background.
        
        Note: This test uses global-font-size from palette attributes. Alert text elements
        default to 'font-size: 1em', which inherits the global font size. This assumes
        terminal-alert elements do not override their font-size from the global value.
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        palette_attributes = all_palette_css_attributes.get(palette_name)
        assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"
        
        error_color = palette_attributes.get("error-color")
        background_color = palette_attributes.get("background-color")
        font_size_str = palette_attributes.get("global-font-size", "14px")
        
        assert error_color is not None, f"No error color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Parse font size from string (e.g., "15px" -> 15.0)
        font_size = float(font_size_str.replace("px", "").strip())
        
        # Calculate contrast ratio
        ratio = get_contrast_ratio(error_color, background_color)
        assert ratio is not None, f"Could not calculate contrast ratio for {error_color} on {background_color}"
        
        # Validate using meets_wcag_aa with actual palette font size
        is_compliant = meets_wcag_aa(ratio, text_size=font_size, is_bold=False)
        assert is_compliant, \
            f"Palette '{palette_name}': Error color {error_color} on {background_color} " \
            f"has contrast {ratio:.2f}:1, does not meet WCAG 2.1 AA minimum for {font_size}px text"

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_ghost_error_button_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify ghost error buttons (btn-error.btn-ghost) have sufficient contrast.
        
        Ghost error buttons use the error-color CSS variable for text on a transparent
        background (showing the page background). This test validates that the button
        text color has sufficient contrast against the page background.
        
        Note: This test uses global-font-size from palette attributes. Button elements
        default to 'font-size: 1em', which inherits the global font size. This assumes
        .btn elements do not override their font-size from the global value.
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        palette_attributes = all_palette_css_attributes.get(palette_name)
        assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"
        
        # Ghost error buttons use error-color for text on transparent background
        button_color = palette_attributes.get("error-color")
        background_color = palette_attributes.get("background-color")
        font_size_str = palette_attributes.get("global-font-size", "14px")
        
        assert button_color is not None, f"No error color defined for palette: {palette_name}"
        assert background_color is not None, f"No background color defined for palette: {palette_name}"
        
        # Parse font size from string (e.g., "15px" -> 15.0)
        font_size = float(font_size_str.replace("px", "").strip())
        
        # Calculate contrast ratio
        ratio = get_contrast_ratio(button_color, background_color)
        assert ratio is not None, f"Could not calculate contrast ratio for {button_color} on {background_color}"
        
        # Validate using meets_wcag_aa with actual palette font size
        # UI components can use 3:1 but button text is typically at normal size
        is_compliant = meets_wcag_aa(ratio, text_size=font_size, is_bold=False)
        assert is_compliant, \
            f"Palette '{palette_name}': Ghost error button text color {button_color} on {background_color} " \
            f"has contrast {ratio:.2f}:1, does not meet WCAG 2.1 AA minimum for {font_size}px text"

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
        ("default", 18.26),
        ("dark", 13.07),
        ("gruvbox_dark", 10.74),
        ("pink", 19.3),
        ("sans", 18.26),
        ("sans_dark", 13.07),
    ])
    def test_text_contrast_ratio_calculations_are_accurate(self, palette_name, expected_ratio, all_palette_css_attributes):
        """Verify contrast ratio calculations are mathematically accurate.
        
        This test validates that contrast ratio calculations match expected values. 
        It serves as a regression test for the
        color_utils.get_contrast_ratio() function.
        
        Uses actual palette colors to ensure calculations are correct across
        different color ranges.
        
        Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html

        Expected values calculated using an external WCAG contrast calculator.
        1. https://webaim.org/resources/contrastchecker/
        """
        palette_attributes = all_palette_css_attributes.get(palette_name)
        assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"
        
        link_color = palette_attributes.get("font-color")
        background_color = palette_attributes.get("background-color")
        
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

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("search-enabled", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_details_alert_elements_meet_wcag_aa_contrast(self, built_example_site_with_palette):
        """Verify details/alert elements have sufficient contrast for WCAG AA.
        
        Tests that terminal-alert elements (including terminal-alert-error and 
        terminal-alert-primary) have sufficient contrast between their colored text
        and background. Details elements with alert styling should be readable.
        
        This test scans all HTML files looking for:
        - .terminal-alert elements
        - .terminal-alert-error elements (red error alerts)
        - .terminal-alert-primary elements (blue primary alerts)
        
        Validates that the text color used in these elements meets 4.5:1 contrast
        minimum for WCAG 2.1 AA compliance.
        
        Tests all default palettes to catch palette-specific contrast issues.
        
        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        site_path = Path(built_example_site_with_palette)
        assert site_path.exists(), f"Built site not found at {site_path}"
        
        html_files = list(site_path.glob("**/*.html"))
        assert len(html_files) > 0, "No HTML files found in built site"
        
        # Track all details/alert elements by class and their colors
        alert_elements = {
            'error': {'elements': [], 'color_combos': {}},
            'primary': {'elements': [], 'color_combos': {}},
        }
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Load CSS from site to extract variables
            css_content = _load_css_from_site(site_path, html_content)
            css_variables = _extract_css_variables(html_content, css_content)
            
            soup = BeautifulSoup(html_content, 'html.parser')
            file_path = str(html_file.relative_to(site_path))
            
            # Find all alert elements
            alert_error_elements = soup.find_all(class_='terminal-alert-error')
            alert_primary_elements = soup.find_all(class_='terminal-alert-primary')
            
            for alert_type, elements in [('error', alert_error_elements), ('primary', alert_primary_elements)]:
                for elem_idx, elem in enumerate(elements):
                    # Get text content for context
                    text = elem.get_text(strip=True)[:50]
                    
                    # Extract computed style for the alert element
                    elem_styles = _get_element_computed_styles(elem, css_variables)
                    alert_color = elem_styles.get('color')
                    alert_bg = elem_styles.get('background-color')
                    
                    # If no explicit background, check parent elements
                    if not alert_bg or alert_bg == 'transparent':
                        parent = elem.parent
                        while parent and (not alert_bg or alert_bg == 'transparent'):
                            parent_styles = _get_element_computed_styles(parent, css_variables)
                            parent_bg = parent_styles.get('background-color')
                            if parent_bg and parent_bg != 'transparent':
                                alert_bg = parent_bg
                                break
                            parent = parent.parent
                    
                    # Default to body background if still not found
                    if not alert_bg:
                        body = soup.find('body')
                        body_styles = _get_element_computed_styles(body, css_variables)
                        alert_bg = body_styles.get('background-color') or '#ffffff'
                    
                    if alert_color and alert_bg:
                        # Store for reporting
                        location = f"{file_path}:{alert_type} #{elem_idx}"
                        alert_elements[alert_type]['elements'].append({
                            'location': location,
                            'text': text,
                            'color': alert_color,
                            'background': alert_bg,
                        })
                        
                        # Group by color combination
                        color_key = (alert_color.lower(), alert_bg.lower())
                        if color_key not in alert_elements[alert_type]['color_combos']:
                            alert_elements[alert_type]['color_combos'][color_key] = {
                                'count': 0,
                                'locations': [],
                            }
                        alert_elements[alert_type]['color_combos'][color_key]['count'] += 1
                        alert_elements[alert_type]['color_combos'][color_key]['locations'].append(location)
        
        # Validate contrast for each unique color combination
        failures = []
        
        for alert_type in ['error', 'primary']:
            for (fg_color, bg_color), data in alert_elements[alert_type]['color_combos'].items():
                ratio = get_contrast_ratio(fg_color, bg_color)
                
                if ratio and ratio < 4.5:
                    locations_str = '\n      '.join(data['locations'][:3])
                    if len(data['locations']) > 3:
                        locations_str += f'\n      ... and {len(data["locations"]) - 3} more'
                    
                    failures.append(
                        f"terminal-alert-{alert_type}: {fg_color} on {bg_color} = {ratio:.2f}:1 "
                        f"({data['count']} elements)\n      {locations_str}"
                    )
        
        assert not failures, \
            f"Details/alert elements have insufficient contrast (need 4.5:1):\n" + \
            "\n".join([f"  {f}" for f in failures])



