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
        tile = Tile(alt_text=defaults.GITHUB_IMG_ONLY_DESCRIPTION, tooltip=defaults.GITHUB_IMG_ONLY_TOOLTIP, img_src=defaults.GITHUB_IMG_SRC, img_width=defaults.GITHUB_IMG_WIDTH, img_height=defaults.GITHUB_IMG_HEIGHT)
        rendered_image = image_macro.module.make_image(tile)
        assert "alt=\"" + defaults.GITHUB_IMG_ONLY_DESCRIPTION + "\"" in rendered_image
        assert "src=\"" + defaults.GITHUB_IMG_SRC + "\"" in rendered_image
        assert "title=\"" + defaults.GITHUB_IMG_ONLY_TOOLTIP + "\"" in rendered_image
        assert_valid_html(rendered_image)

    def test_that_img_tile_renders_with_integer_inputs(self, image_macro, all_integer_tile):
        try:
            image_macro.module.make_image(all_integer_tile)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex}")
