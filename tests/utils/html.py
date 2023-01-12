from tidylib import tidy_fragment


def check_html(fragment):
    result = {}
    document, errors = tidy_fragment(fragment, options={'numeric-entities': 1})
    result['errors'] = errors
    result['document'] = document
    return result


def strip_html(fragment):
    return ' '.join(fragment.split())


def print_trimmed_html(fragment):
    print(strip_html(fragment))


def assert_valid_html(fragment):
    stripped_html = strip_html(fragment)
    # if (check_html(stripped_html)["errors"]):
    #     print(check_html(stripped_html)["errors"])
    assert check_html(stripped_html)["errors"] == ""


def assert_tile_has_terminal_marker(html):
    assert "class=\"terminal-mkdocs-tile " in html


def tile_has_anchor(html):
    return "<a " in html and "</a>" in html


def tile_has_img(html):
    return "<img " in html
