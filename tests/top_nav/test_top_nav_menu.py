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
def menu_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/top-nav/menu.html")


class TestTopNav():
    def test_no_page_links_when_nav_empty(self, menu_partial, enabled_context):
        pass

    def test_all_top_level_pages_included(self, menu_partial, enabled_context):
        pass
