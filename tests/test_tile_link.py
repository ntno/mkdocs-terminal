import pytest
from tests.utils.tile import Tile


class TestTileLinkHelper():

    def test_helper_with_minimal_link_only_tile(self, env, filesystem_terminal_loader):
        env.loader = filesystem_terminal_loader
        tile_link_macro = env.get_template("macros/tile-link.j2")

        t = Tile(link_href="https://example.com")
        rendered_link_start = tile_link_macro.module.make_link_start(t)
        assert t.link_href in rendered_link_start
