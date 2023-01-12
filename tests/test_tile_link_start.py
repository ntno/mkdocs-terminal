from tests import defaults
import pytest


class TestTileLinkHelper():

    def test_that_link_start_contains_href_with_minimal_link_only_tile(self, env_with_terminal_loader, minimal_link_tile):
        tile_link_macro = env_with_terminal_loader.get_template("macros/tile-link.j2")
        rendered_link_start = tile_link_macro.module.make_link_start(minimal_link_tile)
        assert defaults.GITHUB_LINK_HREF in rendered_link_start

    def test_that_link_start_fragment_renders_with_integer_inputs(self, env_with_terminal_loader, all_integer_tile):
        link_macro = env_with_terminal_loader.get_template("macros/tile-link.j2")
        try:
            link_macro.module.make_link_start(all_integer_tile)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")
