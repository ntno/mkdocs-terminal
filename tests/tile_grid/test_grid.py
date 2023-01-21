from tests.utils.html import assert_valid_html
from tests.utils.filters import mock_markup_filter
from terminal.plugins.md_to_html.plugin import DEFAULT_MARKUP_FILTER_NAME
import pytest
GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"


@pytest.fixture
def grid_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(GRID_PARTIAL_PATH)


@pytest.fixture
def env_without_markup_filter(env_with_terminal_loader):
    del env_with_terminal_loader.filters[DEFAULT_MARKUP_FILTER_NAME]
    return env_with_terminal_loader


class TestGrid():

    def test_grid_with_no_tiles_is_empty_string(self, grid_partial):
        rendered_grid = grid_partial.render()
        assert rendered_grid.strip() == ""

    def test_grid_with_one_tile(self, minimal_linked_image_tile, grid_partial):
        context_data = {
            "page": {
                "meta": {
                    "tiles": [minimal_linked_image_tile]
                }
            }
        }
        rendered_grid = grid_partial.render(context_data)
        assert "class=\"terminal-mkdocs-tile-grid \">" in rendered_grid
        assert_valid_html(rendered_grid)

    def test_that_grid_includes_all_valid_tiles(self, minimal_linked_image_tile, minimal_link_tile, minimal_image_tile, empty_tile, grid_partial):
        minimal_linked_image_tile.tile_id = "myLinkedImageTile"
        minimal_link_tile.tile_id = "myLinkOnlyTile"
        empty_tile.tile_id = "myInvalidTile"
        minimal_image_tile.tile_id = "myImageOnlyTile"

        context_data = {
            "page": {
                "meta": {
                    "tiles": [minimal_linked_image_tile, minimal_link_tile, empty_tile, minimal_image_tile]
                }
            }
        }
        rendered_grid = grid_partial.render(context_data)
        assert "class=\"terminal-mkdocs-tile-grid \">" in rendered_grid
        assert "id=\"myLinkedImageTile\"" in rendered_grid
        assert "id=\"myLinkOnlyTile\"" in rendered_grid
        assert "id=\"myImageOnlyTile\"" in rendered_grid
        assert "id=\"myInvalidTile\"" not in rendered_grid
        assert_valid_html(rendered_grid)

    def test_grid_id_and_css_set(self, minimal_linked_image_tile, grid_partial):
        context_data = {
            "page": {
                "meta": {
                    "grid_id": "myGridId",
                    "grid_css": "myGridCss",
                    "tiles": [minimal_linked_image_tile]
                }
            }
        }
        rendered_grid = grid_partial.render(context_data)
        assert "id=\"myGridId\"" in rendered_grid
        assert "class=\"terminal-mkdocs-tile-grid myGridCss\">" in rendered_grid
        assert_valid_html(rendered_grid)

    def test_grid_renders_with_integer_input(self, grid_partial):
        context_data = {
            "page": {
                "meta": {
                    "grid_id": 0,
                    "grid_css": 1,
                    "tiles": 3
                }
            }
        }
        try:
            grid_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_grid_renders_with_integer_tile_input(self, all_integer_tile, grid_partial):
        context_data = {
            "page": {
                "meta": {
                    "grid_id": 0,
                    "grid_css": 1,
                    "tiles": [all_integer_tile]
                }
            }
        }
        try:
            grid_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_no_render_error_if_markup_filter_undefined(self, env_without_markup_filter, valid_linked_image_tile):
        grid_partial = env_without_markup_filter.get_template(GRID_PARTIAL_PATH)
        try:
            context_data = {
                "page": {
                    "meta": {
                        "grid_id": "myGridId",
                        "grid_css": "myGridCss",
                        "tiles": [valid_linked_image_tile]
                    }
                }
            }
            grid_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_caption_is_not_run_through_markup_filter_if_md_to_html_plugin_disabled(self, valid_linked_image_tile, grid_partial):
        valid_linked_image_tile.caption = "myCaption"
        expected_html = "<figcaption>myCaption</figcaption>"
        context_data = {
            "config": {
                "plugins": []
            },
            "page": {
                "meta": {
                    "grid_id": "myGridId",
                    "grid_css": "myGridCss",
                    "tiles": [valid_linked_image_tile]
                }
            }
        }
        rendered_grid = grid_partial.render(context_data)
        assert expected_html in rendered_grid
        assert_valid_html(rendered_grid)

    @pytest.mark.parametrize("plugin_name", [
        pytest.param(
            "md-to-html", id="implicit-theme-namespace"
        ),
        pytest.param(
            "terminal/md-to-html", id="explicit-theme-namespace"
        )
    ])
    def test_caption_is_run_through_markup_filter_if_md_to_html_plugin_enabled(self, plugin_name, valid_linked_image_tile, grid_partial):
        valid_linked_image_tile.caption = "myCaption"
        expected_figcaption = mock_markup_filter(context={}, value="myCaption")
        expected_html = "<figcaption>" + expected_figcaption + "</figcaption>"
        context_data = {
            "config": {
                "plugins": [plugin_name]
            },
            "page": {
                "meta": {
                    "grid_id": "myGridId",
                    "grid_css": "myGridCss",
                    "tiles": [valid_linked_image_tile]
                }
            }
        }
        rendered_grid = grid_partial.render(context_data)
        assert expected_html in rendered_grid
        assert_valid_html(rendered_grid)
