from pathlib import Path
from jinja2 import loaders
from jinja2.environment import Environment
from tests.interface.tile import Tile
from tests import defaults
from tests.utils.filters import mock_url_filter
import pytest


@pytest.fixture
def env():
    """returns a new environment with mock mkdocs url filter."""
    env = Environment()
    env.filters['url'] = mock_url_filter
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


@pytest.fixture
def top_menu_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/top-nav/menu.html")


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
