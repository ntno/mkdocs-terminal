from tests.interface import theme_features, page_features
from tests.utils.html import assert_valid_html
import pytest
from mkdocs.structure.files import File, Files, set_exclusions
from mkdocs.structure.nav import Section, _get_by_type, get_navigation
from mkdocs.structure.pages import Page
from tests.integration_base import dedent, load_config

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



class TestSideNav():
        def test_flat_nav_entries_styled_as_pages(self, flat_nav):
            site_navigation=flat_nav
           
            
            print(site_navigation)
            assert len(site_navigation.items) == 2
            assert len(site_navigation.pages) == 2
            assert repr(site_navigation.homepage) == "Page(title='Home', url='/')"
            assert 1 == 2
            # self.assertEqual(str(site_navigation).strip(), expected)
            # self.assertEqual(, 2)
            # self.assertEqual(len(site_navigation.pages), 2)
            # self.assertEqual(, )

    # def test_no_content_when_theme_feature_enabled(self, side_toc_partial, enabled_context):
    #     enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_SIDE_TOC]
    #     context_data = enabled_context
    #     rendered_side_toc = side_toc_partial.render(context_data)
    #     assert rendered_side_toc == ""

    # def test_no_content_when_page_feature_enabled(self, side_toc_partial, enabled_context):
    #     enabled_context["page"]["meta"]["hide"] = [page_features.HIDE_SIDE_TOC_ON_PAGE]
    #     context_data = enabled_context
    #     rendered_side_toc = side_toc_partial.render(context_data)
    #     assert rendered_side_toc == ""

    # def test_no_entries_when_page_has_no_headers(self, side_toc_partial, enabled_context):
    #     enabled_context["page"]["toc"] = []
    #     context_data = enabled_context
    #     rendered_side_toc = side_toc_partial.render(context_data)
    #     assert rendered_side_toc == ""

    # def test_has_entries_when_page_has_headers(self, side_toc_partial, enabled_context):
    #     context_data = enabled_context
    #     rendered_side_toc = side_toc_partial.render(context_data)
    #     assert "<a href=\"anchor_to_first_header_placeholder\">first_header_placeholder</a>" in rendered_side_toc
    #     assert "<a href=\"anchor_to_child_header_placeholder\">child_header_placeholder</a>" in rendered_side_toc
    #     assert_valid_html(rendered_side_toc)
