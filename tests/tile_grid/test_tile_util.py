from tests.interface.tile import Tile
from tests.utils.html import assert_valid_html, tile_has_anchor, tile_has_img
from tests.utils.filters import mock_markup_filter
from tests import defaults
import pytest
TILE_UTIL_MACRO_PATH = "pluglets/tile_grid/templates/j2-macros/tile-util.j2"


@pytest.fixture
def tile_util_macro(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(TILE_UTIL_MACRO_PATH)


class TestTileUtil():

    def test_empty_tile_is_empty(self, tile_util_macro, empty_tile):
        assert "false" == tile_util_macro.module.has_link(empty_tile)
        assert "false" == tile_util_macro.module.has_image(empty_tile)
        assert "false" == tile_util_macro.module.has_caption(empty_tile)
        assert "false" == tile_util_macro.module.is_valid(empty_tile)

    def test_minimal_link_tile_is_valid(self, tile_util_macro, minimal_link_tile):
        assert "true" == tile_util_macro.module.has_link(minimal_link_tile)
        assert "false" == tile_util_macro.module.has_image(minimal_link_tile)
        assert "false" == tile_util_macro.module.has_caption(minimal_link_tile)
        assert "true" == tile_util_macro.module.is_valid(minimal_link_tile)
        assert "true" == tile_util_macro.module.is_link_only(minimal_link_tile)        