from tests.utils.html import assert_valid_html
# from tests.utils.filters import mock_markup_filter
from tests.interface import page_features
import pytest
PAGE_BASE_PARTIAL_PATH = "partials/page-base.html"


@pytest.fixture
def page_base_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(PAGE_BASE_PARTIAL_PATH)


@pytest.fixture
def tiles(minimal_linked_image_tile, minimal_link_tile, minimal_image_tile):
    minimal_linked_image_tile.tile_id = "myLinkedImageTile"
    minimal_link_tile.tile_id = "myLinkOnlyTile"
    minimal_image_tile.tile_id = "myImageOnlyTile"
    return [minimal_linked_image_tile, minimal_link_tile, minimal_image_tile]


class TestGridPlacement():

    def test_that_grid_is_after_markdown_content_by_default(self):
        pass

    @pytest.mark.parametrize("grid_configuration, expected_placement", [
        pytest.param(
            {}, "after", id="default_values"
        ),
        pytest.param(
            {page_features.SHOW_TILES_FIRST: False}, "after", id="show_last"
        ),
        pytest.param(
            {page_features.SHOW_TILES_FIRST: True}, "before", id="show_first"
        ),
        pytest.param(
            {page_features.SHOW_TILES_INLINE: True}, "inline", id="show_inline"
        ),
        pytest.param(
            {
                page_features.SHOW_TILES_INLINE: True,
                page_features.SHOW_TILES_FIRST: True
            }, "inline", id="inline_overrides_first"
        ),
    ])
    def test_that_grid_is_in_expected_place(self, grid_configuration, expected_placement, page_base_partial, tiles):
        print(grid_configuration)
        print(expected_placement)
        context_data = {
            "page": {
                "content": "placeholder_markdown_content",
                "meta": {
                    "tiles": [tiles]
                }
            },
            "config":{
                "theme":{}
            }
        }
        rendered_page = page_base_partial.render(context_data)
        assert_valid_html(rendered_page)
        assert "class=\"terminal-mkdocs-tile-grid \">" in rendered_page
        assert "id=\"myLinkedImageTile\"" in rendered_page
        assert "id=\"myLinkOnlyTile\"" in rendered_page
        assert "id=\"myImageOnlyTile\"" in rendered_page

