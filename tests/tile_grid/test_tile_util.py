from tests.interface.tile import Tile
import pytest
TILE_UTIL_MACRO_PATH = "pluglets/tile_grid/templates/j2-macros/tile-util.j2"


@pytest.fixture
def tile_util_macro(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(TILE_UTIL_MACRO_PATH)


def assert_link_only_tile_expectations(macro, tile):
    assert "true" == macro.module.has_link(tile)
    assert "true" == macro.module.is_valid(tile)
    assert "true" == macro.module.is_link_only(tile)

    assert "false" == macro.module.has_image(tile)
    assert "false" == macro.module.is_image_only(tile)
    assert "false" == macro.module.is_linked_image(tile)


def assert_image_only_tile_expectations(macro, tile):
    assert "true" == macro.module.has_image(tile)
    assert "true" == macro.module.is_valid(tile)
    assert "true" == macro.module.is_image_only(tile)

    assert "false" == macro.module.has_link(tile)
    assert "false" == macro.module.is_link_only(tile)
    assert "false" == macro.module.is_linked_image(tile)


def assert_linked_image_tile_expectations(macro, tile):
    assert "true" == macro.module.has_link(tile)
    assert "true" == macro.module.has_image(tile)
    assert "true" == macro.module.is_valid(tile)
    assert "true" == macro.module.is_linked_image(tile)

    assert "false" == macro.module.is_link_only(tile)
    assert "false" == macro.module.is_image_only(tile)


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

    def test_utils_with_minimal_link_tile(self, tile_util_macro, minimal_link_tile):
        assert_link_only_tile_expectations(tile_util_macro, minimal_link_tile)
        assert "false" == tile_util_macro.module.has_caption(minimal_link_tile)

    def test_utils_with_valid_link_tile(self, tile_util_macro, valid_link_only_tile):
        assert_link_only_tile_expectations(tile_util_macro, valid_link_only_tile)
        assert "true" == tile_util_macro.module.has_caption(valid_link_only_tile)

    def test_utils_with_minimal_image_tile(self, tile_util_macro, minimal_image_tile):
        assert_image_only_tile_expectations(tile_util_macro, minimal_image_tile)
        assert "false" == tile_util_macro.module.has_caption(minimal_image_tile)

    def test_utils_with_valid_image_tile(self, tile_util_macro, valid_image_only_tile):
        assert_image_only_tile_expectations(tile_util_macro, valid_image_only_tile)
        assert "true" == tile_util_macro.module.has_caption(valid_image_only_tile)

    def test_integer_tile_does_not_throw_exception(self, tile_util_macro, all_integer_tile):
        tile = all_integer_tile
        try:
            assert "true" == tile_util_macro.module.has_link(tile)
            assert "true" == tile_util_macro.module.has_image(tile)
            assert "true" == tile_util_macro.module.is_valid(tile)
            assert "true" == tile_util_macro.module.is_linked_image(tile)
            assert "true" == tile_util_macro.module.has_caption(tile)

            assert "false" == tile_util_macro.module.is_link_only(tile)
            assert "false" == tile_util_macro.module.is_image_only(tile)
        except:
            pytest.fail("util macros should not throw exception")

    def test_utils_with_minimal_linked_image_tile(self, tile_util_macro, minimal_linked_image_tile):
        assert_linked_image_tile_expectations(tile_util_macro, minimal_linked_image_tile)
        assert "false" == tile_util_macro.module.has_caption(tile_util_macro)

    def test_utils_with_valid_linked_image_tile(self, tile_util_macro, valid_linked_image_tile):
        assert_linked_image_tile_expectations(tile_util_macro, valid_linked_image_tile)
        assert "true" == tile_util_macro.module.has_caption(valid_linked_image_tile)