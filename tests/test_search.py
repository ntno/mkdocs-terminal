from tests.utils import theme_plugins, theme_features
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
def search_button_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/top/search-button.html")


class TestSearchButton():
    @pytest.mark.parametrize("plugins_list", [
        pytest.param(
            None, id="null_plugins_list"
        ),
        pytest.param(
            [], id="empty_plugins_list"
        )
    ])
    def test_no_search_button_when_search_plugin_disabled(self, search_button_partial, enabled_context, plugins_list):
        enabled_context["config"]["plugins"] = plugins_list
        context_data = enabled_context
        rendered_nav = search_button_partial.render(context_data)
        assert rendered_nav == ""


    def test_search_button_included_when_search_plugin_enabled(self, search_button_partial, enabled_context):
        context_data = enabled_context
        rendered_nav = search_button_partial.render(context_data)
        assert "#mkdocs_search_modal" in rendered_nav

    def test_search_button_not_included_when_feature_disabled(self, search_button_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_SEARCH_BUTTON]
        context_data = enabled_context
        rendered_nav = search_button_partial.render(context_data)
        assert rendered_nav == ""