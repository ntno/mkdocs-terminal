from tests.utils.tile import Tile
from tests.utils.html import check_html
from tests import defaults
import pytest


class TestTileImage():

    def test_empty_image_is_invalid(self, env_with_terminal_loader, empty_tile):
        assert isinstance(empty_tile, Tile)
        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        rendered_image = image_macro.module.make_image(empty_tile)
        assert len(check_html(rendered_image)["errors"]) > 0

    def test_minimal_image_only_includes_required(self, env_with_terminal_loader, minimal_image_tile):
        assert isinstance(minimal_image_tile, Tile)
        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        rendered_image = image_macro.module.make_image(minimal_image_tile)
        assert len(check_html(rendered_image)["errors"]) == 0
        assert "src=\"" + defaults.GITHUB_IMG_SRC + "\"" in rendered_image
        assert "alt=\"\"" in rendered_image
        assert "title=\"" not in rendered_image
        assert "width=\"" not in rendered_image
        assert "height=\"" not in rendered_image

    def test_all_img_attributes_used(self, env_with_terminal_loader):
        tile = Tile(img_alt=defaults.GITHUB_IMG_ALT, img_src=defaults.GITHUB_IMG_SRC, img_title=defaults.GITHUB_IMG_TITLE, img_width=defaults.GITHUB_IMG_WIDTH, img_height=defaults.GITHUB_IMG_HEIGHT)
        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        rendered_image = image_macro.module.make_image(tile)
        assert "alt=\"" + defaults.GITHUB_IMG_ALT + "\"" in rendered_image
        assert "src=\"" + defaults.GITHUB_IMG_SRC + "\"" in rendered_image
        assert "title=\"" + defaults.GITHUB_IMG_TITLE + "\"" in rendered_image
        assert "width=\"" + defaults.GITHUB_IMG_WIDTH + "\"" in rendered_image
        assert "height=\"" + defaults.GITHUB_IMG_HEIGHT + "\"" in rendered_image
        assert len(check_html(rendered_image)["errors"]) == 0

    def test_that_img_tile_renders_for_integer_width_and_height(self, env_with_terminal_loader):
        tile = Tile(img_width=100, img_height=200, img_src=defaults.GITHUB_IMG_SRC)
        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        rendered_image = image_macro.module.make_image(tile)
        assert len(check_html(rendered_image)["errors"]) == 0

    def test_that_img_tile_renders_with_integer_inputs(self, env_with_terminal_loader, all_integer_tile):
        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        try:
            print("\n", image_macro.module.make_image(all_integer_tile))
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
