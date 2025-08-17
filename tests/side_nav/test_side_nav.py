from tests.interface import theme_features, page_features
from tests.utils.html import assert_valid_html, strip_whitespace
import pytest
from mkdocs.structure.files import File, Files, set_exclusions
from mkdocs.structure.nav import Section, _get_by_type, get_navigation
from mkdocs.structure.pages import Page
from tests.integration_base import dedent, load_config


@pytest.fixture
def side_nav_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/side-nav/side-nav.html")


def build_site_navigation_from_config(nav_cfg):
    cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
    fs = [
        File(list(item.values())[0], cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        for item in nav_cfg
    ]
    files = Files(fs)
    site_navigation = get_navigation(files, cfg)
    return site_navigation

@pytest.fixture
def flat_nav():
    nav_cfg = [
            {'Home': 'index.md'},
            {'About': 'about.md'},
        ]
    return build_site_navigation_from_config(nav_cfg)

@pytest.fixture
def empty_nav():
    nav_cfg = []
    return build_site_navigation_from_config(nav_cfg)


class TestSideNav():
    def test_empty_side_nav(self, empty_nav, side_nav_partial):
        site_navigation=empty_nav
        enabled_context = {
                "nav": site_navigation
        }
        rendered_side_nav = side_nav_partial.render(enabled_context)
        print(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert "<nav> </nav>" in stripped_side_nav


    def test_flat_nav_entries_styled_as_simple_nav_items(self, flat_nav, side_nav_partial):
        expected_style = "terminal-mkdocs-side-nav-item"
        site_navigation=flat_nav
        enabled_context = {
                "nav": site_navigation
        }
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert format("<a class=\"%s\" href=\"mocked_url_path/\">Home</a>" % expected_style) in stripped_side_nav
        assert format("<a class=\"%s\" href=\"mocked_url_path/about/\">About</a>" % expected_style) in stripped_side_nav

    # if a flat nav entry is active, it should be a span instead of a link
    def test_active_flat_nav_entry_styled_as_span(self, flat_nav, side_nav_partial):
        default_style = "terminal-mkdocs-side-nav-item"
        active_style = "terminal-mkdocs-side-nav-item--active"
        site_navigation=flat_nav
        enabled_context = {
                "nav": site_navigation
        }
        site_navigation.items[1].active = True  # Mark 'About' as active
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        print(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert format("<a class=\"%s\" href=\"mocked_url_path/\">Home</a>" % default_style) in stripped_side_nav
        assert format("<span class=\"%s\">About</span>" % active_style) in stripped_side_nav
