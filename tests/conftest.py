from pathlib import Path
from jinja2 import loaders
from jinja2.environment import Environment
from tests.interface.tile import Tile
from tests import defaults
from tests.utils.filters import mock_url_filter, mock_markup_filter
from terminal.plugins.md_to_html.plugin import DEFAULT_MARKUP_FILTER_NAME
from terminal.pluglets.tile_grid.macro import TileGridMacroEnvironment
from unittest.mock import MagicMock, PropertyMock
import pytest


@pytest.fixture
def env():
    """returns a new environment with mock mkdocs url filter."""
    env = Environment()
    env.filters['url'] = mock_url_filter
    env.filters[DEFAULT_MARKUP_FILTER_NAME] = mock_markup_filter
    return env


@pytest.fixture
def filesystem_terminal_loader():
    """returns FileSystemLoader initialized to ../terminal directory"""
    here = Path(__file__)
    parent = here.parent
    project_folder = parent.parent.resolve()
    return loaders.FileSystemLoader(project_folder / "terminal")


@pytest.fixture
def env_with_terminal_loader(env, filesystem_terminal_loader):
    """returns environment with loader set to terminal file system loader"""
    env.loader = filesystem_terminal_loader
    return env


@pytest.fixture(autouse=True)
def reset_singletons():
    TileGridMacroEnvironment._instances = {}


@pytest.fixture
def empty_tile():
    """returns an empty tile"""
    return Tile()


@pytest.fixture
def minimal_link_tile():
    """returns a minimal link only title"""
    return Tile(link_href=defaults.GITHUB_LINK_HREF)


@pytest.fixture
def minimal_image_tile():
    return Tile(img_src=defaults.GITHUB_IMG_SRC)


@pytest.fixture
def minimal_linked_image_tile():
    return Tile(link_href=defaults.GITHUB_LINK_HREF, img_src=defaults.GITHUB_IMG_SRC)


@pytest.fixture
def all_integer_tile():
    return Tile(caption=0, tile_id=1, tile_css=2, link_text=3, link_href=4, link_title=5, link_target=6, img_src=7, img_alt=8, img_title=9, img_width=10, img_height=11)


@pytest.fixture
def valid_linked_image_tile():
    return Tile(caption=defaults.GITHUB_CAPTION, tile_id="myGitHubLinkTile", tile_css="myGitHubTileClass", link_text=defaults.GITHUB_LINK_TEXT, link_href=defaults.GITHUB_LINK_HREF, link_title=defaults.GITHUB_LINK_TITLE, link_target=defaults.GITHUB_LINK_TARGET, img_src=defaults.GITHUB_IMG_SRC, img_alt=defaults.GITHUB_IMG_ALT, img_title=defaults.GITHUB_IMG_TITLE, img_width=defaults.GITHUB_IMG_WIDTH, img_height=defaults.GITHUB_IMG_HEIGHT)


@pytest.fixture
def inactive_page_1_properties():
    return make_nav_object_property_mocks(False, "title_1", "url_1", False)


@pytest.fixture
def inactive_page_1(inactive_page_1_properties):
    return make_mock_nav_object(inactive_page_1_properties)


@pytest.fixture
def inactive_page_2_properties():
    return make_nav_object_property_mocks(False, "title_2", "url_2", False)


@pytest.fixture
def inactive_page_2(inactive_page_2_properties):
    return make_mock_nav_object(inactive_page_2_properties)


def make_nav_object_property_mocks(is_section_value, title_value, url_value, active_value):
    properties = {}
    properties["is_section"] = PropertyMock(return_value=is_section_value)
    properties["title"] = PropertyMock(return_value=title_value)
    properties["url"] = PropertyMock(return_value=url_value)
    properties["active"] = PropertyMock(return_value=active_value)
    return properties


def make_mock_nav_object(mock_properties):
    nav_object = MagicMock()
    type(nav_object).is_section = mock_properties["is_section"]
    type(nav_object).title = mock_properties["title"]
    type(nav_object).url = mock_properties["url"]
    type(nav_object).active = mock_properties["active"]
    return nav_object


# @pytest.fixture
# def dict_loader():
#     """returns DictLoader"""
#     return loaders.DictLoader({"justdict.html": "FOO"})


# @pytest.fixture
# def package_loader():
#     """returns PackageLoader initialized from templates"""
#     return loaders.PackageLoader("res", "templates")


# @pytest.fixture
# def filesystem_loader():
#     """returns FileSystemLoader initialized to res/templates directory"""
#     here = Path(__file__).parent.resolve()
#     return loaders.FileSystemLoader(here / "res" / "templates")


# @pytest.fixture
# def function_loader():
#     """returns a FunctionLoader"""
#     return loaders.FunctionLoader({"justfunction.html": "FOO"}.get)


# @pytest.fixture
# def choice_loader(dict_loader, package_loader):
#     """returns a ChoiceLoader"""
#     return loaders.ChoiceLoader([dict_loader, package_loader])


# @pytest.fixture
# def prefix_loader(filesystem_loader, dict_loader):
#     """returns a PrefixLoader"""
#     return loaders.PrefixLoader({"a": filesystem_loader, "b": dict_loader})
