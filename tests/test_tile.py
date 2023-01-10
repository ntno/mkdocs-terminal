import pytest
from tests.tile import Tile

class TestTile():

    def test_empty_tile(self, env_with_terminal_loader, empty_tile):
        assert isinstance(empty_tile, Tile)
        
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(empty_tile)
        assert rendered_tile.strip() == ""


    def test_minimal_link_tile(self, env_with_terminal_loader, minimal_link_tile):
        assert isinstance(minimal_link_tile, Tile)
        
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_link_tile)
        assert rendered_tile.strip() != ""
        assert "<a " in rendered_tile
        assert "</a>" in rendered_tile
        assert "<img " not in rendered_tile
        #TODO assert contains <div/figure/a>

    def test_minimal_image_tile(self, env_with_terminal_loader, minimal_image_tile):
        assert isinstance(minimal_image_tile, Tile)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_image_tile)
        assert rendered_tile.strip() != ""
        assert "<a " not in rendered_tile
        assert "</a>" not in rendered_tile
        assert "<img " in rendered_tile
        #TODO assert contains <div/figure/img>

    def test_minimal_linked_img_tile(self, env_with_terminal_loader, minimal_linked_image_tile):
        assert isinstance(minimal_linked_image_tile, Tile)
        tile_macro = env_with_terminal_loader.get_template("macros/tile.j2")
        rendered_tile = tile_macro.module.make_tile(minimal_linked_image_tile)
        assert rendered_tile.strip() != ""
        assert "<a " in rendered_tile
        assert "</a>" in rendered_tile
        assert "<img " in rendered_tile
        #TODO assert contains <div/figure/a/img>