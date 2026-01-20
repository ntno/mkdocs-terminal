import pytest
from bs4 import BeautifulSoup
from tests.accessibility.utils import validate_aria_buttons, validate_aria_hidden


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
    button_found = False
    for html_file in html_files:
        html = html_file.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        if soup.find("button"):
            button_found = True

        aria_violations = validate_aria_buttons(html, html_file.name)
        all_violations.extend(aria_violations)

    if not button_found:
        pytest.fail("No <button> elements found in built site. This likely indicates a test misconfiguration or missing modal. At least one button is expected (e.g., in the search modal).")

    assert not all_violations, f"Buttons missing text or aria-label: {all_violations}"


@pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
def test_aria_hidden_only_on_decorative(index_html):
    html, filename = index_html
    soup = BeautifulSoup(html, "html.parser")
    hidden_elements = soup.find_all(attrs={"aria-hidden": "true"})
    if not hidden_elements:
        pytest.fail("No elements with aria-hidden='true' found in built site. This likely indicates a test misconfiguration or missing modal. At least one such element is expected (e.g., in the search modal).")
    violations = validate_aria_hidden(html, filename)
    assert not violations, f"aria-hidden used on non-decorative elements: {violations}"
