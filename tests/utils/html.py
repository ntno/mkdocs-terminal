from tidylib import tidy_fragment
import pytest
DEBUG = False
VERBOSE = False


def check_html(fragment):
    result = {}
    document, errors = tidy_fragment(fragment, options={'numeric-entities': 1})
    result['errors'] = errors
    result['document'] = document
    return result


def strip_internal_whitespace(fragment):
    return ' '.join(fragment.split())


def strip_leading_whitespace(fragment):
    return fragment.strip()


def strip_whitespace(fragment):
    return strip_leading_whitespace(strip_internal_whitespace(fragment))


def assert_valid_html(fragment):
    results = check_html(fragment)
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
