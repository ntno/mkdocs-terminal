from tidylib import tidy_fragment


def check_html(fragment):
    result = {}
    document, errors = tidy_fragment(fragment, options={'numeric-entities': 1})
    result['errors'] = errors
    result['document'] = document
    return result


def assert_valid_html(html):
    assert len(check_html(html)["errors"]) == 0


def assert_tile_has_terminal_marker(html):
    assert "class=\"terminal-mkdocs-tile " in html


def tile_has_anchor(html):
    return "<a " in html and "</a>" in html


def tile_has_img(html):
    return "<img " in html


def assert_tile_has_anchor(html):
    assert tile_has_anchor(html)


def assert_tile_has_img(html):
    assert tile_has_img(html)
