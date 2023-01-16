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
                    "url": "anchor_to_child_header_placeholder"
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
# {%- if "navigation.side.hide" in features -%}{%- else -%}<hr>{%- endif -%}

@pytest.fixture
def side_panel_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/side-panel/side-panel.html")


class TestSidePanel():
    def test_no_content_when_theme_feature_enabled(self, side_panel_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_SIDE_NAV, theme_features.HIDE_SIDE_TOC]
        context_data = enabled_context
        rendered_side_panel = side_panel_partial.render(context_data)
        assert rendered_side_panel == ""

    def test_that_visual_break_between_side_nav_and_side_toc(self, side_panel_partial, enabled_context):
        pass

    