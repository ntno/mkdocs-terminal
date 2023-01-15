from tests.utils import theme_plugins
import pytest


@pytest.fixture
def top_nav_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/top-nav.html")


@pytest.fixture
def enabled_context():
    return {
        "nav": [],
        "config": {
            "site_name": "site_name_placeholder",
            "site_url": "site_url_placeholder",
            "plugins": [theme_plugins.SEARCH]
        }
    }


class TestTopNav():
    @pytest.mark.parametrize("plugins_list", [
        pytest.param(
            None, id="null_plugins_list"
        ),
        pytest.param(
            [], id="empty_plugins_list"
        )
    ])
    def test_no_search_button_when_search_plugin_disabled(self, top_nav_partial, enabled_context, plugins_list):
        enabled_context["plugins"] = plugins_list
        context_data = enabled_context
        rendered_nav = top_nav_partial.render(context_data)
        assert "#mkdocs_search_modal" not in rendered_nav

    def test_search_button_included_when_search_plugin_enabled(self, top_nav_partial, enabled_context):
        context_data = enabled_context
        rendered_nav = top_nav_partial.render(context_data)
        assert "#mkdocs_search_modal" in rendered_nav

    # def test_revision_renders_when_plugin_enabled(self, top_nav_partial):
    #     context_data = {
    #         "config": {
    #             "plugins": [theme_plugins.REVISION],
    #             "theme": {}
    #         }
    #     }
    #     try:
    #         top_nav_partial.render(context_data)
    #     except Exception as ex:
    #         pytest.fail(f"Got exception during render: {ex})")
