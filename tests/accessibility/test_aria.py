import pytest
from bs4 import BeautifulSoup
from tests.accessibility.validators import (
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

    @pytest.mark.parametrize("built_example_site", ["search-enabled"], indirect=True)
    def test_buttons_have_text_or_aria_label(self, built_example_site):
        """Verify all buttons across built site have accessible names.

        This test scans all HTML files and ensures:
        1. At least one button was found (test is configured correctly)
        2. All buttons have either text content or aria-label
        """
        html_files = list(built_example_site.glob("**/*.html"))
        assert html_files, "No HTML files found in built simple site"

        all_violations = []
        buttons_found = []

        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")
            buttons = soup.find_all("button")

            if buttons:
                buttons_found.extend(buttons)

            aria_violations = validate_aria_buttons(html, html_file.name)
            all_violations.extend(aria_violations)

        # Verify test configuration: we should have found at least one button
        # (e.g., close button in search modal)
        assert buttons_found, (
            "No <button> elements found in built site. "
            "Test configuration error: expected at least one button "
            "(e.g., search modal close button). "
            "Check that example site contains interactive elements."
        )

        # Verify all buttons have accessible names
        assert not all_violations, "Buttons missing text or aria-label:\n" + "\n".join(all_violations)


class TestARIAAttributes:
    """Tests for aria-hidden and other ARIA attributes.

    Requirement: aria-hidden should only be used on decorative elements.
    Icon buttons should use aria-label for accessible naming.
    """

    @pytest.mark.parametrize("built_example_site", ["search-enabled"], indirect=True)
    def test_aria_hidden_only_on_decorative(self, built_example_site):
        """Verify aria-hidden='true' only appears on genuinely decorative elements.

        This test ensures:
        1. Test found aria-hidden elements to validate (test configured correctly)
        2. Any aria-hidden elements have no text content (truly decorative)

        Note: After refactoring close button to use aria-label instead of aria-hidden+sr-only,
        aria-hidden elements should only appear on truly decorative content.
        """
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        aria_hidden_found = False

        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")

            # Check if this file has aria-hidden elements
            if soup.find_all(attrs={"aria-hidden": "true"}):
                aria_hidden_found = True

            violations = validate_aria_hidden(html, html_file.name)
            all_violations.extend(violations)

        # Verify test configuration: aria-hidden elements should exist somewhere
        # in the theme (even if just for decorative purposes)
        assert aria_hidden_found, (
            "No elements with aria-hidden='true' found in built site. "
            "Test configuration error: aria-hidden is expected to be used in the theme "
            "(e.g., on decorative icons, visual separators, or other non-semantic elements). "
            "Check that example site is built correctly and theme templates are present."
        )

        # Verify all aria-hidden usage is correct (only on decorative elements)
        assert not all_violations, "aria-hidden used incorrectly:\n" + "\n".join(all_violations)


class TestModalAccessibility:
    """Tests for search modal ARIA attributes.

    Requirement: Modal dialogs must have proper ARIA attributes per
    WCAG dialog pattern: role, aria-modal, aria-labelledby.
    """

    @pytest.mark.parametrize("built_example_site", ["search-enabled"], indirect=True)
    def test_modal_has_correct_aria_attributes(self, built_example_site):
        """Verify search modal has required ARIA attributes for accessibility.

        This test ensures:
        1. Modal element exists in the site (test configured correctly)
        2. Modal has all required ARIA attributes for screen reader users
        """
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        modal_found = False

        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")

            # Check if this file contains the search modal
            if soup.find(id="mkdocs_search_modal"):
                modal_found = True

            violations = validate_modal_accessibility(html, html_file.name)
            all_violations.extend(violations)

        # Verify test configuration: modal should exist in the site
        assert modal_found, (
            "Search modal (id='mkdocs_search_modal') not found in built site. "
            "Test configuration error: expected modal to be present. "
            "Check that the search plugin is enabled in the site config."
        )

        # Verify modal has correct ARIA attributes
        assert not all_violations, (
            "Modal accessibility violations found:\n" + "\n".join(all_violations)
        )


class TestFormAccessibility:
    """Tests for form input labeling.

    Requirement: All form inputs must have associated labels so screen reader
    users know what each input is for.
    """

    @pytest.mark.parametrize("built_example_site", ["search-enabled"], indirect=True)
    def test_form_inputs_have_labels(self, built_example_site):
        """Verify all form inputs have associated labels or aria-label.

        This test ensures:
        1. Form inputs exist in the site (test configured correctly)
        2. All inputs have accessible names via label, aria-label, or aria-labelledby
        """
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        form_inputs_found = []

        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")

            # Find all form inputs (excluding submit buttons, etc)
            inputs = soup.find_all(["input", "textarea", "select"])
            for inp in inputs:
                input_type = inp.get("type", "text").lower()
                if input_type not in ("hidden", "submit", "button", "reset", "image"):
                    form_inputs_found.append(inp)

            violations = validate_form_labels(html, html_file.name)
            all_violations.extend(violations)

        # Verify test configuration: at least one form input should exist
        # (e.g., search input in modal)
        assert form_inputs_found, (
            "No form inputs found in built site. "
            "Test configuration error: at least one form input is expected "
            "(e.g., search input in the modal). "
            "Check that the search plugin is enabled in the site config."
        )

        # Verify all form inputs have accessible labels
        assert not all_violations, (
            "Form input labeling violations found:\n" + "\n".join(all_violations)
        )


class TestLinkAccessibility:
    """Tests for link text clarity.

    Requirement: Links in theme regions (nav, header, footer) must have
    descriptive text or aria-label. Avoids generic link text.
    """

    @pytest.mark.parametrize("built_example_site", ["search-enabled"], indirect=True)
    def test_theme_links_have_text_or_aria_label(self, built_example_site):
        """Verify theme region links have descriptive text or aria-label.

        This test ensures:
        1. Theme region links exist in the site (test configured correctly)
        2. All links in nav/header/footer have descriptive text or aria-label

        Tested regions: nav, header, footer, aside
        """
        html_files = list(built_example_site.glob("**/*.html"))
        all_violations = []
        links_by_region = {"nav": [], "header": [], "footer": [], "aside": []}

        for html_file in html_files:
            html = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")

            # Find links in each theme region separately for visibility
            for region_name in ["nav", "header", "footer", "aside"]:
                regions = soup.find_all(region_name)
                for region in regions:
                    links = region.find_all("a")
                    links_by_region[region_name].extend(links)

            violations = validate_link_text(html, html_file.name)
            all_violations.extend(violations)

        # Verify test configuration: links should exist in key theme regions
        # At minimum, nav elements should not be empty (semantic requirement)
        for nav in soup.find_all("nav"):
            assert nav.find("a"), (
                "Empty <nav> element found with no links. "
                "Navigation elements must contain navigation content (links). "
                "Empty nav elements are semantically incorrect and should be removed."
            )

        nav_links = links_by_region["nav"]
        assert nav_links, (
            "No links found in <nav> regions. "
            "Test configuration error: navigation links are expected in the theme. "
            "Check that example site has navigation structure."
        )

        # Also verify overall link presence across all regions
        all_theme_links = sum(len(links) for links in links_by_region.values())
        assert all_theme_links > 0, (
            "No theme region links found in any region (nav, header, footer, aside). "
            "Test configuration error: at least navigation links are expected. "
            "Check that theme templates have proper structure."
        )

        # Verify all theme region links have descriptive text
        assert not all_violations, (
            "Link accessibility violations found:\n" + "\n".join(all_violations)
        )
