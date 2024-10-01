from tests.utils.html import assert_valid_html
from tests.interface import theme_features, theme_plugins
from unittest.mock import MagicMock, PropertyMock
import pytest
PREV_URL = "prev_page_title_placeholder"
PREV_TITLE = "prev_page_url_placeholder"
NEXT_URL = "next_page_url_placeholder"
NEXT_TITLE = "next_page_title_placeholder"
PREV_NEXT_DIVIDER = "|"
EXPECTED_PREV_LINK = "<a href=\"%s%s\" title=\"%s\">%s</a>" % ("mocked_url_path/", PREV_URL, PREV_TITLE, "Previous")
EXPECTED_NEXT_LINK = "<a href=\"%s%s\" title=\"%s\">%s</a>" % ("mocked_url_path/", NEXT_URL, NEXT_TITLE, "Next")


@pytest.fixture
def footer_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/footer.html")


def make_mock_page_properties(previous_page_value, next_page_value, title_value, url_value):
    properties = {}
    properties["previous_page"] = PropertyMock(return_value=previous_page_value)
    properties["next_page"] = PropertyMock(return_value=next_page_value)
    properties["title"] = PropertyMock(return_value=title_value)
    properties["url"] = PropertyMock(return_value=url_value)
    return properties


def make_mock_page_object(mock_properties):
    page_object = MagicMock()
    type(page_object).previous_page = mock_properties["previous_page"]
    type(page_object).next_page = mock_properties["next_page"]
    type(page_object).title = mock_properties["title"]
    type(page_object).url = mock_properties["url"]
    return page_object


@pytest.fixture
def mock_next_page():
    properties_of_next = make_mock_page_properties(None, None, NEXT_TITLE, NEXT_URL)
    mock = make_mock_page_object(properties_of_next)
    return mock


@pytest.fixture
def mock_prev_page():
    properties_of_previous = make_mock_page_properties(None, None, PREV_TITLE, PREV_URL)
    mock = make_mock_page_object(properties_of_previous)
    return mock


@pytest.fixture
def enabled_context(mock_prev_page, mock_next_page):
    next_page = mock_next_page
    prev_page = mock_prev_page
    return {
        "page": {
            "title": "current_page_title_placeholder",
            "url": "current_page_url_placeholder",
            "next_page": next_page,
            "previous_page": prev_page
        },
        "config": {
            "repo_name": "GitHub",
            "repo_url": "repo_url_placeholder",
            "plugins": [theme_plugins.REVISION],
            "theme": {
                "features": [theme_features.FOOTER_PREV_NEXT, theme_features.SHOW_REVISION_DATE, theme_features.SHOW_REVISION_HISTORY]
            }
        }
    }


class TestFooter():

    def test_no_prev_next_when_feature_disabled(self, footer_partial, enabled_context):
        context_data = enabled_context
        context_data["config"]["theme"]["features"] = []
        rendered_footer = footer_partial.render(context_data)
        expected_div_id = "id=\"terminal-mkdocs-footer-prev-next\""
        assert expected_div_id not in rendered_footer
        assert EXPECTED_PREV_LINK not in rendered_footer
        assert PREV_NEXT_DIVIDER not in rendered_footer
        assert EXPECTED_NEXT_LINK not in rendered_footer
        assert_valid_html(rendered_footer)

    def test_no_prev_when_none_available(self, footer_partial, enabled_context):
        context_data = enabled_context
        del context_data["page"]["previous_page"]
        rendered_footer = footer_partial.render(context_data)
        expected_div_id = "id=\"terminal-mkdocs-footer-prev-next\""
        assert expected_div_id in rendered_footer
        assert EXPECTED_PREV_LINK not in rendered_footer
        assert PREV_NEXT_DIVIDER not in rendered_footer
        assert EXPECTED_NEXT_LINK in rendered_footer
        assert_valid_html(rendered_footer)

    def test_no_next_when_none_available(self, footer_partial, enabled_context):
        context_data = enabled_context
        del context_data["page"]["next_page"]
        rendered_footer = footer_partial.render(context_data)
        expected_div_id = "id=\"terminal-mkdocs-footer-prev-next\""
        assert expected_div_id in rendered_footer
        assert EXPECTED_PREV_LINK in rendered_footer
        assert PREV_NEXT_DIVIDER not in rendered_footer
        assert EXPECTED_NEXT_LINK not in rendered_footer
        assert_valid_html(rendered_footer)

    def test_prev_and_next_when_available(self, footer_partial, enabled_context):
        context_data = enabled_context
        rendered_footer = footer_partial.render(context_data)
        expected_div_id = "id=\"terminal-mkdocs-footer-prev-next\""
        assert expected_div_id in rendered_footer
        assert EXPECTED_PREV_LINK in rendered_footer
        assert PREV_NEXT_DIVIDER in rendered_footer
        assert EXPECTED_NEXT_LINK in rendered_footer
        assert_valid_html(rendered_footer)

    def test_footer_renders_when_single_page(self, footer_partial, enabled_context):
        context_data = enabled_context
        del context_data["page"]["previous_page"]
        del context_data["page"]["next_page"]
        rendered_footer = footer_partial.render(context_data)
        expected_div_id = "id=\"terminal-mkdocs-footer-prev-next\""
        assert expected_div_id not in rendered_footer
        assert EXPECTED_PREV_LINK not in rendered_footer
        assert PREV_NEXT_DIVIDER not in rendered_footer
        assert EXPECTED_NEXT_LINK not in rendered_footer
        assert_valid_html(rendered_footer)
