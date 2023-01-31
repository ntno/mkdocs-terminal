from tests import defaults
from tests.interface import theme_pluglets
import pytest


@pytest.fixture
def tile_link_macro(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("pluglets/tile_grid/templates/j2-macros/tile-link.j2")


class TestTileLinkHelper():

    def test_that_link_start_contains_href_with_minimal_link_only_tile(self, tile_link_macro, minimal_link_tile):
        rendered_link_start = tile_link_macro.module.make_link_start(minimal_link_tile)
        assert defaults.GITHUB_LINK_HREF in rendered_link_start
        assert theme_pluglets.TILE_LINK_START_TAG in rendered_link_start

    def test_that_link_start_fragment_renders_with_integer_inputs(self, tile_link_macro, all_integer_tile):
        try:
            tile_link_macro.module.make_link_start(all_integer_tile)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
