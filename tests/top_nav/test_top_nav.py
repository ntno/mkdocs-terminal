import pytest


@pytest.fixture
def enabled_context():
    nav_list = []
    return {
        "nav": nav_list,
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
        pass

    def test_no_content_when_page_feature_enabled(self, top_nav_partial, enabled_context):
        pass

    def test_no_site_title_when_missing(self, top_nav_partial, enabled_context):
        pass

    def test_site_title_present_when_provided(self, top_nav_partial, enabled_context):
        pass
