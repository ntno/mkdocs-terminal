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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set, Tuple

from bs4 import BeautifulSoup, Tag

from tests.accessibility.color_utils import get_contrast_ratio, meets_wcag_aa
from tests.accessibility.utils import (
    _extract_css_variables,
    _get_element_computed_styles,
    validate_color_contrast,
)
from tests.interface.theme_features import DEFAULT_PALETTES


# -----------------------------------------------------------------------------
# Helper: CSS Loading
# -----------------------------------------------------------------------------


def load_css_from_site(site_path: Path, html_content: str) -> str:
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
    loaded_paths: Set[Path] = set()
    active_palette = None

    soup = BeautifulSoup(html_content, "html.parser")
    head = soup.find("head")

    if head:
        link_tags = head.find_all("link", rel="stylesheet")

        for link in link_tags:
            href = link.get("href")
            if href and href.endswith(".css"):
                css_file = href.split("?")[0]

                palette_match = re.match(r".*/css/palettes/([^/]+)\.css$", css_file)
                if palette_match:
                    active_palette = palette_match.group(1)

                if css_file.startswith("/"):
                    css_path = site_path / css_file.lstrip("/")
                else:
                    css_path = site_path / css_file

                if css_path.exists():
                    try:
                        with open(css_path, "r", encoding="utf-8") as f:
                            css_content += f.read() + "\n"
                        loaded_paths.add(css_path.resolve())
                    except Exception:
                        pass

    if active_palette:
        palette_css_path = site_path / "css" / "palettes" / f"{active_palette}.css"
        resolved_path = palette_css_path.resolve()

        if palette_css_path.exists() and resolved_path not in loaded_paths:
            try:
                with open(palette_css_path, "r", encoding="utf-8") as f:
                    css_content += f.read() + "\n"
            except Exception:
                pass

    return css_content


# -----------------------------------------------------------------------------
# Helper: Site Context
# -----------------------------------------------------------------------------


@dataclass
class SiteContext:
    """Context for a single HTML file in a built site."""

    site_path: Path
    html_file: Path
    html_content: str
    css_content: str
    css_variables: Dict[str, str]
    soup: BeautifulSoup

    @property
    def relative_path(self) -> str:
        """File path relative to site root."""
        return str(self.html_file.relative_to(self.site_path))


def iter_site_html_files(site_path: Path) -> Iterator[SiteContext]:
    """Iterate over all HTML files in a built site with parsed context.

    Yields a SiteContext for each HTML file containing:
    - Parsed HTML (BeautifulSoup)
    - Loaded CSS content
    - Extracted CSS variables

    Args:
        site_path: Path to built site directory

    Yields:
        SiteContext for each HTML file
    """
    html_files = list(site_path.glob("**/*.html"))

    for html_file in html_files:
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        css_content = load_css_from_site(site_path, html_content)
        css_variables = _extract_css_variables(html_content, css_content)
        soup = BeautifulSoup(html_content, "html.parser")

        yield SiteContext(
            site_path=site_path,
            html_file=html_file,
            html_content=html_content,
            css_content=css_content,
            css_variables=css_variables,
            soup=soup,
        )


def get_site_path(built_example_site_with_palette: str) -> Path:
    """Get and validate the site path from fixture.

    Args:
        built_example_site_with_palette: Path string from fixture

    Returns:
        Validated Path object

    Raises:
        AssertionError: If site path doesn't exist or has no HTML files
    """
    site_path = Path(built_example_site_with_palette)
    assert site_path.exists(), f"Built site not found at {site_path}"

    html_files = list(site_path.glob("**/*.html"))
    assert len(html_files) > 0, f"No HTML files found in {site_path}"

    return site_path


# -----------------------------------------------------------------------------
# Helper: Background Color Resolution
# -----------------------------------------------------------------------------


def resolve_background_color(
    element: Tag,
    css_variables: Dict[str, str],
    soup: BeautifulSoup,
    default: str = "#ffffff",
) -> Optional[str]:
    """Resolve the effective background color for an element.

    Walks up the DOM tree to find the first non-transparent background color.
    Falls back to body background or the provided default.

    Args:
        element: The element to resolve background for
        css_variables: CSS variable definitions
        soup: BeautifulSoup document (for finding body)
        default: Default color if none found

    Returns:
        Resolved background color string
    """
    elem_styles = _get_element_computed_styles(element, css_variables)
    bg_color = elem_styles.get("background-color")

    if not bg_color or bg_color == "transparent":
        parent = element.parent
        while parent and (not bg_color or bg_color == "transparent"):
            parent_styles = _get_element_computed_styles(parent, css_variables)
            parent_bg = parent_styles.get("background-color")
            if parent_bg and parent_bg != "transparent":
                bg_color = parent_bg
                break
            parent = parent.parent

    if not bg_color or bg_color == "transparent":
        body = soup.find("body")
        if body:
            body_styles = _get_element_computed_styles(body, css_variables)
            bg_color = body_styles.get("background-color") or default
        else:
            bg_color = default

    return bg_color


# -----------------------------------------------------------------------------
# Helper: Palette Attribute Access
# -----------------------------------------------------------------------------


@dataclass
class PaletteColors:
    """Extracted color values from a palette's CSS attributes."""

    palette_name: str
    font_color: str
    background_color: str
    primary_color: Optional[str] = None
    error_color: Optional[str] = None
    font_size: float = 14.0


def get_palette_colors(
    palette_name: str,
    all_palette_css_attributes: Dict[str, Dict[str, str]],
    required_attrs: Optional[List[str]] = None,
) -> PaletteColors:
    """Extract and validate palette color attributes.

    Args:
        palette_name: Name of the palette
        all_palette_css_attributes: Fixture with all palette attributes
        required_attrs: Additional attributes to require (beyond font/background)

    Returns:
        PaletteColors with extracted values

    Raises:
        AssertionError: If required attributes are missing
    """
    palette_attributes = all_palette_css_attributes.get(palette_name)
    assert palette_attributes is not None, f"No CSS attributes defined for palette: {palette_name}"

    font_color = palette_attributes.get("font-color")
    background_color = palette_attributes.get("background-color")

    assert font_color is not None, f"No font-color defined for palette: {palette_name}"
    assert background_color is not None, f"No background-color defined for palette: {palette_name}"

    # Parse font size
    font_size_str = palette_attributes.get("global-font-size", "14px")
    font_size = float(font_size_str.replace("px", "").strip())

    # Extract optional colors
    primary_color = palette_attributes.get("primary-color")
    error_color = palette_attributes.get("error-color")

    # Validate any additional required attributes
    if required_attrs:
        for attr in required_attrs:
            assert palette_attributes.get(attr) is not None, f"No {attr} defined for palette: {palette_name}"

    return PaletteColors(
        palette_name=palette_name,
        font_color=font_color,
        background_color=background_color,
        primary_color=primary_color,
        error_color=error_color,
        font_size=font_size,
    )


# -----------------------------------------------------------------------------
# Helper: Contrast Validation
# -----------------------------------------------------------------------------


def assert_contrast_meets_wcag_aa(
    fg_color: str,
    bg_color: str,
    font_size: float,
    context: str,
    is_bold: bool = False,
) -> None:
    """Assert that a color combination meets WCAG AA contrast requirements.

    Args:
        fg_color: Foreground (text) color
        bg_color: Background color
        font_size: Font size in pixels
        context: Description for error message (e.g., "Palette 'default': Primary link color")
        is_bold: Whether text is bold

    Raises:
        AssertionError: If contrast ratio doesn't meet WCAG AA
    """
    ratio = get_contrast_ratio(fg_color, bg_color)
    assert ratio is not None, f"Could not calculate contrast ratio for {fg_color} on {bg_color}"

    is_compliant = meets_wcag_aa(ratio, text_size=font_size, is_bold=is_bold)
    required = 3.0 if (font_size >= 24 or (is_bold and font_size >= 18.67)) else 4.5

    assert is_compliant, (
        f"{context} {fg_color} on {bg_color} has contrast {ratio:.2f}:1, "
        f"does not meet WCAG 2.1 AA minimum of {required}:1 for {font_size}px text"
    )


# -----------------------------------------------------------------------------
# Helper: Color Combination Tracking
# -----------------------------------------------------------------------------


@dataclass
class ColorCombination:
    """Tracks occurrences of a foreground/background color pair."""

    fg_color: str
    bg_color: str
    count: int = 0
    locations: List[str] = field(default_factory=list)
    element_types: Set[str] = field(default_factory=set)

    def add_occurrence(self, location: str, element_type: Optional[str] = None) -> None:
        """Record an occurrence of this color combination."""
        self.count += 1
        self.locations.append(location)
        if element_type:
            self.element_types.add(element_type)


class ColorCombinationTracker:
    """Tracks unique color combinations found during site scanning."""

    def __init__(self):
        self._combinations: Dict[Tuple[str, str], ColorCombination] = {}

    def add(
        self,
        fg_color: str,
        bg_color: str,
        location: str,
        element_type: Optional[str] = None,
    ) -> None:
        """Add an occurrence of a color combination."""
        key = (fg_color.lower(), bg_color.lower())
        if key not in self._combinations:
            self._combinations[key] = ColorCombination(fg_color=fg_color.lower(), bg_color=bg_color.lower())
        self._combinations[key].add_occurrence(location, element_type)

    def get_failures(self, min_ratio: float = 4.5) -> List[str]:
        """Get list of failure messages for combinations below threshold."""
        failures = []
        for combo in self._combinations.values():
            ratio = get_contrast_ratio(combo.fg_color, combo.bg_color)
            if ratio and ratio < min_ratio:
                locations_preview = ", ".join(combo.locations[:3])
                if len(combo.locations) > 3:
                    locations_preview += f" (+{len(combo.locations) - 3} more)"

                msg = f"Color {combo.fg_color} on {combo.bg_color} = {ratio:.2f}:1 (need {min_ratio}:1)"
                if combo.element_types:
                    msg += f" - Elements: {', '.join(sorted(combo.element_types))}"
                msg += f" - Found {combo.count} times"
                if locations_preview:
                    msg += f" - Examples: {locations_preview}"
                failures.append(msg)
        return failures


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
        site_path = get_site_path(built_example_site_with_palette)

        all_violations = []
        for ctx in iter_site_html_files(site_path):
            violations = validate_color_contrast(
                ctx.html_content,
                filename=ctx.relative_path,
                css_content=ctx.css_content,
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
        site_path = get_site_path(built_example_site_with_palette)
        tracker = ColorCombinationTracker()

        for ctx in iter_site_html_files(site_path):
            for link in ctx.soup.find_all("a"):
                link_text = link.get_text(strip=True)[:40]
                if not link_text:
                    continue

                link_styles = _get_element_computed_styles(link, ctx.css_variables)
                link_color = link_styles.get("color")
                if not link_color:
                    continue

                link_bg = resolve_background_color(link, ctx.css_variables, ctx.soup)

                if link_color and link_bg:
                    tracker.add(link_color, link_bg, f"{ctx.relative_path}: {link_text[:30]}")

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
        site_path = get_site_path(built_example_site_with_palette)
        tracker = ColorCombinationTracker()

        text_tags = ["p", "span", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "td", "th"]

        for ctx in iter_site_html_files(site_path):
            for elem in ctx.soup.find_all(text_tags):
                if not elem.get_text(strip=True):
                    continue

                elem_styles = _get_element_computed_styles(elem, ctx.css_variables)
                elem_color = elem_styles.get("color")
                if not elem_color:
                    continue

                elem_bg = resolve_background_color(elem, ctx.css_variables, ctx.soup)

                if elem_color and elem_bg:
                    tracker.add(elem_color, elem_bg, f"{ctx.relative_path}:{elem.name}", elem.name)

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
        site_path = get_site_path(built_example_site_with_palette)

        all_violations = []
        for ctx in iter_site_html_files(site_path):
            violations = validate_color_contrast(
                ctx.html_content,
                filename=ctx.relative_path,
                css_content=ctx.css_content,
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
        site_path = get_site_path(built_example_site_with_palette)

        html_file = site_path / "index.html"
        assert html_file.exists(), f"HTML file not found at {html_file}"

        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        css_content = load_css_from_site(site_path, html_content)
        assert len(css_content) > 0, "No CSS content loaded from site"

        css_variables = _extract_css_variables(html_content, css_content)
        assert len(css_variables) > 0, "No CSS variables extracted"

        # Determine palette from site path
        palette_name = None
        for palette in sorted(DEFAULT_PALETTES, key=len, reverse=True):
            if f"_{palette}_site" in str(site_path):
                palette_name = palette
                break

        assert palette_name is not None, f"Could not determine palette from site path: {site_path}"

        assert css_variables.get("--font-color") is not None, (
            f"Palette '{palette_name}': CSS variable --font-color not found"
        )
        assert css_variables.get("--background-color") is not None, (
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
        site_path = get_site_path(built_example_site_with_palette)
        contrast_failures = []

        for ctx in iter_site_html_files(site_path):
            for link_index, link in enumerate(ctx.soup.find_all("a")):
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
                            f"{ctx.relative_path} (link {link_index}): '{link_text}' "
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
        site_path = get_site_path(built_example_site_with_palette)

        alert_trackers = {
            "error": ColorCombinationTracker(),
            "primary": ColorCombinationTracker(),
        }

        for ctx in iter_site_html_files(site_path):
            for alert_type, class_name in [
                ("error", "terminal-alert-error"),
                ("primary", "terminal-alert-primary"),
            ]:
                for elem_idx, elem in enumerate(ctx.soup.find_all(class_=class_name)):
                    elem_styles = _get_element_computed_styles(elem, ctx.css_variables)
                    alert_color = elem_styles.get("color")
                    if not alert_color:
                        continue

                    alert_bg = resolve_background_color(elem, ctx.css_variables, ctx.soup)

                    if alert_color and alert_bg:
                        location = f"{ctx.relative_path}:{alert_type} #{elem_idx}"
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



