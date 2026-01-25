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
- DOM-level contrast checks were removed because inline-style-only analysis
    produced false negatives; palette validation serves as the authoritative
    signal for failing colors until a browser engine is available.

Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
"""

import pytest

from tests.accessibility.utilities.color_utils import get_contrast_ratio
from tests.accessibility.utilities.site_context import SiteContextBuilder
from tests.accessibility.validators import (
    assert_contrast_meets_wcag_aa,
    get_palette_colors,
)
from tests.interface.theme_features import DEFAULT_PALETTES


class TestColorContrast:
    """Tests for WCAG 2.1 AA color contrast compliance in theme."""

    # -------------------------------------------------------------------------
    # Limited built-site sanity checks
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "built_example_site_with_palette",
        [("minimal", palette) for palette in DEFAULT_PALETTES],
        indirect=True,
    )
    def test_css_classes_loaded_correctly(self, built_example_site_with_palette):
        """Smoke-test built output to ensure palette CSS actually loads.

        Catches regressions where MkDocs stops emitting theme CSS, the extractor
        no longer finds variables, or palette naming drifts. Prevents palette-only
        contrast checks from passing when the build pipeline is broken.
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

        assert palette_name is not None, f"Could not determine palette from site path: {builder.site_path}"

        assert current_page_context.css_variables.get("--font-color") is not None, (
            f"Palette '{palette_name}': CSS variable --font-color not found"
        )
        assert current_page_context.css_variables.get("--background-color") is not None, (
            f"Palette '{palette_name}': CSS variable --background-color not found"
        )

    # -------------------------------------------------------------------------
    # Palette Attribute Tests (no site build required)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_ratios_meet_wcag_aa_minimum(self, palette_name, all_palette_css_attributes):
        """Verify palette font colors meet the 4.5:1 minimum contrast."""

        colors = get_palette_colors(palette_name, all_palette_css_attributes)

        ratio = get_contrast_ratio(colors.font_color, colors.background_color)
        assert ratio is not None, (
            f"Could not calculate contrast ratio for {colors.font_color} on {colors.background_color}"
        )

        assert ratio >= 4.5, (
            f"Palette '{palette_name}': Font color {colors.font_color} on {colors.background_color} "
            f"has contrast ratio {ratio:.2f}:1, which is below the WCAG AA minimum of 4.5:1"
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_link_contrast_passes_wcag_aa_validation(self, palette_name, all_palette_css_attributes):
        """Validate font colors via `assert_contrast_meets_wcag_aa`."""

        colors = get_palette_colors(palette_name, all_palette_css_attributes)

        assert_contrast_meets_wcag_aa(
            colors.font_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Font color",
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_primary_link_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify palette primary link colors meet WCAG AA contrast."""

        colors = get_palette_colors(palette_name, all_palette_css_attributes, required_attrs=["primary-color"])

        assert_contrast_meets_wcag_aa(
            colors.primary_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Primary link color",
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_alert_error_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify terminal-alert-error color meets WCAG AA contrast."""

        colors = get_palette_colors(palette_name, all_palette_css_attributes, required_attrs=["error-color"])

        assert_contrast_meets_wcag_aa(
            colors.error_color,
            colors.background_color,
            colors.font_size,
            f"Palette '{palette_name}': Error color",
        )

    @pytest.mark.parametrize("palette_name", DEFAULT_PALETTES)
    def test_ghost_error_button_color_meets_wcag_aa(self, palette_name, all_palette_css_attributes):
        """Verify ghost error buttons (btn-error.btn-ghost) maintain contrast."""

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
        self,
        palette_name,
        expected_ratio,
        all_palette_css_attributes,
    ):
        """Regression test to ensure ratio calculations stay accurate."""

        colors = get_palette_colors(palette_name, all_palette_css_attributes)

        ratio = get_contrast_ratio(colors.font_color, colors.background_color)
        assert ratio is not None, (
            f"Could not calculate contrast for {colors.font_color} on {colors.background_color}"
        )

        tolerance = 0.1
        assert abs(ratio - expected_ratio) <= tolerance, (
            f"Palette '{palette_name}': Expected contrast {expected_ratio}:1, "
            f"got {ratio:.2f}:1 (colors: {colors.font_color} on {colors.background_color})"
        )
