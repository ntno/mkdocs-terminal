from tests.utils.tile import Tile
from tests.utils.html import assert_valid_html, tile_has_anchor, tile_has_img
from tests import defaults
import pytest


class TestTile():

    def test_empty_tile(self, env_with_terminal_loader, empty_tile):
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(empty_tile)
        assert rendered_tile.strip() == ""
        assert_valid_html(rendered_tile)

    def test_minimal_link_tile(self, env_with_terminal_loader, minimal_link_tile):
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_link_tile)
        assert tile_has_anchor(rendered_tile)
        assert not tile_has_img(rendered_tile)
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/a
        assert_valid_html(rendered_tile)

    def test_minimal_image_tile(self, env_with_terminal_loader, minimal_image_tile):
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_image_tile)
        assert tile_has_img(rendered_tile)
        assert not tile_has_anchor(rendered_tile)
        assert_valid_html(rendered_tile)

    def test_minimal_linked_img_tile(self, env_with_terminal_loader, minimal_linked_image_tile):
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_linked_image_tile)
        assert tile_has_anchor(rendered_tile)
        assert tile_has_img(rendered_tile)
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/a/img>
        assert_valid_html(rendered_tile)

    @pytest.mark.skip(reason="breaking change needs to be fixed in major release")
    def test_id_and_class_added_to_tile(self, env_with_terminal_loader):
        tile = Tile(html_id="myId", css_class="myClass", link_href=defaults.GITHUB_LINK_HREF)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(tile)
        assert "id=\"myID\"" in rendered_tile
        assert "class=\"terminal-mkdocs-tile myClass\"" in rendered_tile
        assert_valid_html(rendered_tile)
