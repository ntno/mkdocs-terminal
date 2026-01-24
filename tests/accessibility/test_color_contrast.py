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
import re

from tests.accessibility.utilities import _get_element_computed_styles
from tests.accessibility.utilities.color_utils import get_contrast_ratio
from tests.accessibility.utilities.site_context import SiteContextBuilder
from tests.accessibility.utils import validate_color_contrast
from tests.accessibility.validators import (
    BackgroundColorResolver,
    ColorCombinationTracker,
    assert_contrast_meets_wcag_aa,
    get_palette_colors,
)
from tests.interface.theme_features import DEFAULT_PALETTES


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------


class TestColorContrast:
    """Tests for WCAG 2.1 AA color contrast compliance in theme."""

    # -------------------------------------------------------------------------
    # Built Site Tests (parametrized by palette)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("search-enabled", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_theme_body_text_contrast_meets_wcag_aa(self, built_example_site_with_palette):
        """Verify theme body text color meets WCAG AA contrast against background.

        Theme-controlled text colors (default body text, paragraphs) must meet
        WCAG 2.1 AA minimum contrast ratio of 4.5:1 for normal text.

        Validates: Default text color has sufficient contrast with background.
        """
        builder = SiteContextBuilder(built_example_site_with_palette)

        all_violations = []
        for current_page_context in builder.iter_html_files():
            violations = validate_color_contrast(
                current_page_context.html_content,
                filename=current_page_context.relative_path,
                css_content=current_page_context.css_content,
            )
            all_violations.extend(violations)

        if all_violations:
            pytest.fail(f"Color contrast violations found:\n" + "\n".join(all_violations))

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("minimal", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_all_link_color_combinations_meet_wcag_aa(self, built_example_site_with_palette):
        """Verify all unique link color combinations in built site meet WCAG AA contrast.

        Extracts all link elements and their computed colors, groups by unique
        color combination, and validates each meets 4.5:1 minimum.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        builder = SiteContextBuilder(built_example_site_with_palette)
        tracker = ColorCombinationTracker()

        for current_page_context in builder.iter_html_files():
            background_resolver = BackgroundColorResolver(
                current_page_context.css_variables,
                current_page_context.soup,
            )

            for link in current_page_context.soup.find_all("a"):
                link_text = link.get_text(strip=True)[:40]
                if not link_text:
                    continue

                link_styles = _get_element_computed_styles(link, current_page_context.css_variables)
                link_color = link_styles.get("color")
                if not link_color:
                    continue

                link_bg = background_resolver.resolve(link)

                if link_color and link_bg:
                    tracker.add(link_color, link_bg, f"{current_page_context.relative_path}: {link_text[:30]}")

        failures = tracker.get_failures(min_ratio=4.5)
        assert not failures, f"Link color contrast violations found:\n" + "\n".join(failures)

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("minimal", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_all_text_element_colors_meet_wcag_aa(self, built_example_site_with_palette):
        """Verify all text element color combinations in built site meet WCAG AA contrast.

        Checks p, span, headings, list items, blockquotes, and table cells.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        builder = SiteContextBuilder(built_example_site_with_palette)
        tracker = ColorCombinationTracker()

        text_tags = ["p", "span", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "td", "th"]

        for current_page_context in builder.iter_html_files():
            background_resolver = BackgroundColorResolver(
                current_page_context.css_variables,
                current_page_context.soup,
            )

            for elem in current_page_context.soup.find_all(text_tags):
                if not elem.get_text(strip=True):
                    continue

                elem_styles = _get_element_computed_styles(elem, current_page_context.css_variables)
                elem_color = elem_styles.get("color")
                if not elem_color:
                    continue

                elem_bg = background_resolver.resolve(elem)

                if elem_color and elem_bg:
                    tracker.add(elem_color, elem_bg, f"{current_page_context.relative_path}:{elem.name}", elem.name)

        failures = tracker.get_failures(min_ratio=4.5)
        assert not failures, f"Text element color contrast violations found:\n" + "\n".join(failures)

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("minimal", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_theme_button_and_form_contrast_meets_wcag_aa(self, built_example_site_with_palette):
        """Verify theme button and form control colors meet WCAG AA contrast.

        Theme-provided button and form control colors must meet WCAG 2.1 AA
        minimum contrast ratio of 3:1 for UI components.

        Validates: Button and form element colors have sufficient contrast.
        """
        builder = SiteContextBuilder(built_example_site_with_palette)

        all_violations = []
        for current_page_context in builder.iter_html_files():
            violations = validate_color_contrast(
                current_page_context.html_content,
                filename=current_page_context.relative_path,
                css_content=current_page_context.css_content,
            )
            form_violations = [
                v for v in violations if any(term in v.lower() for term in ["button", "input", "form", "label"])
            ]
            all_violations.extend(form_violations)

        if all_violations:
            pytest.fail(f"Button/form color contrast violations found:\n" + "\n".join(all_violations))

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("minimal", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_css_classes_loaded_correctly(self, built_example_site_with_palette):
        """Verify that CSS classes and variables are loaded correctly for each palette.

        Validates:
        - CSS files are found and loaded from the built site
        - CSS variables are correctly extracted from :root blocks
        - Expected palette colors are present in the extracted variables
        """
        builder = SiteContextBuilder(built_example_site_with_palette)

        html_file = builder.site_path / "index.html"
        assert html_file.exists(), f"HTML file not found at {html_file}"

        current_page_context = builder.build_context(html_file)
        assert len(current_page_context.css_content) > 0, "No CSS content loaded from site"
        assert len(current_page_context.css_variables) > 0, "No CSS variables extracted"

        # Determine palette from site path
        palette_name = None
        for palette in sorted(DEFAULT_PALETTES, key=len, reverse=True):
            if f"_{palette}_site" in str(builder.site_path):
                palette_name = palette
                break

        assert palette_name is not None, f"Could not determine palette from site path: {site_path}"

        assert current_page_context.css_variables.get("--font-color") is not None, (
            f"Palette '{palette_name}': CSS variable --font-color not found"
        )
        assert current_page_context.css_variables.get("--background-color") is not None, (
            f"Palette '{palette_name}': CSS variable --background-color not found"
        )

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("minimal", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_all_links_in_site_meet_wcag_aa_contrast(self, built_example_site_with_palette):
        """Verify all rendered links in built site meet WCAG AA contrast requirements.

        Scans all HTML files and validates inline-styled links have sufficient contrast.

        Limitations:
        - Tests static HTML colors; hover/focus states require browser automation
        - Only validates inline-styled links (CSS class resolution is limited)

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        builder = SiteContextBuilder(built_example_site_with_palette)
        contrast_failures = []

        for current_page_context in builder.iter_html_files():
            for link_index, link in enumerate(current_page_context.soup.find_all("a")):
                link_text = link.get_text(strip=True)[:50]
                style = link.get("style", "")

                color_match = re.search(r"color\s*:\s*([^;]+)", style, re.IGNORECASE)
                link_color = color_match.group(1).strip() if color_match else None

                bg_match = re.search(r"background(?:-color)?\s*:\s*([^;]+)", style, re.IGNORECASE)
                bg_color = bg_match.group(1).strip() if bg_match else None

                if link_color and bg_color:
                    ratio = get_contrast_ratio(link_color, bg_color)
                    if ratio and ratio < 4.5:
                        contrast_failures.append(
                            f"{current_page_context.relative_path} (link {link_index}): '{link_text}' "
                            f"has contrast {ratio:.2f}:1 (need 4.5:1)"
                        )

        assert not contrast_failures, f"Link contrast violations found:\n" + "\n".join(contrast_failures)

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("search-enabled", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_details_alert_elements_meet_wcag_aa_contrast(self, built_example_site_with_palette):
        """Verify details/alert elements have sufficient contrast for WCAG AA.

        Tests terminal-alert elements (error and primary variants) have sufficient
        contrast between their colored text and background.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        builder = SiteContextBuilder(built_example_site_with_palette)

        alert_trackers = {
            "error": ColorCombinationTracker(),
            "primary": ColorCombinationTracker(),
        }

        for current_page_context in builder.iter_html_files():
            background_resolver = BackgroundColorResolver(
                current_page_context.css_variables,
                current_page_context.soup,
            )
            for alert_type, class_name in [
                ("error", "terminal-alert-error"),
                ("primary", "terminal-alert-primary"),
            ]:
                for elem_idx, elem in enumerate(current_page_context.soup.find_all(class_=class_name)):
                    elem_styles = _get_element_computed_styles(elem, current_page_context.css_variables)
                    alert_color = elem_styles.get("color")
                    if not alert_color:
                        continue

                    alert_bg = background_resolver.resolve(elem)

                    if alert_color and alert_bg:
                        location = f"{current_page_context.relative_path}:{alert_type} #{elem_idx}"
                        alert_trackers[alert_type].add(alert_color, alert_bg, location)

        all_failures = []
        for alert_type, tracker in alert_trackers.items():
            for failure in tracker.get_failures(min_ratio=4.5):
                all_failures.append(f"terminal-alert-{alert_type}: {failure}")

        assert not all_failures, (
            f"Details/alert elements have insufficient contrast (need 4.5:1):\n" + "\n".join(all_failures)
        )

    # -------------------------------------------------------------------------
    # Palette Attribute Tests (no site build required)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_ratios_meet_wcag_aa_minimum(self, palette_name, all_palette_css_attributes):
        """Verify calculated contrast ratios for font colors meet WCAG AA minimum of 4.5:1.

        Tests each default palette's font color (foreground) against its background color.

        Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
        """
        colors = get_palette_colors(palette_name, all_palette_css_attributes)

        ratio = get_contrast_ratio(colors.font_color, colors.background_color)
        assert ratio is not None, f"Could not calculate contrast ratio for {colors.font_color} on {colors.background_color}"

        assert ratio >= 4.5, (
            f"Palette '{palette_name}': Font color {colors.font_color} on {colors.background_color} "
            f"has contrast ratio {ratio:.2f}:1, which is below the WCAG AA minimum of 4.5:1"
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_passes_wcag_aa_validation(self, palette_name, all_palette_css_attributes):
        """Verify font colors pass WCAG AA validation using meets_wcag_aa validator.

        Uses the global-font-size extracted from the palette's CSS.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        colors = get_palette_colors(palette_name, all_palette_css_attributes)

        assert_contrast_meets_wcag_aa(
            colors.font_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Font color",
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_primary_link_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify primary link colors (used in <a> tags) meet WCAG AA contrast.

        Primary color is used for links throughout the theme.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        colors = get_palette_colors(palette_name, all_palette_css_attributes, required_attrs=["primary-color"])

        assert_contrast_meets_wcag_aa(
            colors.primary_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Primary link color",
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_alert_error_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify terminal-alert-error color meets WCAG AA contrast.

        Error alerts use the error-color CSS variable for text.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        colors = get_palette_colors(palette_name, all_palette_css_attributes, required_attrs=["error-color"])

        assert_contrast_meets_wcag_aa(
            colors.error_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Error color",
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_ghost_error_button_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify ghost error buttons (btn-error.btn-ghost) have sufficient contrast.

        Ghost error buttons use error-color for text on transparent background.

        Reference: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
        """
        colors = get_palette_colors(palette_name, all_palette_css_attributes, required_attrs=["error-color"])

        assert_contrast_meets_wcag_aa(
            colors.error_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Ghost error button text color",
        )

    @pytest.mark.parametrize(
        "palette_name,expected_ratio",
        [
            ("default", 18.26),
            ("dark", 13.07),
            ("gruvbox_dark", 10.74),
            ("pink", 19.3),
            ("sans", 18.26),
            ("sans_dark", 13.07),
        ],
    )
    def test_text_contrast_ratio_calculations_are_accurate(
        self, palette_name, expected_ratio, all_palette_css_attributes
    ):
        """Verify contrast ratio calculations are mathematically accurate.

        Serves as a regression test for color_utils.get_contrast_ratio().

        Expected values calculated using WebAIM contrast checker:
        https://webaim.org/resources/contrastchecker/

        Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
        """
        colors = get_palette_colors(palette_name, all_palette_css_attributes)

        ratio = get_contrast_ratio(colors.font_color, colors.background_color)
        assert ratio is not None, f"Could not calculate contrast for {colors.font_color} on {colors.background_color}"

        tolerance = 0.1
        assert abs(ratio - expected_ratio) <= tolerance, (
            f"Palette '{palette_name}': Expected contrast {expected_ratio}:1, "
            f"got {ratio:.2f}:1 (colors: {colors.font_color} on {colors.background_color})"
        )



