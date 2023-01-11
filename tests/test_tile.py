from tests.utils.tile import Tile
from tests.utils.html import check_html
from tests import defaults
import pytest


class TestTile():

    def test_empty_tile(self, env_with_terminal_loader, empty_tile):
        assert isinstance(empty_tile, Tile)

        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(empty_tile)
        assert rendered_tile.strip() == ""
        assert len(check_html(rendered_tile)["errors"]) == 0

    def test_minimal_link_tile(self, env_with_terminal_loader, minimal_link_tile):
        assert isinstance(minimal_link_tile, Tile)

        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_link_tile)
        assert rendered_tile.strip() != ""
        assert "<a " in rendered_tile
        assert "</a>" in rendered_tile
        assert "<img " not in rendered_tile
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/a
        assert len(check_html(rendered_tile)["errors"]) == 0

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
        assert len(check_html(rendered_tile)["errors"]) == 0

    def test_minimal_linked_img_tile(self, env_with_terminal_loader, minimal_linked_image_tile):
        assert isinstance(minimal_linked_image_tile, Tile)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_linked_image_tile)
        assert rendered_tile.strip() != ""
        assert "<a " in rendered_tile
        assert "</a>" in rendered_tile
        assert "<img " in rendered_tile
        assert "id=" not in rendered_tile
        # TODO assert contains <div/figure/a/img>
        assert len(check_html(rendered_tile)["errors"]) == 0

    @pytest.mark.skip(reason="breaking change needs to be fixed in major release")
    def test_id_and_class_added_to_tile(self, env_with_terminal_loader):
        tile = Tile(html_id="myId", css_class="myClass", link_href=defaults.GITHUB_LINK_HREF)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(tile)
        assert rendered_tile.strip() != ""
        assert "id=\"myID\"" in rendered_tile
        assert "class=\"terminal-mkdocs-tile myClass\"" in rendered_tile
        assert len(check_html(rendered_tile)["errors"]) == 0

    def test_that_tile_renders_with_integer_inputs(self, env_with_terminal_loader, all_integer_tile):
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        try:
            print(tile_macro.module.make_tile(all_integer_tile))
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
