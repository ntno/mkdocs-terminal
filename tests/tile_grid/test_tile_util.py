from tests.interface.tile import Tile
import pytest
TILE_UTIL_MACRO_PATH = "pluglets/tile_grid/templates/j2-macros/tile-util.j2"


@pytest.fixture
def tile_util_macro(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(TILE_UTIL_MACRO_PATH)


class TestTileUtil():

    def test_empty_tile_is_empty(self, tile_util_macro, empty_tile):
        tile = empty_tile
        assert "false" == tile_util_macro.module.has_link(tile)
        assert "false" == tile_util_macro.module.has_image(tile)
        assert "false" == tile_util_macro.module.has_caption(tile)
        assert "false" == tile_util_macro.module.is_valid(tile)
        assert "false" == tile_util_macro.module.is_link_only(tile)
        assert "false" == tile_util_macro.module.is_image_only(tile)
        assert "false" == tile_util_macro.module.is_linked_image(tile)

    def test_minimal_link_tile_is_valid(self, tile_util_macro, minimal_link_tile):
        tile = minimal_link_tile
        assert "true" == tile_util_macro.module.has_link(tile)
        assert "true" == tile_util_macro.module.is_valid(tile)
        assert "true" == tile_util_macro.module.is_link_only(tile)

        assert "false" == tile_util_macro.module.has_image(tile)
        assert "false" == tile_util_macro.module.has_caption(tile)
        assert "false" == tile_util_macro.module.is_image_only(tile)
        assert "false" == tile_util_macro.module.is_linked_image(tile)

    def test_minimal_image_tile_is_valid(self, tile_util_macro, minimal_image_tile):
        tile = minimal_image_tile
        assert "true" == tile_util_macro.module.has_image(tile)
        assert "true" == tile_util_macro.module.is_valid(tile)
        assert "true" == tile_util_macro.module.is_image_only(tile)

        assert "false" == tile_util_macro.module.has_link(tile)        
        assert "false" == tile_util_macro.module.has_caption(tile)
        assert "false" == tile_util_macro.module.is_link_only(tile)
        assert "false" == tile_util_macro.module.is_linked_image(tile)

    def test_minimal_linked_image_tile_is_valid(self, tile_util_macro, minimal_linked_image_tile):
        tile = minimal_linked_image_tile
        assert "true" == tile_util_macro.module.has_link(tile)
        assert "true" == tile_util_macro.module.has_image(tile)
        assert "true" == tile_util_macro.module.is_valid(tile)
        assert "true" == tile_util_macro.module.is_linked_image(tile)

        assert "false" == tile_util_macro.module.has_caption(tile)
        assert "false" == tile_util_macro.module.is_link_only(tile)
        assert "false" == tile_util_macro.module.is_image_only(tile)