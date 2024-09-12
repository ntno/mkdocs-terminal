from tests.interface import theme_features, page_features
from tests.utils.html_utils import assert_valid_html
import pytest


@pytest.fixture
def enabled_context():
    nav_list = []
    return {
        "nav": nav_list,
        "page": {
            "meta": {
                "hide": []
            }
        },
        "config": {
            "site_name": "site_name_placeholder",
            "site_url": "site_url_placeholder",
            "theme": {
                "features": []
            }
        },
        "button_idx": len(nav_list)
    }


@pytest.fixture
def top_nav_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/top-nav/top.html")


class TestTopNav():
    def test_no_content_when_theme_feature_enabled(self, top_nav_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = [theme_features.HIDE_TOP_NAV]
        context_data = enabled_context
        rendered_top_nav = top_nav_partial.render(context_data)
        assert rendered_top_nav == ""

    def test_no_content_when_page_feature_enabled(self, top_nav_partial, enabled_context):
        enabled_context["page"]["meta"]["hide"] = [page_features.HIDE_TOP_NAV_ON_PAGE]
        context_data = enabled_context
        rendered_top_nav = top_nav_partial.render(context_data)
        assert rendered_top_nav == ""

    def test_home_link_is_forward_slash_when_no_site_url(self, top_nav_partial, enabled_context):
        enabled_context["config"]["site_url"] = None
        context_data = enabled_context
        rendered_top_nav = top_nav_partial.render(context_data)
        assert "<a href=\"/\" class=\"no-style\">site_name_placeholder</a>" in rendered_top_nav
        assert_valid_html(rendered_top_nav)

    def test_site_title_present_when_provided(self, top_nav_partial, enabled_context):
        enabled_context["config"]["site_name"] = "My Documentation"
        context_data = enabled_context
        rendered_top_nav = top_nav_partial.render(context_data)
        assert "My Documentation" in rendered_top_nav
        assert_valid_html(rendered_top_nav)

    def test_site_url_present_when_provided(self, top_nav_partial, enabled_context):
        enabled_context["config"]["site_url"] = "https://mydocs.com"
        enabled_context["config"]["site_name"] = "My Documentation"
        context_data = enabled_context
        rendered_top_nav = top_nav_partial.render(context_data)
        assert "<a href=\"https://mydocs.com\" class=\"no-style\">My Documentation</a>" in rendered_top_nav
        assert_valid_html(rendered_top_nav)
