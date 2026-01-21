import pytest
from bs4 import BeautifulSoup
from tests.accessibility.utils import (
    validate_aria_buttons,
    validate_aria_hidden,
    validate_modal_accessibility,
    validate_form_labels,
    validate_link_text,
)


@pytest.fixture
def index_html(built_example_site):
    index_file = built_example_site / "index.html"
    return index_file.read_text(encoding="utf-8"), index_file.name


class TestARIAButtons:
    """Tests for button ARIA attributes.

    Requirement: Buttons must have text content or aria-label so screen readers
    can announce their purpose.
    """

    @pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
    def test_buttons_have_text_or_aria_label(self, built_example_site):
        """Verify all buttons across built site have accessible names."""
        html_files = list(built_example_site.glob("**/*.html"))
        assert html_files, "No HTML files found in built simple site"

        all_violations = []
        button_found = False
        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")
            if soup.find("button"):
                button_found = True

            aria_violations = validate_aria_buttons(html, html_file.name)
            all_violations.extend(aria_violations)

        if not button_found:
            pytest.fail(
                "No <button> elements found in built site. "
                "At least one button is expected (e.g., in the search modal)."
            )

        assert not all_violations, f"Buttons missing text or aria-label:\n" + "\n".join(all_violations)


class TestARIAAttributes:
    """Tests for aria-hidden and other ARIA attributes.

    Requirement: aria-hidden should only be used on decorative elements.
    Screen readers use aria-label for accessible naming of icon buttons.
    """

    @pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
    def test_aria_hidden_only_on_decorative(self, index_html):
        """Verify aria-hidden='true' only appears on decorative elements (no text)."""
        html, filename = index_html
        violations = validate_aria_hidden(html, filename)
        assert not violations, f"aria-hidden used on non-decorative elements:\n" + "\n".join(violations)


class TestModalAccessibility:
    """Tests for search modal ARIA attributes.

    Requirement: Modal dialogs must have proper ARIA attributes per
    WCAG dialog pattern: role, aria-modal, aria-labelledby.
    """

    @pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
    def test_modal_has_correct_aria_attributes(self, built_example_site):
        """Verify search modal has required ARIA attributes for accessibility."""
        # Build site and check all HTML files for modal accessibility
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        
        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            violations = validate_modal_accessibility(html, html_file.name)
            all_violations.extend(violations)

        assert not all_violations, (
            "Modal accessibility violations found:\n" + "\n".join(all_violations)
        )


class TestFormAccessibility:
    """Tests for form input labeling.

    Requirement: All form inputs must have associated labels so screen reader
    users know what each input is for.
    """

    @pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
    def test_form_inputs_have_labels(self, built_example_site):
        """Verify all form inputs have associated labels."""
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        
        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            violations = validate_form_labels(html, html_file.name)
            all_violations.extend(violations)

        assert not all_violations, (
            "Form input labeling violations found:\n" + "\n".join(all_violations)
        )


class TestLinkAccessibility:
    """Tests for link text clarity.

    Requirement: Links in theme regions (nav, header, footer) must have
    descriptive text or aria-label. Avoids generic link text.
    """

    @pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
    def test_theme_links_have_text_or_aria_label(self, built_example_site):
        """Verify theme region links have descriptive text or aria-label."""
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        
        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            violations = validate_link_text(html, html_file.name)
            all_violations.extend(violations)

        assert not all_violations, (
            "Link accessibility violations found:\n" + "\n".join(all_violations)
        )

