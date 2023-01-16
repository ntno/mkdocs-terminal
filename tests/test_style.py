from tests.utils.html import assert_valid_html
from tests.interface import theme_features
from tests.utils.filters import MOCK_URL_PATH_PREFIX
import pytest


@pytest.fixture
def styles_partial(env_with_terminal_loader_and_mocked_url_filter):
    return env_with_terminal_loader_and_mocked_url_filter.get_template("partials/styles.html")


@pytest.fixture
def enabled_context():
    return {
        "config": {
            "theme": {
                "features": []
            }
        }
    }


class TestStyles():
    def test_that_default_palette_included_by_default(self, styles_partial, enabled_context):
        expected_css_path = MOCK_URL_PATH_PREFIX + "css/palettes/default.css"
        rendered_styles = styles_partial.render(enabled_context)
        assert expected_css_path in rendered_styles
        assert_valid_html(rendered_styles)

    @pytest.mark.parametrize("palette_option", [
        pytest.param(
            "dark", id="dark_palette_option"
        ),
        pytest.param(
            "default", id="default_palette_option"
        ),
        pytest.param(
            "gruvbox_dark", id="gruvbox_dark_palette_option"
        ),
        pytest.param(
            "pink", id="pink_palette_option"
        ),
        pytest.param(
            "sans_dark", id="sans_dark_palette_option"
        ),
        pytest.param(
            "sans", id="sans_palette_option"
        )
    ])
    def test_that_alternate_palette_can_be_specified_in_theme_config(self, palette_option, styles_partial, enabled_context):
        enabled_context["config"]["theme"][theme_features.PALETTE_OPTION] = palette_option
        context_data = enabled_context
        expected_css_path = MOCK_URL_PATH_PREFIX + "css/palettes/" + palette_option + ".css"
        rendered_styles = styles_partial.render(context_data)
        assert expected_css_path in rendered_styles
        assert_valid_html(rendered_styles)

    def test_that_override_css_added_when_cursor_is_hidden(self, styles_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_TOP_CURSOR_ANIMATION]
        context_data = enabled_context
        rendered_styles = styles_partial.render(context_data)
        assert "terminal-prompt::after" in rendered_styles
        assert_valid_html(rendered_styles)