from terminal.pluglets.tile_grid.util import tile_grid
from tests.utils.html import assert_valid_html
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def grid_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("pluglets/tile_grid/templates/j2-partials/tiles.html")


class TestTileGridPluglet():

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
        assert "USAGE" in pluglet_output
        pluglet_macro_mock.assert_not_called()

    @patch('terminal.pluglets.tile_grid.MACRO')
    def test_pluglet_renders_grid_with_one_tile(self, pluglet_macro_mock, minimal_linked_image_tile, grid_partial):
        mock_jinja2_env = MagicMock()
        mock_jinja2_env_attr = {'get_template.return_value': grid_partial}
        mock_jinja2_env.configure_mock(**mock_jinja2_env_attr)
        pluglet_macro_mock_attr = {'jinja2_env': mock_jinja2_env}
        pluglet_macro_mock.configure_mock(**pluglet_macro_mock_attr)

        minimal_linked_image_tile.tile_id = "myTileId"
        page_meta = {"tiles": [minimal_linked_image_tile]}
        pluglet_output = tile_grid(page_meta)
        assert "USAGE" not in pluglet_output
        assert "id=\"myTileId\"" in pluglet_output
        assert_valid_html(pluglet_output)
