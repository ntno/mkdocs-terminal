
from tests.utils.html import assert_valid_html, strip_whitespace
import tests.interface.theme_features as theme_features
import pytest

DEFAULT_CONFIG = {
    "theme": {
        "name": "terminal",
        "features": [],
    },
    "extra":{}
} 


@pytest.fixture
def side_nav_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/side-nav/side-nav.html")


class TestSideNav():
    def test_empty_side_nav(self, empty_nav, side_nav_partial):
        site_navigation = empty_nav
        enabled_context = {
            "nav": site_navigation,
            "config": DEFAULT_CONFIG
        }
        rendered_side_nav = side_nav_partial.render(enabled_context)
        print(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert "<nav> </nav>" in stripped_side_nav


    def test_flat_nav_entries_styled_as_simple_links(self, flat_nav, side_nav_partial):
        expected_style = "terminal-mkdocs-side-nav-item"
        site_navigation=flat_nav
        enabled_context = {
            "nav": site_navigation,
            "config": DEFAULT_CONFIG
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
        site_navigation = flat_nav
        enabled_context = {
            "nav": site_navigation,
            "config": DEFAULT_CONFIG
        }
                
        site_navigation.items[1].active = True  # Mark 'About' as active
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert format("<a class=\"%s\" href=\"mocked_url_path/\">Home</a>" % default_style) in stripped_side_nav
        assert format("<span class=\"%s\">About</span>" % active_style) in stripped_side_nav

    # a section with children but without an index should be styled as a span
    def test_nest_without_index_styled_as_section_span(self, nest_one_nav, side_nav_partial):
        expected_style = "terminal-mkdocs-side-nav-item terminal-mkdocs-side-nav-section-no-index"
        site_navigation = nest_one_nav
        enabled_context = {
            "nav": site_navigation,
            "config": DEFAULT_CONFIG
        }
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
  
        # TODO - there is a whitespace bug that inserts a leading space before the expected class in some cases
        assert format("<span class=\" %s\">About</span>" % expected_style) in stripped_side_nav
        assert format("<span class=\" %s\">API Guide</span>" % expected_style) in stripped_side_nav

    # a section with children but without an index should be styled as an activated span when its child is active
    def test_nest_without_index_styled_active_when_child_active(self, nest_one_nav, side_nav_partial):
        default_style = "terminal-mkdocs-side-nav-item terminal-mkdocs-side-nav-section-no-index"
        active_style = "terminal-mkdocs-side-nav-item--active terminal-mkdocs-side-nav-section-no-index"
        active_child_style = "terminal-mkdocs-side-nav-item--active"
        site_navigation = nest_one_nav
        enabled_context = {
            "nav": site_navigation,
            "config": DEFAULT_CONFIG
        }
        # Mark 'Debugging' as active
        site_navigation.items[1].children[2].active = True
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)

        # TODO - there is a whitespace bug that inserts a leading space before the expected class in some cases
        assert format("<span class=\" %s\">About</span>" % default_style) in stripped_side_nav
        assert format("<span class=\" %s\">API Guide</span>" % active_style) in stripped_side_nav
        assert format("<span class=\"%s\">Debugging</span>" % active_child_style) in stripped_side_nav
    
    # the second level (API Guide > Advanced) is rendered but not the third level (API Guide > Advanced > Part 1)
    def test_second_level_nest_rendered_but_not_third_level(self, nest_two_nav, side_nav_partial):
        site_navigation = nest_two_nav
        enabled_context = {
            "nav": site_navigation,
            "config": DEFAULT_CONFIG
        }
        rendered_side_nav = side_nav_partial.render(enabled_context)
   
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        
        assert "Advanced" in stripped_side_nav
        assert "Part 1" not in stripped_side_nav
    
    
    # a section with children AND an index should be a link instead of a span
    def test_section_with_index_is_link(self, nest_three_nav, side_nav_partial):
        expected_section_index_style = "terminal-mkdocs-side-nav-item"
        site_navigation = nest_three_nav
        enabled_context = {
            "nav": site_navigation,
            "config":{
                "theme": {
                    "name": "terminal",
                    "features": [theme_features.SHOW_INDEX_SECTIONS]
                },
                "extra":{}
            }
        }
        
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert format("<a class=\"%s\" href=\"mocked_url_path/about/release-notes/\">Release notes</a>" % expected_section_index_style) in stripped_side_nav
        
    # a section with children AND an index should be styled as an active link when its child is active
    def test_section_with_index_styled_active_when_child_active(self, nest_three_nav, side_nav_partial):
        expected_section_index_style = "terminal-mkdocs-side-nav-item--active"
        site_navigation = nest_three_nav
        enabled_context = {
            "nav": site_navigation,
            "config":{
                "theme": {
                    "name": "terminal",
                    "features": [theme_features.SHOW_INDEX_SECTIONS]
                },
                "extra":{}
            }
        }
        
        site_navigation.items[2].children[1].active = True  # Mark 'v1.0' as active
        rendered_side_nav = side_nav_partial.render(enabled_context)
        assert_valid_html(rendered_side_nav)
        stripped_side_nav = strip_whitespace(rendered_side_nav)
        assert format("<a class=\"%s\" href=\"mocked_url_path/about/release-notes/\">Release notes</a>" % expected_section_index_style) in stripped_side_nav
