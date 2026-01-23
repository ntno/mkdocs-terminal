from pathlib import Path
from jinja2 import loaders
from jinja2.environment import Environment
from tests.interface.tile import Tile
from tests.interface.theme_features import DEFAULT_PALETTES
from tests import defaults
from tests.utils.filters import mock_url_filter, mock_markup_filter
from tests.accessibility.utils import extract_css_attributes
from terminal.plugins.md_to_html.plugin import DEFAULT_MARKUP_FILTER_NAME
from terminal.pluglets.tile_grid.macro import TileGridMacroEnvironment
from unittest.mock import MagicMock, PropertyMock
import pytest
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import get_navigation
from tests.integration_helper import load_config
import yaml
from mkdocs.commands.build import build


@pytest.fixture
def env():
    """returns a new environment with mock mkdocs url filter."""
    env = Environment()
    env.filters['url'] = mock_url_filter
    env.filters[DEFAULT_MARKUP_FILTER_NAME] = mock_markup_filter
    env.add_extension('jinja2.ext.i18n')
    env.install_null_translations()
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
    return Tile(caption=0, img_src=1, link_href=2, alt_text=3, tooltip=4, tile_id=5, tile_css=6)


@pytest.fixture
def valid_link_only_tile():
    return Tile(caption=defaults.GITHUB_CAPTION, tile_id="myGitHubLinkTile", tile_css="myGitHubTileClass", alt_text=defaults.GITHUB_LINK_TEXT, link_href=defaults.GITHUB_LINK_HREF, tooltip=defaults.GITHUB_LINK_TOOLTIP)


@pytest.fixture
def valid_image_only_tile():
    return Tile(caption=defaults.GITHUB_CAPTION, tile_id="myGitHubLinkTile", tile_css="myGitHubTileClass", alt_text=defaults.GITHUB_IMG_ONLY_DESCRIPTION, img_src=defaults.GITHUB_IMG_SRC, tooltip=defaults.GITHUB_IMG_ONLY_TOOLTIP)


@pytest.fixture
def valid_linked_image_tile():
    return Tile(caption=defaults.GITHUB_CAPTION, tile_id="myGitHubLinkTile", tile_css="myGitHubTileClass", alt_text=defaults.GITHUB_LINK_TEXT, link_href=defaults.GITHUB_LINK_HREF, tooltip=defaults.GITHUB_LINK_TOOLTIP, img_src=defaults.GITHUB_IMG_SRC)


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


@pytest.fixture
def empty_nav():
    nav_cfg = []
    return build_flat_site_navigation_from_config(nav_cfg)


@pytest.fixture
def flat_nav():
    nav_cfg = [
        {'Home': 'index.md'},
        {'About': 'about.md'},
    ]
    return build_flat_site_navigation_from_config(nav_cfg)


@pytest.fixture
def nest_one_nav():
    nav_cfg = [
        {'Home': 'index.md'},
        {
            'API Guide': [
                {'Running': 'api-guide/running.md'},
                {'Testing': 'api-guide/testing.md'},
                {'Debugging': 'api-guide/debugging.md'},
            ]
        },
        {
            'About': [
                {'Release notes': 'about/release-notes.md'},
                {'License': 'about/license.md'},
            ]
        },
    ]
    cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
    fs = [
        'index.md',
        'api-guide/running.md',
        'api-guide/testing.md',
        'api-guide/debugging.md',
        'about/release-notes.md',
        'about/license.md',
    ]
    files = Files([File(s, cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls) for s in fs])
    return get_navigation(files, cfg)


@pytest.fixture
def nest_two_nav():
    nav_cfg = [
        {'Home': 'index.md'},
        {
            'API Guide': [
                {'Running': 'api-guide/running.md'},
                {'Testing': 'api-guide/testing.md'},
                {'Debugging': 'api-guide/debugging.md'},
                {
                    'Advanced': [
                        {'Part 1': 'api-guide/advanced/part-1.md'},
                    ]
                },
            ]
        },
        {
            'About': [
                {'Release notes': 'about/release-notes.md'},
                {'License': 'about/license.md'},
            ]
        },
    ]
    cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
    fs = [
        'index.md',
        'api-guide/running.md',
        'api-guide/testing.md',
        'api-guide/debugging.md',
        'api-guide/advanced/part-1.md',
        'about/release-notes.md',
        'about/license.md',
    ]
    files = Files([File(s, cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls) for s in fs])
    return get_navigation(files, cfg)


@pytest.fixture
def nest_three_nav():
    nav_cfg = [
        {'Home': 'index.md'},
        {
            'API Guide': [
                {'Running': 'api-guide/running.md'},
                {'Testing': 'api-guide/testing.md'},
                {'Debugging': 'api-guide/debugging.md'},
                {
                    'Advanced': [
                        {'Part 1': 'api-guide/advanced/part-1.md'},
                    ]
                },
            ]
        },
        {
            'Release notes': [
                {'Index': 'about/release-notes/index.md'},
                {'v1.0': [
                    {'Changelog': 'about/release-notes/v1.0.md'},
                ]},
                {'v2.0': [
                    {'Changelog': 'about/release-notes/v2.0.md'},
                ]},
            ]
        },
    ]
    cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
    fs = [
        'index.md',
        'api-guide/running.md',
        'api-guide/testing.md',
        'api-guide/debugging.md',
        'api-guide/advanced/part-1.md',
        'about/release-notes/index.md',
        'about/release-notes/v1.0.md',
        'about/release-notes/v2.0.md',

    ]
    files = Files([File(s, cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls) for s in fs])
    return get_navigation(files, cfg)


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


def build_flat_site_navigation_from_config(nav_cfg):
    cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
    fs = [
        File(list(item.values())[0], cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        for item in nav_cfg
    ]
    files = Files(fs)
    site_navigation = get_navigation(files, cfg)
    return site_navigation

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


@pytest.fixture(scope="session")
def built_example_site(tmp_path_factory, request):
    """Build any example site for testing.

    This fixture builds an example documentation site using the theme files
    from terminal/ to ensure tests validate against the actual theme code.

    The site name is extracted from the example site's mkdocs.yml file.

    Usage:
        def test_something(built_example_site):
            # Returns path to default minimal site

        # With parametrize to test different examples:
        @pytest.mark.parametrize("built_example_site", ["minimal", "demo"], indirect=True)
        def test_multiple_examples(built_example_site):
            # Runs test with both minimal and demo sites

    Args:
        request: pytest request object for parametrization support

    Returns:
        Path to the built site directory
    """

    # Allow parametrization to specify which example to build
    example_name = getattr(request, "param", "minimal")

    tmp_dir = tmp_path_factory.mktemp(f"built_{example_name}_site")
    example_dir = Path(__file__).parent / "examples" / example_name
    docs_dir = example_dir / "docs"
    theme_dir = Path(__file__).parent.parent / "terminal"

    if not docs_dir.exists():
        raise ValueError(f"Example site not found at {docs_dir}")

    # Extract site_name, plugins, and markdown_extensions from mkdocs.yml
    mkdocs_yml = example_dir / "mkdocs.yml"
    site_name = "Test Site"
    plugins = None
    markdown_extensions = None
    if mkdocs_yml.exists():
        with open(mkdocs_yml) as f:
            config_data = yaml.safe_load(f)
            if config_data:
                if "site_name" in config_data:
                    site_name = config_data["site_name"]
                if "plugins" in config_data:
                    plugins = config_data["plugins"]
                if "markdown_extensions" in config_data:
                    markdown_extensions = config_data["markdown_extensions"]

    config_kwargs = dict(
        docs_dir=str(docs_dir.resolve()),
        site_dir=str(tmp_dir.resolve()),
        site_name=site_name,
        theme={
            "name": None,
            "custom_dir": str(theme_dir.resolve())
        }
    )
    if plugins is not None:
        config_kwargs["plugins"] = plugins
    if markdown_extensions is not None:
        config_kwargs["markdown_extensions"] = markdown_extensions

    config = load_config(**config_kwargs)
    build(config)
    return tmp_dir


@pytest.fixture(scope="session")
def built_minimal_site(built_example_site):
    """Convenience fixture for the minimal example site.

    This is a simple wrapper around built_example_site for the minimal example.
    """
    return built_example_site

@pytest.fixture(scope="session")
def built_demo_site(built_example_site):
    """Convenience fixture for the demo example site.

    This is a simple wrapper around built_example_site for the demo example.
    """
    return built_example_site


@pytest.fixture(scope="session")
def built_example_site_with_palette(tmp_path_factory, request):
    """Build an example site with a specific color palette.

    This fixture builds an example documentation site with a specified color palette
    to validate that all default palettes meet accessibility standards.

    Usage:
        @pytest.mark.parametrize("built_example_site_with_palette", [
            ("minimal", "default"),
            ("minimal", "dark"),
            ("minimal", "gruvbox_dark"),
        ], indirect=True)
        def test_all_palettes(built_example_site_with_palette):
            # Runs test with minimal site using each palette

    Args:
        tmp_path_factory: pytest fixture for temporary directory creation
        request: pytest request object for parametrization support
                 Expects request.param = (example_name, palette_name)

    Returns:
        Path to the built site directory
    """
    # Extract example name and palette from parametrize
    example_name, palette_name = getattr(request, "param", ("minimal", "default"))

    # Create temp directory with descriptive name
    tmp_dir = tmp_path_factory.mktemp(f"built_{example_name}_{palette_name}_site")
    example_dir = Path(__file__).parent / "examples" / example_name
    docs_dir = example_dir / "docs"
    theme_dir = Path(__file__).parent.parent / "terminal"

    if not docs_dir.exists():
        raise ValueError(f"Example site not found at {docs_dir}")

    # Extract site_name, plugins, and markdown_extensions from mkdocs.yml
    mkdocs_yml = example_dir / "mkdocs.yml"
    site_name = "Test Site"
    plugins = None
    markdown_extensions = None
    if mkdocs_yml.exists():
        with open(mkdocs_yml) as f:
            config_data = yaml.safe_load(f)
            if config_data:
                if "site_name" in config_data:
                    site_name = config_data["site_name"]
                if "plugins" in config_data:
                    plugins = config_data["plugins"]
                if "markdown_extensions" in config_data:
                    markdown_extensions = config_data["markdown_extensions"]

    # Build config with palette setting
    theme_config = {
        "name": None,
        "custom_dir": str(theme_dir.resolve()),
        "palette": palette_name
    }

    config_kwargs = dict(
        docs_dir=str(docs_dir.resolve()),
        site_dir=str(tmp_dir.resolve()),
        site_name=site_name,
        theme=theme_config
    )
    if plugins is not None:
        config_kwargs["plugins"] = plugins
    if markdown_extensions is not None:
        config_kwargs["markdown_extensions"] = markdown_extensions

    config = load_config(**config_kwargs)
    build(config)
    return tmp_dir


@pytest.fixture
def palette_css_attributes(request):
    """Extract CSS attributes for a given palette.

    Returns a map of extracted CSS values for the specified palette by reading
    the palette CSS file and the fallback terminal.css file, then calling
    extract_css_attributes with both.

    Args:
        request: pytest request object for parametrization support
                 Expects request.param = palette_name (string)

    Returns:
        Dictionary mapping CSS attribute names to their resolved values

    Raises:
        ValueError: If the palette name is not in DEFAULT_PALETTES
    """
    palette_name = getattr(request, "param", "default")

    # Validate palette name
    if palette_name not in DEFAULT_PALETTES:
        raise ValueError(f"Palette '{palette_name}' not found in DEFAULT_PALETTES. Valid palettes: {DEFAULT_PALETTES}")

    # Get paths to CSS files
    project_dir = Path(__file__).parent.parent.resolve()
    palette_css_path = project_dir / "terminal" / "css" / "palettes" / f"{palette_name}.css"
    fallback_css_path = project_dir / "terminal" / "css" / "terminal.css"

    # Read CSS files
    if not palette_css_path.exists():
        raise FileNotFoundError(f"Palette CSS file not found: {palette_css_path}")
    if not fallback_css_path.exists():
        raise FileNotFoundError(f"Fallback CSS file not found: {fallback_css_path}")

    with open(palette_css_path, 'r') as f:
        palette_content = f.read()

    with open(fallback_css_path, 'r') as f:
        fallback_content = f.read()

    # Extract and return CSS attributes
    return extract_css_attributes(palette_content, fallback_content)
