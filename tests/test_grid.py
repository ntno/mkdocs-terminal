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

        try:
            grid_partial.new_context(context_data)
            rendered_grid = grid_partial.render(context_data)
            print(rendered_grid)
            assert "class=\"terminal-mkdocs-tile-grid\">" in rendered_grid
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
