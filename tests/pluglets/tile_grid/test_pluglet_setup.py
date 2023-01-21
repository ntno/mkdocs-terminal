from terminal.pluglets.tile_grid.macro import TileGridMacroEnvironment
from unittest.mock import patch, MagicMock, PropertyMock
from tests.interface import theme_plugins
import pytest


def make_mkdocs_config_property_mocks(plugin_list=[]):
    properties = {}
    properties["plugins"] = PropertyMock(return_value=plugin_list)
    properties["markdown_extensions"] = PropertyMock(return_value=[])
    properties["mdx_configs"] = PropertyMock(return_value={})
    return properties


def make_mock_mkdocs_config(mock_properties):
    mkdocs_config = MagicMock()
    type(mkdocs_config).plugins = mock_properties["plugins"]
    type(mkdocs_config).markdown_extensions = mock_properties["markdown_extensions"]
    type(mkdocs_config).mdx_configs = mock_properties["mdx_configs"]
    return mkdocs_config


@pytest.fixture
def mkdocs_config_property_mocks():
    return make_mkdocs_config_property_mocks()


@pytest.fixture
def mock_mkdocs_config(mkdocs_config_property_mocks):
    return make_mock_mkdocs_config(mkdocs_config_property_mocks)


class TestPlugletSetup():

    @patch('terminal.pluglets.tile_grid.main.TileGridMacroEnvironment.get_chatter')
    def test_that_markup_filter_not_added_when_plugin_disabled(self, get_chatter, mock_mkdocs_config, mkdocs_config_property_mocks):
        get_chatter.return_value = MagicMock()
        macro = TileGridMacroEnvironment()

        assert macro.jinja2_env is None
        assert macro.macro_config is None
        assert macro.chatter is None

        filter_list = macro.create_jinja2_filters(mock_mkdocs_config)
        assert len(filter_list) == 0
        mkdocs_config_property_mocks["plugins"].assert_called()

    @patch('terminal.pluglets.tile_grid.main.TileGridMacroEnvironment.get_chatter')
    @pytest.mark.parametrize("plugin_name", [
        pytest.param(
            theme_plugins.MD_TO_HTML_IMPLICIT, id="implicit-theme-namespace"
        ),
        pytest.param(
            theme_plugins.MD_TO_HTML_EXPLICIT, id="explicit-theme-namespace"
        )
    ])
    # NOTE: the order of the inputs passed to the test is important here
    # the patched mock needs to come before the pytest param
    # see https://github.com/hackebrot/pytest-tricks/issues/32
    def test_that_markup_filter_added_when_plugin_enabled(self, get_chatter, plugin_name):
        mkdocs_config_property_mocks = make_mkdocs_config_property_mocks(plugin_list=[plugin_name])
        mock_mkdoc_config = make_mock_mkdocs_config(mkdocs_config_property_mocks)

        get_chatter.return_value = MagicMock()
        macro = TileGridMacroEnvironment()

        assert macro.jinja2_env is None
        assert macro.macro_config is None
        assert macro.chatter is None

        filter_list = macro.create_jinja2_filters(mock_mkdoc_config)
        assert len(filter_list) == 1
        assert theme_plugins.DEFAULT_MARKUP_FILTER_NAME == filter_list[0]["name"]
        mkdocs_config_property_mocks["plugins"].assert_called()
        mkdocs_config_property_mocks["markdown_extensions"].assert_called()
        mkdocs_config_property_mocks["mdx_configs"].assert_called()
