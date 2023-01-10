from tests.utils.tile import Tile
from tests.utils.html import check_html
from tests import defaults


class TestTileImage():

    def test_empty_image_is_invalid(self, env_with_terminal_loader, empty_tile):
        assert isinstance(empty_tile, Tile)

        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        rendered_image = image_macro.module.make_image(empty_tile)
        assert len(check_html(rendered_image)["errors"]) > 0

    def test_all_img_attributes_used(self, env_with_terminal_loader):
        tile = Tile(img_alt=defaults.GITHUB_IMG_ALT, img_src=defaults.GITHUB_IMG_SRC, img_title=defaults.GITHUB_IMG_TITLE)
        image_macro = env_with_terminal_loader.get_template("macros/tile-image.j2")
        rendered_image = image_macro.module.make_image(tile)
        assert "alt=\"" + defaults.GITHUB_IMG_ALT + "\"" in rendered_image
        assert "src=\"" + defaults.GITHUB_IMG_SRC + "\"" in rendered_image
        assert "title=\"" + defaults.GITHUB_IMG_TITLE + "\"" in rendered_image
        assert len(check_html(rendered_image)["errors"]) == 0
