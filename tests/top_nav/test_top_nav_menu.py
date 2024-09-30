from tests.utils.html_utils import assert_valid_html, ALLOW_EMPTY_ELEMENTS
from tests.interface import theme_plugins
import pytest


@pytest.fixture
def enabled_context(inactive_page_1, inactive_page_2):
    nav_list = [inactive_page_1, inactive_page_2]
    return {
        "nav": nav_list,
        "config": {
            "site_name": "site_name_placeholder",
            "site_url": "site_url_placeholder",
            "plugins": [theme_plugins.SEARCH],
            "theme": {
                "features": []
            }
        },
        "button_idx": len(nav_list)
    }


@pytest.fixture
def menu_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/top-nav/menu.html")


class TestTopNavMenu():

    def test_no_page_links_when_nav_empty(self, menu_partial, enabled_context):
        enabled_context["nav"] = []
        context_data = enabled_context
        rendered_nav = menu_partial.render(context_data)
        assert_valid_html(rendered_nav, ALLOW_EMPTY_ELEMENTS)
        assert "WebPage" not in rendered_nav

    def test_all_top_level_pages_included(self, menu_partial, enabled_context, inactive_page_1_properties, inactive_page_2_properties):
        context_data = enabled_context
        rendered_nav = menu_partial.render(context_data)
        inactive_page_1_properties["title"].assert_called_once()
        inactive_page_2_properties["title"].assert_called_once()
        assert_valid_html(rendered_nav, ALLOW_EMPTY_ELEMENTS)
        assert "title_1" in rendered_nav
        assert "title_2" in rendered_nav

    def test_search_button_when_search_plugin_enabled(self, menu_partial, enabled_context):
        context_data = enabled_context
        rendered_nav = menu_partial.render(context_data)
        assert "#mkdocs_search_modal" in rendered_nav
        assert_valid_html(rendered_nav, ALLOW_EMPTY_ELEMENTS)

    @pytest.mark.parametrize("plugins_list", [
        pytest.param(
            None, id="null_plugins_list"
        ),
        pytest.param(
            [], id="empty_plugins_list"
        )
    ])
    def test_no_search_button_when_search_plugin_disabled(self, menu_partial, enabled_context, plugins_list):
        enabled_context["config"]["plugins"] = plugins_list
        context_data = enabled_context
        rendered_nav = menu_partial.render(context_data)
        assert "#mkdocs_search_modal" not in rendered_nav
        assert_valid_html(rendered_nav, ALLOW_EMPTY_ELEMENTS)
