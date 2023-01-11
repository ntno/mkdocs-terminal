from tests.utils.tile import Tile
from tests.conftest import assert_valid_html
from tests import defaults
import pytest


def assert_tile_has_terminal_marker(html):
    assert "class=\"terminal-mkdocs-tile " in html


def tile_has_anchor(html):
    return "<a " in html and "</a>" in html


def tile_has_img(html):
    return "<img " in html


def assert_tile_has_anchor(html):
    assert tile_has_anchor(html)


def assert_tile_has_img(html):
    assert tile_has_img(html)


class TestTile():

    def test_empty_tile(self, env_with_terminal_loader, empty_tile):
        assert isinstance(empty_tile, Tile)

        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(empty_tile)
        assert rendered_tile.strip() == ""
        assert_valid_html(rendered_tile)

    def test_minimal_link_tile(self, env_with_terminal_loader, minimal_link_tile):
        assert isinstance(minimal_link_tile, Tile)

        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_link_tile)
        assert rendered_tile.strip() != ""
        assert_tile_has_anchor(rendered_tile)
        assert "<img " not in rendered_tile
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/a
        assert_valid_html(rendered_tile)

    def test_minimal_image_tile(self, env_with_terminal_loader, minimal_image_tile):
        assert isinstance(minimal_image_tile, Tile)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_image_tile)
        assert rendered_tile.strip() != ""
        assert "<a " not in rendered_tile
        assert "</a>" not in rendered_tile
        assert "<img " in rendered_tile
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/img>
        assert_valid_html(rendered_tile)

    def test_minimal_linked_img_tile(self, env_with_terminal_loader, minimal_linked_image_tile):
        assert isinstance(minimal_linked_image_tile, Tile)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_linked_image_tile)
        assert rendered_tile.strip() != ""
        assert_tile_has_anchor(rendered_tile)
        assert_tile_has_img(rendered_tile)
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/a/img>
        assert_valid_html(rendered_tile)

    @pytest.mark.skip(reason="breaking change needs to be fixed in major release")
    def test_id_and_class_added_to_tile(self, env_with_terminal_loader):
        tile = Tile(html_id="myId", css_class="myClass", link_href=defaults.GITHUB_LINK_HREF)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(tile)
        assert rendered_tile.strip() != ""
        assert "id=\"myID\"" in rendered_tile
        assert "class=\"terminal-mkdocs-tile myClass\"" in rendered_tile
        assert_valid_html(rendered_tile)
