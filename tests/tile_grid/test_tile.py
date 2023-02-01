from tests.interface.tile import Tile
from tests.utils.html import assert_valid_html, tile_has_anchor, tile_has_img
from tests.utils.filters import mock_markup_filter
from tests import defaults
import pytest
TILE_MACRO_PATH = "pluglets/tile_grid/templates/j2-macros/tile.j2"


@pytest.fixture
def tile_macro(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(TILE_MACRO_PATH)


class TestTile():

    def test_empty_tile(self, tile_macro, empty_tile):
        rendered_tile = tile_macro.module.make_tile(empty_tile)
        assert rendered_tile.strip() == ""

    def test_minimal_link_tile(self, tile_macro, minimal_link_tile):
        rendered_tile = tile_macro.module.make_tile(minimal_link_tile)
        assert tile_has_anchor(rendered_tile)
        assert not tile_has_img(rendered_tile)
        assert "id=" not in rendered_tile
        assert_valid_html(rendered_tile)

    def test_minimal_image_tile(self, tile_macro, minimal_image_tile):
        rendered_tile = tile_macro.module.make_tile(minimal_image_tile)
        assert tile_has_img(rendered_tile)
        assert not tile_has_anchor(rendered_tile)
        assert_valid_html(rendered_tile)

    def test_minimal_linked_img_tile(self, tile_macro, minimal_linked_image_tile):
        rendered_tile = tile_macro.module.make_tile(minimal_linked_image_tile)
        assert tile_has_anchor(rendered_tile)
        assert tile_has_img(rendered_tile)
        assert "id=" not in rendered_tile
        assert_valid_html(rendered_tile)

    def test_id_and_class_added_to_tile(self, tile_macro):
        tile = Tile(tile_id="myTileId", tile_css="myTileClass", link_href=defaults.GITHUB_LINK_HREF)
        rendered_tile = tile_macro.module.make_tile(tile)
        assert "id=\"myTileId\"" in rendered_tile
        assert "class=\"terminal-mkdocs-tile myTileClass\"" in rendered_tile
        assert_valid_html(rendered_tile)

    def test_backup_text_added_to_link_only_tile(self, tile_macro):
        tile = Tile(text="link_display_text", link_href=defaults.GITHUB_LINK_HREF)
        rendered_tile = tile_macro.module.make_tile(tile)
        assert ">link_display_text</a>" in rendered_tile
        assert_valid_html(rendered_tile)

    def test_link_backup_text_ignored_when_image_included(self, tile_macro, valid_linked_image_tile):
        valid_linked_image_tile.link_text = "an unusual backup text"
        rendered_tile = tile_macro.module.make_tile(valid_linked_image_tile)
        assert "an unusual backup text" not in rendered_tile
        assert_valid_html(rendered_tile)

    def test_href_used_as_display_when_no_backup_text(self, tile_macro):
        tile = Tile(link_href=defaults.GITHUB_LINK_HREF)
        rendered_tile = tile_macro.module.make_tile(tile)
        assert ">" + defaults.GITHUB_LINK_HREF + "</a>" in rendered_tile
        assert_valid_html(rendered_tile)

    def test_that_tile_renders_with_integer_inputs(self, tile_macro, all_integer_tile):
        try:
            tile_macro.module.make_tile(all_integer_tile)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_caption_when_run_through_markup_filter(self, tile_macro, valid_linked_image_tile):
        valid_linked_image_tile.caption = "myCaption"
        rendered_tile = tile_macro.module.make_tile(valid_linked_image_tile, True)
        expected_figcaption = mock_markup_filter(context={}, value="myCaption")
        expected_html = "<figcaption>" + expected_figcaption + "</figcaption>"
        assert expected_html in rendered_tile
        assert_valid_html(rendered_tile)

    def test_caption_when_markup_filter_not_used(self, tile_macro, valid_linked_image_tile):
        valid_linked_image_tile.caption = "myCaption"
        rendered_tile = tile_macro.module.make_tile(valid_linked_image_tile, False)
        expected_html = "<figcaption>myCaption</figcaption>"
        assert expected_html in rendered_tile
        assert_valid_html(rendered_tile)
