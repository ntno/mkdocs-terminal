from tidylib import tidy_fragment
import pytest
DEBUG = False
VERBOSE = False
DEFAULT_TIDY_OPTIONS = {"numeric-entities": 1}
ALLOW_EMPTY_ELEMENTS = {"numeric-entities": 1, "drop-empty-elements": "no"}


def check_html(fragment, tidy_options=DEFAULT_TIDY_OPTIONS):
    result = {}
    document, errors = tidy_fragment(fragment, options=tidy_options)
    result['errors'] = errors
    result['document'] = document
    return result


def strip_internal_whitespace(fragment):
    return ' '.join(fragment.split())


def strip_leading_whitespace(fragment):
    return fragment.strip()


def strip_whitespace(fragment):
    return strip_leading_whitespace(strip_internal_whitespace(fragment))


def assert_valid_html(fragment, tidy_options={"numeric-entities": 1}):
    results = check_html(fragment, tidy_options)
    if (DEBUG):
        stripped_html = strip_leading_whitespace(fragment)
        print("\n---")
        print("fragment: ")
        if (VERBOSE):
            print(fragment)
        else:
            print(stripped_html)
        print("errors: " + results["errors"])
        print("\n---")
    if (results["errors"] != ""):
        pytest.fail("Invalid HTML: \n" + results["errors"])


def assert_tile_has_terminal_marker(html):
    assert "class=\"terminal-mkdocs-tile " in html


def tile_has_anchor(html):
    return "<a " in html and "</a>" in html


def tile_has_img(html):
    return "<img " in html
