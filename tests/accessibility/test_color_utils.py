"""Unit tests for color utility functions.

Tests color parsing, contrast ratio calculation, and WCAG compliance checking.

Reference: https://www.w3.org/TR/WCAG20-TECHS/G17.html
"""

import pytest
from tests.accessibility.color_utils import (
    normalize_color,
    get_relative_luminance,
    get_contrast_ratio,
    meets_wcag_aa,
)


class TestColorNormalization:
    """Tests for color string parsing and normalization."""

    def test_normalize_hex_6_digit(self):
        """Test 6-digit hex color parsing."""
        assert normalize_color("#ffffff") == (1.0, 1.0, 1.0)
        assert normalize_color("#000000") == (0.0, 0.0, 0.0)
        assert normalize_color("#ff0000") == (1.0, 0.0, 0.0)
        assert normalize_color("#00ff00") == (0.0, 1.0, 0.0)
        assert normalize_color("#0000ff") == (0.0, 0.0, 1.0)

    def test_normalize_hex_3_digit(self):
        """Test 3-digit hex color expansion."""
        # #fff should expand to #ffffff
        assert normalize_color("#fff") == (1.0, 1.0, 1.0)
        assert normalize_color("#000") == (0.0, 0.0, 0.0)
        assert normalize_color("#f00") == (1.0, 0.0, 0.0)

    def test_normalize_hex_case_insensitive(self):
        """Test that hex parsing is case-insensitive."""
        assert normalize_color("#FFFFFF") == (1.0, 1.0, 1.0)
        assert normalize_color("#FFF") == (1.0, 1.0, 1.0)
        assert normalize_color("#aAbBcC") == normalize_color("#aabbcc")

    def test_normalize_rgb_decimal(self):
        """Test rgb() notation with 0-255 range."""
        result = normalize_color("rgb(255, 0, 0)")
        assert result is not None
        assert abs(result[0] - 1.0) < 0.01  # Red
        assert abs(result[1] - 0.0) < 0.01  # Green
        assert abs(result[2] - 0.0) < 0.01  # Blue

    def test_normalize_rgb_whitespace(self):
        """Test rgb() notation with variable whitespace."""
        result1 = normalize_color("rgb(255,0,0)")
        result2 = normalize_color("rgb( 255 , 0 , 0 )")
        assert result1 == result2

    def test_normalize_named_colors(self):
        """Test CSS named color parsing."""
        assert normalize_color("white") == (1.0, 1.0, 1.0)
        assert normalize_color("black") == (0.0, 0.0, 0.0)
        assert normalize_color("red") == (1.0, 0.0, 0.0)
        assert normalize_color("green") == (0.0, 0.5019607843137255, 0.0)
        assert normalize_color("blue") == (0.0, 0.0, 1.0)

    def test_normalize_transparent(self):
        """Test transparent color handling."""
        assert normalize_color("transparent") is None
        assert normalize_color("rgba(0,0,0,0)") is None

    def test_normalize_invalid_color(self):
        """Test invalid color strings return None."""
        assert normalize_color("notacolor") is None
        assert normalize_color("") is None
        assert normalize_color(None) is None


class TestRelativeLuminance:
    """Tests for relative luminance calculation."""

    def test_luminance_white(self):
        """White should have luminance of 1.0."""
        result = get_relative_luminance((1.0, 1.0, 1.0))
        assert abs(result - 1.0) < 0.01

    def test_luminance_black(self):
        """Black should have luminance of 0.0."""
        result = get_relative_luminance((0.0, 0.0, 0.0))
        assert abs(result - 0.0) < 0.01

    def test_luminance_gray(self):
        """Gray should have intermediate luminance."""
        result = get_relative_luminance((0.5, 0.5, 0.5))
        assert 0.2 < result < 0.3  # Approximate expected range


class TestContrastRatio:
    """Tests for contrast ratio calculation."""

    def test_contrast_black_white(self):
        """Black and white should have maximum contrast (21:1)."""
        ratio = get_contrast_ratio("#000000", "#ffffff")
        assert ratio is not None
        assert abs(ratio - 21.0) < 0.1

    def test_contrast_same_color(self):
        """Same color should have minimum contrast (1:1)."""
        ratio = get_contrast_ratio("#808080", "#808080")
        assert ratio is not None
        assert abs(ratio - 1.0) < 0.1

    def test_contrast_order_independent(self):
        """Contrast ratio should be the same regardless of argument order."""
        ratio1 = get_contrast_ratio("#000000", "#ffffff")
        ratio2 = get_contrast_ratio("#ffffff", "#000000")
        assert ratio1 == ratio2

    def test_contrast_common_pairs(self):
        """Test common color pairs."""
        # Black text on white background (should pass WCAG AAA)
        black_on_white = get_contrast_ratio("#000000", "#ffffff")
        assert black_on_white is not None
        assert black_on_white >= 18.0

        # Gray text on white (should fail WCAG AA)
        gray_on_white = get_contrast_ratio("#888888", "#ffffff")
        assert gray_on_white is not None
        assert gray_on_white < 4.5

    def test_contrast_invalid_colors(self):
        """Invalid colors should return None."""
        assert get_contrast_ratio("#invalidcolor", "#ffffff") is None
        assert get_contrast_ratio("#000000", "#notacolor") is None
        assert get_contrast_ratio("transparent", "#ffffff") is None


class TestWCAGCompliance:
    """Tests for WCAG AA compliance checking."""

    def test_wcag_aa_normal_text_passing(self):
        """Test normal text that meets 4.5:1 requirement."""
        assert meets_wcag_aa(4.5, text_size=14, is_bold=False) is True
        assert meets_wcag_aa(7.0, text_size=14, is_bold=False) is True

    def test_wcag_aa_normal_text_failing(self):
        """Test normal text that doesn't meet 4.5:1 requirement."""
        assert meets_wcag_aa(3.0, text_size=14, is_bold=False) is False
        assert meets_wcag_aa(4.4, text_size=14, is_bold=False) is False

    def test_wcag_aa_large_text_passing(self):
        """Test large text that meets 3:1 requirement."""
        # 18pt = 24px
        assert meets_wcag_aa(3.0, text_size=24, is_bold=False) is True
        assert meets_wcag_aa(4.5, text_size=24, is_bold=False) is True

    def test_wcag_aa_large_text_failing(self):
        """Test large text that doesn't meet 3:1 requirement."""
        assert meets_wcag_aa(2.9, text_size=24, is_bold=False) is False
        assert meets_wcag_aa(1.5, text_size=24, is_bold=False) is False

    def test_wcag_aa_bold_text(self):
        """Test bold text large text threshold.
        
        Per WCAG 2.1 AA, "large text" is defined as:
        - 18pt (24px) or larger, OR
        - 14pt (18.67px) or larger and bold
        
        When text_size is 14px, bold text needs at least 18.67px to qualify as large.
        Since we're passing 14 (not 18.67), it should still require 4.5:1.
        """
        # 14px bold is less than 18.67px, so needs 4.5:1
        assert meets_wcag_aa(3.0, text_size=14, is_bold=True) is False
        assert meets_wcag_aa(4.5, text_size=14, is_bold=True) is True
        
        # 19px bold should use 3:1 threshold
        assert meets_wcag_aa(3.0, text_size=19, is_bold=True) is True

    def test_wcag_aa_none_ratio(self):
        """None ratio should not meet WCAG AA."""
        assert meets_wcag_aa(None, text_size=14) is False


class TestIntegrationWithRealColors:
    """Integration tests using real theme color pairs."""

    def test_black_text_on_white(self):
        """Black text on white background should pass WCAG AAA."""
        ratio = get_contrast_ratio("#000000", "#ffffff")
        assert ratio is not None
        assert meets_wcag_aa(ratio, text_size=14) is True

    def test_gray_text_on_white(self):
        """Medium gray text on white should fail WCAG AA."""
        ratio = get_contrast_ratio("#999999", "#ffffff")
        assert ratio is not None
        assert meets_wcag_aa(ratio, text_size=14) is False

    def test_dark_blue_text_on_white(self):
        """Dark blue text on white should pass WCAG AA."""
        ratio = get_contrast_ratio("#0066cc", "#ffffff")
        assert ratio is not None
        assert meets_wcag_aa(ratio, text_size=14) is True

    def test_light_colors_on_dark(self):
        """Light text on dark background."""
        ratio = get_contrast_ratio("#ffffff", "#333333")
        assert ratio is not None
        assert meets_wcag_aa(ratio, text_size=14) is True
