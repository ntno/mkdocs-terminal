from terminal.pluglets.tile_grid.util import tile_grid
from tests.utils.html import assert_valid_html
from tests.interface import theme_pluglets
from unittest.mock import patch
import pytest


@pytest.fixture
def grid_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("pluglets/tile_grid/templates/j2-partials/tiles.html")


class TestTileGridPlugletUserInterface():

    @patch('terminal.pluglets.tile_grid.MACRO')
    @pytest.mark.parametrize("bad_input", [
        pytest.param(
            None, id="null_input"
        ),
        pytest.param(
            {}, id="empty_dict_input"
        ),
        pytest.param(
            [], id="list_input"
        ),
        pytest.param(
            "tiles", id="string_input"
        )
    ])
    # NOTE: the order of the inputs passed to the test is important here
    # the patched mock needs to come before the pytest param
    # see https://github.com/hackebrot/pytest-tricks/issues/32
    def test_usage_message_when_bad_input(self, pluglet_macro_mock, bad_input):
        pluglet_output = tile_grid(bad_input)
        assert theme_pluglets.TILE_GRID_MACRO_USAGE_MESSAGE == pluglet_output
        assert_valid_html(pluglet_output)
        pluglet_macro_mock.jinja2_env.get_template.assert_not_called()

    @patch('terminal.pluglets.tile_grid.MACRO')
    def test_pluglet_renders_grid_with_one_tile(self, pluglet_macro_mock, minimal_linked_image_tile, grid_partial):
        pluglet_macro_mock.jinja2_env.get_template.return_value = grid_partial

        minimal_linked_image_tile.tile_id = "myTileId"
        page_meta = {"tiles": [minimal_linked_image_tile]}
        pluglet_output = tile_grid(page_meta)
        assert theme_pluglets.TILE_GRID_MACRO_USAGE_MESSAGE not in pluglet_output
        assert "id=\"myTileId\"" in pluglet_output
        assert_valid_html(pluglet_output)
        pluglet_macro_mock.jinja2_env.get_template.assert_called_once()
        pluglet_macro_mock.jinja2_env.get_template.assert_called_with("pluglets/tile_grid/templates/j2-partials/tiles.html")
