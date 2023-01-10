from pathlib import Path
from jinja2 import loaders
from jinja2.environment import Environment
import mkdocs.utils.filters
import pytest
from tests.tile import Tile
from tests import defaults 

@pytest.fixture
def env():
    """returns a new environment with mkdocs url filter."""
    env = Environment()
    env.filters['url'] = mkdocs.utils.filters.url_filter
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
def empty_tile():
    """returns an empty tile"""
    return Tile()


@pytest.fixture
def minimal_link_tile():
    """returns a minimal link only title"""
    return Tile(link_href=defaults.github_link_href)


@pytest.fixture
def minimal_image_tile():
    return Tile(img_src=defaults.github_img_src)


@pytest.fixture
def minimal_linked_image_tile():
    return Tile(link_href=defaults.github_link_href, img_src=defaults.github_img_src)


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