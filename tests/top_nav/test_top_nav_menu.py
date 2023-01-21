from tests.utils.html import assert_valid_html
from tests.interface import theme_plugins
import pytest


@pytest.fixture
def enabled_context():
    nav_list = []
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
    @pytest.mark.skip(reason="implementation TODO")
    def test_no_page_links_when_nav_empty(self, menu_partial, enabled_context):
        pass

    @pytest.mark.skip(reason="implementation TODO")
    def test_all_top_level_pages_included(self, menu_partial, enabled_context):
        pass

    def test_search_button_when_search_plugin_enabled(self, menu_partial, enabled_context):
        context_data = enabled_context
        rendered_nav = menu_partial.render(context_data)
        assert "#mkdocs_search_modal" in rendered_nav
        assert_valid_html(rendered_nav)

    @pytest.mark.parametrize("plugins_list", [
        pytest.param(
            None, id="null_plugins_list"
        ),
        pytest.param(
            [], id="empty_plugins_list"
        )
    ])
    def test_no_search_button_when_search_plugin_disabled(self, menu_partial, enabled_context, plugins_list):
        enabled_context["plugins"] = plugins_list
        context_data = enabled_context
        rendered_nav = menu_partial.render(context_data)
        assert "#mkdocs_search_modal" not in rendered_nav
        assert_valid_html(rendered_nav)
