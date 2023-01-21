# from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from terminal.pluglets.tile_grid.macro import TileGridMacroEnvironment
from unittest.mock import patch, MagicMock
import pytest


class TestTileGridPlugletSetup():

    @patch('terminal.pluglets.tile_grid.TileGridMacroEnvironment.get_chatter')
    def test_that_markup_filter_not_added_when_plugin_disabled(self, get_chatter):
        get_chatter.return_value = MagicMock()
        macro = TileGridMacroEnvironment()

        assert macro.jinja2_env is None
        assert macro.macro_config is None
        assert macro.chatter is None

        mkdocs_config = MkDocsConfig()
        filter_list = macro.create_jinja2_filters(mkdocs_config)
        assert len(filter_list) == 0

    @patch('terminal.pluglets.tile_grid.TileGridMacroEnvironment.get_chatter')
    @pytest.mark.parametrize("plugin_name", [
        pytest.param(
            "md-to-html", id="implicit-theme-namespace"
        ),
        pytest.param(
            "terminal/md-to-html", id="explicit-theme-namespace"
        )
    ])
    # NOTE: the order of the inputs passed to the test is important here
    # the patched mock needs to come before the pytest param
    # see https://github.com/hackebrot/pytest-tricks/issues/32
    def test_that_markup_filter_added_when_plugin_enabled(self, get_chatter, plugin_name):
        get_chatter.return_value = MagicMock()
        macro = TileGridMacroEnvironment()

        assert macro.jinja2_env is None
        assert macro.macro_config is None
        assert macro.chatter is None

        mkdocs_config = MkDocsConfig()
        mkdocs_config.plugins = [plugin_name]
        filter_list = macro.create_jinja2_filters(mkdocs_config)
        assert len(filter_list) == 1
        filter = filter_list[0]
        filter_name = filter["name"]
        assert "markup" == filter_name
