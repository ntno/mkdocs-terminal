import pytest
from bs4 import BeautifulSoup
from tests.accessibility.utils import validate_aria


@pytest.fixture
def index_html(built_example_site):
    index_file = built_example_site / "index.html"
    return index_file.read_text(encoding="utf-8"), index_file.name


@pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
def test_buttons_have_text_or_aria_label(built_example_site):
    """
    Scan all HTML files in the built simple site for button accessibility violations.
    This ensures modals and all pages are checked, not just index.html.
    """
    html_files = list(built_example_site.glob("**/*.html"))
    assert html_files, "No HTML files found in built simple site"

    all_violations = []
    for html_file in html_files:
        html = html_file.read_text(encoding="utf-8")
        violations = [v for v in validate_aria(html, html_file.name) if "Button missing text content or aria-label" in v]
        all_violations.extend(violations)

    assert not all_violations, f"Buttons missing text or aria-label: {all_violations}"


def test_aria_hidden_only_on_decorative(index_html):
    html, filename = index_html
    violations = [v for v in validate_aria(html, filename) if "aria-hidden='true' contains content" in v]
    assert not violations, f"aria-hidden used on non-decorative elements: {violations}"
