from tests.interface import theme_features, page_features
from tests.utils.html import assert_valid_html
import pytest


@pytest.fixture
def enabled_context():
    toc_list = [
         {
            "title": "first_header_placeholder",
            "level": 0,
            "children": [
                {
                    "title": "child_header_placeholder",
                    "level": 1,
                    "url": "anchor_to_child_placeholder"
                }
            ],
            "url": "anchor_to_first_header_placeholder"
        }
    ]
    return {
        "page": {
            "toc": toc_list,
            "content": "page_conent_placeholder",
            "meta": {
                "hide": []
            }
        },
        "config": {
            "theme": {
                "features": []
            }
        }
    }


@pytest.fixture
def side_toc_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/side-panel/side-toc.html")


class TestSideToc():
    def test_no_content_when_theme_feature_enabled(self, side_toc_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_SIDE_TOC]
        context_data = enabled_context
        rendered_side_toc = side_toc_partial.render(context_data)
        assert rendered_side_toc == ""

    def test_no_content_when_page_feature_enabled(self, side_toc_partial, enabled_context):
        enabled_context["page"]["meta"]["hide"] = [page_features.HIDE_SIDE_TOC_ON_PAGE]
        context_data = enabled_context
        rendered_side_toc = side_toc_partial.render(context_data)
        assert rendered_side_toc == ""

    def test_no_entries_when_page_has_no_headers(self, side_toc_partial, enabled_context):
        enabled_context["page"]["toc"] = []
        context_data = enabled_context
        rendered_side_toc = side_toc_partial.render(context_data)
        assert rendered_side_toc == ""

    def test_has_entries_when_page_has_headers(self, side_toc_partial, enabled_context):
        context_data = enabled_context
        rendered_side_toc = side_toc_partial.render(context_data)
        assert "<a href=\"anchor_to_first_header_placeholder\">first_header_placeholder</a>" in rendered_side_toc
        assert_valid_html(rendered_side_toc)