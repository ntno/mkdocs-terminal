from tests.interface import theme_features, page_features
from tests.utils.html import assert_valid_html, strip_whitespace
import pytest
from mkdocs.structure.files import File, Files, set_exclusions
from mkdocs.structure.nav import Section, _get_by_type, get_navigation
from mkdocs.structure.pages import Page
from tests.integration_base import dedent, load_config


def build_flat_site_navigation_from_config(nav_cfg):
    cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
    fs = [
        File(list(item.values())[0], cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        for item in nav_cfg
    ]
    files = Files(fs)
    site_navigation = get_navigation(files, cfg)
    return site_navigation

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
def side_nav_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/side-nav/side-nav.html")

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


    def test_flat_nav_entries_styled_as_simple_links(self, flat_nav, side_nav_partial):
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
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert format("<a class=\"%s\" href=\"mocked_url_path/\">Home</a>" % default_style) in stripped_side_nav
        assert format("<span class=\"%s\">About</span>" % active_style) in stripped_side_nav

    def test_nest_without_index_styled_as_section_span(self, nest_one_nav, side_nav_partial):
        expected_style = "terminal-mkdocs-side-nav-item terminal-mkdocs-side-nav-section-no-index"
        site_navigation=nest_one_nav
        enabled_context = {
                "nav": site_navigation
        }
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
  
        #TODO - there is a whitespace bug that inserts a leading space before the expected class in some cases
        assert format("<span class=\" %s\">About</span>" % expected_style) in stripped_side_nav
        assert format("<span class=\" %s\">API Guide</span>" % expected_style) in stripped_side_nav

    def test_nest_without_index_styled_active_when_child_active(self, nest_one_nav, side_nav_partial):
        default_style = "terminal-mkdocs-side-nav-item terminal-mkdocs-side-nav-section-no-index"
        active_style = "terminal-mkdocs-side-nav-item--active terminal-mkdocs-side-nav-section-no-index"
        active_child_style = "terminal-mkdocs-side-nav-item--active"
        site_navigation=nest_one_nav
        enabled_context = {
                "nav": site_navigation
        }
        # Mark 'Debugging' as active
        site_navigation.items[1].children[2].active = True
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)

        #TODO - there is a whitespace bug that inserts a leading space before the expected class in some cases
        assert format("<span class=\" %s\">About</span>" % default_style) in stripped_side_nav
        assert format("<span class=\" %s\">API Guide</span>" % active_style) in stripped_side_nav
        assert format("<span class=\"%s\">Debugging</span>" % active_child_style) in stripped_side_nav