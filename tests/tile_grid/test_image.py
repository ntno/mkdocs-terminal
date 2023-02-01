from tests.interface.tile import Tile
from tests.utils.html import check_html
from tests.utils.html import assert_valid_html
from tests import defaults
import pytest


@pytest.fixture
def image_macro(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("pluglets/tile_grid/templates/j2-macros/tile-image.j2")


class TestImage():

    def test_empty_image_is_invalid(self, image_macro, empty_tile):
        rendered_image = image_macro.module.make_image(empty_tile)
        assert len(check_html(rendered_image)["errors"]) > 0

    def test_minimal_image_only_includes_required(self, image_macro, minimal_image_tile):
        rendered_image = image_macro.module.make_image(minimal_image_tile)
        assert "src=\"" + defaults.GITHUB_IMG_SRC + "\"" in rendered_image
        assert "alt=\"\"" in rendered_image
        assert "title=\"" not in rendered_image
        assert "width=\"" not in rendered_image
        assert "height=\"" not in rendered_image
        assert_valid_html(rendered_image)

    def test_all_img_attributes_used(self, image_macro):
        tile = Tile(text=defaults.GITHUB_IMG_DESCRIPTION, title="what a cute octopuss", img_src=defaults.GITHUB_IMG_SRC, img_width=defaults.GITHUB_IMG_WIDTH, img_height=defaults.GITHUB_IMG_HEIGHT)
        rendered_image = image_macro.module.make_image(tile)
        assert "alt=\"" + defaults.GITHUB_IMG_DESCRIPTION + "\"" in rendered_image
        assert "src=\"" + defaults.GITHUB_IMG_SRC + "\"" in rendered_image
        assert "title=\"" + "what a cute octopuss" + "\"" in rendered_image
        assert "width=\"" + defaults.GITHUB_IMG_WIDTH + "\"" in rendered_image
        assert "height=\"" + defaults.GITHUB_IMG_HEIGHT + "\"" in rendered_image
        assert_valid_html(rendered_image)

    def test_that_img_tile_renders_for_integer_width_and_height(self, image_macro):
        tile = Tile(img_width=100, img_height=200, img_src=defaults.GITHUB_IMG_SRC)
        rendered_image = image_macro.module.make_image(tile)
        assert_valid_html(rendered_image)

    def test_that_img_tile_renders_with_integer_inputs(self, image_macro, all_integer_tile):
        try:
            image_macro.module.make_image(all_integer_tile)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
