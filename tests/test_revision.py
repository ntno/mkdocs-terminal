from tests.utils.html import assert_valid_html
from tests.utils import theme_features, theme_plugins
import pytest


@pytest.fixture
def revision_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/revision.html")


@pytest.fixture
def enabled_context():
    return {
        "page": {
            "edit_url": "edit_url_placeholder",
            "meta": {
                "revision_date": "revision_date_placeholder"
            }
        },
        "config": {
            "repo_name": "repo_name_placeholder",
            "repo_url": "repo_url_placeholder",
            "plugins": [theme_plugins.REVISION],
            "theme": {
                "features": [theme_features.SHOW_REVISION_DATE, theme_features.SHOW_REVISION_HISTORY]
            }
        }
    }


class TestRevision():
    @pytest.mark.parametrize("plugins_list", [
        pytest.param(
            None, id="null_plugins_list"
        ),
        pytest.param(
            [], id="empty_plugins_list"
        ),
        pytest.param(
            [theme_plugins.SEARCH], id="missing_plugin"
        )
    ])
    def test_no_content_when_plugin_disabled(self, revision_partial, plugins_list):
        context_data = {
            "page": {
                "meta": {
                    "revision_date": "2023/04/01"
                }
            },
            "config": {
                "plugins": plugins_list,
                "theme": {
                    "features": [theme_features.SHOW_REVISION_DATE, theme_features.SHOW_REVISION_HISTORY]
                }
            }
        }
        rendered_revision = revision_partial.render(context_data)
        assert rendered_revision.strip() == ""

    def test_revision_renders_when_plugin_enabled(self, revision_partial):
        context_data = {
            "config": {
                "plugins": [theme_plugins.REVISION],
                "theme": {}
            }
        }
        try:
            revision_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_no_content_when_theme_features_disabled(self, revision_partial, enabled_context):
        enabled_context["config"]["theme"]["features"] = []
        context_data = enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert rendered_revision.strip() == ""


    @pytest.mark.parametrize("mkdocs_context", [
        pytest.param(
            {
                "page": {},
                "config": {
                    "theme": {}
                }
            }, id="no_page_meta"
        ),
        pytest.param(
            {
                "page": {
                    "meta": {}    
                },
                "config": {
                    "theme": {}
                }
            }, id="empty_page_meta"
        )
    ])
    def test_that_revision_renders_when_missing_context_attributes(self, revision_partial, mkdocs_context):
        try:
            rendered_revision = revision_partial.render(mkdocs_context)
            assert rendered_revision.strip() == ""
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_last_updated_text_when_page_has_revision_date(self, revision_partial, enabled_context):
        enabled_context["page"]["meta"]["revision_date"] = "2023/01/01"
        context_data = enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/01/01. " in rendered_revision
        assert_valid_html(rendered_revision)

    def test_no_last_updated_text_when_missing_revision_date(self, revision_partial, enabled_context):
        enabled_context["page"]["meta"]["revision_date"] = ""
        context_data = enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated" not in rendered_revision
        assert_valid_html(rendered_revision)

    def test_github_history_link(self,revision_partial, enabled_context):
        expected_page_history_url = "https://github.com/myUsername/myRepository/commits/main/docs/index.md"
        enabled_context["page"]["meta"]["revision_date"] = "2022/05/06"
        enabled_context["page"]["edit_url"] = "https://github.com/myUsername/myRepository/edit/main/docs/index.md"
        enabled_context["config"]["repo_name"] = "GitHub"
        context_data = enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2022/05/06. See revision history on" in rendered_revision
        assert "<a target=\"_blank\" href=\"" + expected_page_history_url + "\">GitHub</a>" in rendered_revision
        assert_valid_html(rendered_revision)

    def test_bitbucket_history_link(self, revision_partial, enabled_context):
        expected_page_source_url = "https://bitbucket.org/myUsername/myRepository/src/main/docs/index.md?mode=read"
        enabled_context["page"]["meta"]["revision_date"] = "2023/03/04"
        enabled_context["page"]["edit_url"] = "https://bitbucket.org/myUsername/myRepository/src/main/docs/index.md?mode=edit"
        enabled_context["config"]["repo_name"] = "Bitbucket"
        context_data = enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/03/04. See revision history on" in rendered_revision
        assert "<a target=\"_blank\" href=\"" + expected_page_source_url + "\">Bitbucket</a>" in rendered_revision
        assert_valid_html(rendered_revision)
