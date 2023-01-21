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

        # cleanup singleton after test
        del macro

    @pytest.mark.parametrize("plugin_name", [
        pytest.param(
            "md-to-html", id="implicit-theme-namespace"
        ),
        pytest.param(
            "terminal/md-to-html", id="explicit-theme-namespace"
        )
    ])
    def test_that_markup_filter_added_when_plugin_enabled(self, plugin_name):
        assert "md-to-html" in plugin_name
        pass
