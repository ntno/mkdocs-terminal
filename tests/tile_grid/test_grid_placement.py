from tests.utils.html import assert_valid_html
# from tests.utils.filters import mock_markup_filter
from tests.interface import page_features, theme_plugins, theme_features
import pytest
PAGE_BASE_PARTIAL_PATH = "partials/page-base.html"
INLINE_MACRO_CALL = "{{ tile_grid(page.meta) }}"

@pytest.fixture
def page_base_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(PAGE_BASE_PARTIAL_PATH)


@pytest.fixture
def tiles(minimal_linked_image_tile, minimal_link_tile, minimal_image_tile):
    return [minimal_linked_image_tile, minimal_link_tile, minimal_image_tile]


@pytest.fixture
def fully_enabled_config():
    enabled_config = {
        "config": {
            "plugins": [theme_plugins.REVISION],
            "theme": {
                "features": [
                    theme_features.SHOW_REVISION_DATE
                ]
            }
        }
    }
    return enabled_config


class TestGridPlacement():

    @pytest.mark.parametrize("grid_configuration, with_macro_call, expected_placement", [
        pytest.param(
            {}, False, "after", id="default_values"
        ),
        pytest.param(
            {page_features.SHOW_TILES_FIRST: False}, False, "after", id="show_last"
        ),
        pytest.param(
            {page_features.SHOW_TILES_FIRST: True}, False, "before", id="show_first"
        ),
        pytest.param(
            {page_features.SHOW_TILES_INLINE: True}, True, "inline", id="show_inline"
        ),
        pytest.param(
            {
                page_features.SHOW_TILES_INLINE: True,
                page_features.SHOW_TILES_FIRST: True
            }, 
            True,
            "inline", 
            id="inline_overrides_first"
        ),
    ])
    def test_that_grid_is_in_expected_place(self, grid_configuration, with_macro_call, expected_placement, page_base_partial, tiles, fully_enabled_config):
        tiles_meta = {"tiles": [tiles]}
        revision_meta = {"revision_date": "revision_date_placeholder"}
        page_meta = {**grid_configuration, **tiles_meta, **revision_meta}
        if(with_macro_call):
            page_content = "markdown_content_placeholder\n    " + INLINE_MACRO_CALL
        else:
            page_content = "markdown_content_placeholder" 
        context_data = {
            "page": {
                "content": page_content,
                "meta": page_meta
            },
            **fully_enabled_config
        }
        rendered_page = page_base_partial.render(context_data)
        assert_valid_html(rendered_page)
        assert "<section id=\"mkdocs-terminal-content\">" in rendered_page
        assert "markdown_content_placeholder" in rendered_page
        assert "<section id=\"mkdocs-terminal-revision\">" in rendered_page
        assert "revision_date_placeholder" in rendered_page
        before_content_indicator = "<section id=\"mkdocs-terminal-before-content\""
        after_content_indicator = "<section id=\"mkdocs-terminal-after-content\">"
        grid_indicator = "<div class=\"terminal-mkdocs-tile-grid \">"
        if (expected_placement == "before"):
            assert before_content_indicator in rendered_page
            assert grid_indicator in rendered_page
        elif (expected_placement == "after"):
            assert after_content_indicator in rendered_page
            assert grid_indicator in rendered_page
        elif (expected_placement == "inline"):
            assert before_content_indicator not in rendered_page
            assert after_content_indicator not in rendered_page
            assert grid_indicator not in rendered_page
