from tests.utils.html import assert_valid_html
import pytest


class TestGrid():

    def test_grid_with_no_tiles_is_empty_string(self, env_with_terminal_loader):
        grid_partial = env_with_terminal_loader.get_template("partials/tiles.html")
        rendered_grid = grid_partial.render()
        assert rendered_grid.strip() == ""

    def test_grid_with_one_tile(self, env_with_terminal_loader, minimal_linked_image_tile):
        grid_partial = env_with_terminal_loader.get_template("partials/tiles.html")
        context_data = {
            "page": {
                "meta": {
                    "tiles": [minimal_linked_image_tile]
                }
            }
        }
        grid_partial.new_context(context_data)
        rendered_grid = grid_partial.render(context_data)
        assert "class=\"terminal-mkdocs-tile-grid \">" in rendered_grid
        assert_valid_html(rendered_grid)

    def test_that_grid_includes_all_valid_tiles(self, env_with_terminal_loader, minimal_linked_image_tile, minimal_link_tile, minimal_image_tile, empty_tile):
        grid_partial = env_with_terminal_loader.get_template("partials/tiles.html")
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
        grid_partial.new_context(context_data)
        rendered_grid = grid_partial.render(context_data)
        assert "class=\"terminal-mkdocs-tile-grid \">" in rendered_grid
        assert "id=\"myLinkedImageTile\"" in rendered_grid
        assert "id=\"myLinkOnlyTile\"" in rendered_grid
        assert "id=\"myImageOnlyTile\"" in rendered_grid
        assert "id=\"myInvalidTile\"" not in rendered_grid
        assert_valid_html(rendered_grid)

    def test_grid_id_and_css_set(self, env_with_terminal_loader, minimal_linked_image_tile):
        grid_partial = env_with_terminal_loader.get_template("partials/tiles.html")
        context_data = {
            "page": {
                "meta": {
                    "grid_id": "myGridId",
                    "grid_css": "myGridCss",
                    "tiles": [minimal_linked_image_tile]
                }
            }
        }
        grid_partial.new_context(context_data)
        rendered_grid = grid_partial.render(context_data)
        assert "id=\"myGridId\"" in rendered_grid
        assert "class=\"terminal-mkdocs-tile-grid myGridCss\">" in rendered_grid
        assert_valid_html(rendered_grid)

    def test_grid_renders_with_integer_input(self, env_with_terminal_loader):
        grid_partial = env_with_terminal_loader.get_template("partials/tiles.html")
        context_data = {
            "page": {
                "meta": {
                    "grid_id": 0,
                    "grid_css": 1,
                    "tiles": 3
                }
            }
        }
        grid_partial.new_context(context_data)
        try:
            grid_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_grid_renders_with_integer_tile_input(self, env_with_terminal_loader, all_integer_tile):
        grid_partial = env_with_terminal_loader.get_template("partials/tiles.html")
        context_data = {
            "page": {
                "meta": {
                    "grid_id": 0,
                    "grid_css": 1,
                    "tiles": [all_integer_tile]
                }
            }
        }
        grid_partial.new_context(context_data)
        try:
            grid_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
