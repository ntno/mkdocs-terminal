from pathlib import Path
from tests.utils.html import assert_valid_html
from tests.interface import theme_features
from tests.utils.filters import MOCK_URL_PATH_PREFIX
import pytest


@pytest.fixture
def styles_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/styles.html")


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
        assert "#mkdocs-terminal-site-name.terminal-prompt::after" in rendered_styles
        assert_valid_html(rendered_styles)

    def test_that_override_css_added_when_link_underline_is_hidden(self, styles_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_LINK_UNDERLINE]
        context_data = enabled_context
        rendered_styles = styles_partial.render(context_data)
        assert "#terminal-mkdocs-main-content a:not(.headerlink)" in rendered_styles
        assert_valid_html(rendered_styles)

    def test_that_main_grid_has_two_columns_by_default(self, styles_partial, enabled_context):
        rendered_styles = styles_partial.render(enabled_context)
        assert "grid-template-columns: auto;" in rendered_styles
        assert "grid-template-columns: 4fr 9fr;" in rendered_styles
        assert_valid_html(rendered_styles)

    def test_that_main_grid_is_one_column_when_side_nav_is_hidden(self, styles_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_SIDE_NAV]
        context_data = enabled_context
        rendered_styles = styles_partial.render(context_data)
        assert "grid-template-columns: auto;" in rendered_styles
        assert "grid-template-columns: 4fr 9fr;" not in rendered_styles
        assert_valid_html(rendered_styles)

    def test_palette_css_files_registered_in_default_palettes(self):
        """Ensure every CSS palette file is represented in DEFAULT_PALETTES."""
        repo_root = Path(__file__).resolve().parent.parent
        palettes_dir = repo_root / "terminal" / "css" / "palettes"
        assert palettes_dir.is_dir(), f"Missing palettes directory: {palettes_dir}"

        palette_files = sorted(p.stem for p in palettes_dir.glob("*.css"))
        missing = [palette for palette in palette_files if palette not in theme_features.DEFAULT_PALETTES]

        assert not missing, (
            "Palette CSS files lack DEFAULT_PALETTES registration: " + ", ".join(missing)
        )
