from tests.utils import theme_plugins
from jinja2 import Template, pass_context
import pytest


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


class TestTopNavMenu():
    def test_pass_context_callable_class(self, env):
        class CallableClass:
            @pass_context
            def __call__(self, ctx):
                return ctx.resolve("hello")

        tpl = Template("""{{ callableclass() }}""")
        output = tpl.render(callableclass=CallableClass(), hello="TEST")
        expected = "TEST"

        assert output == expected

    @pytest.mark.parametrize("plugins_list", [
        pytest.param(
            None, id="null_plugins_list"
        ),
        pytest.param(
            [], id="empty_plugins_list"
        )
    ])
    def test_no_search_button_when_search_plugin_disabled(self, top_menu_partial, enabled_context, plugins_list):
        enabled_context["plugins"] = plugins_list
        context_data = enabled_context
        rendered_nav = top_menu_partial.render(context_data)
        assert "#mkdocs_search_modal" not in rendered_nav
