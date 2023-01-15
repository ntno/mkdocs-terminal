from tests.utils.html import assert_valid_html
from tests.utils import theme_features, theme_plugins
import pytest


@pytest.fixture
def revision_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template("partials/revision.html")


@pytest.fixture
def fully_enabled_context():
    context = {
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
    return context


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

    def test_no_content_when_theme_features_disabled(self, revision_partial):
        context_data = {
            "page": {
                "meta": {
                    "revision_date": "2023/04/01"
                }
            },
            "config": {
                "plugins": [theme_plugins.REVISION],
                "theme": {
                    "features": []
                }
            }
        }
        rendered_revision = revision_partial.render(context_data)
        assert rendered_revision.strip() == ""

    def test_that_revision_renders_when_no_page_meta(self, revision_partial):
        context_data = {
            "page": {},
            "config": {
                "theme": {}
            }
        }
        try:
            revision_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_that_no_last_updated_text_when_no_revision_date(self, revision_partial):
        context_data = {
            "page": {
                "meta": {}
            },
            "config": {
                "theme": {}
            }
        }
        rendered_revision = revision_partial.render(context_data)
        assert rendered_revision.strip() == ""

    def test_that_last_updated_text_when_page_has_revision_date(self, revision_partial, fully_enabled_context):
        fully_enabled_context["page"]["meta"]["revision_date"] = "2023/01/01"
        context_data = fully_enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/01/01. " in rendered_revision
        assert_valid_html(rendered_revision)

    def test_that_github_history_link_added_when_site_has_page_edit_url_and_repo_name_set(self,revision_partial, fully_enabled_context):
        mkdocs_generated_page_url = "https://github.com/myUsername/myRepository/edit/main/docs/index.md"
        expected_page_history_url = "https://github.com/myUsername/myRepository/commits/main/docs/index.md"
        mkdocs_generated_repo_name = "GitHub"
        fully_enabled_context["page"]["meta"]["revision_date"] = "2023/01/02"
        fully_enabled_context["page"]["edit_url"] = mkdocs_generated_page_url
        fully_enabled_context["config"]["repo_name"] = mkdocs_generated_repo_name
        context_data = fully_enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/01/02. See revision history on" in rendered_revision
        assert "<a target=\"_blank\" href=\"" + expected_page_history_url + "\">GitHub</a>" in rendered_revision
        assert_valid_html(rendered_revision)

    def test_that_bitbucket_source_link_added_when_site_has_page_edit_url_and_repo_name_set(self, revision_partial, fully_enabled_context):
        mkdocs_generated_page_url = "https://bitbucket.org/myUsername/myRepository/src/main/docs/index.md?mode=edit"
        expected_page_source_url = "https://bitbucket.org/myUsername/myRepository/src/main/docs/index.md?mode=read"
        mkdocs_generated_repo_name = "Bitbucket"
        fully_enabled_context["page"]["meta"]["revision_date"] = "2023/03/04"
        fully_enabled_context["page"]["edit_url"] = mkdocs_generated_page_url
        fully_enabled_context["config"]["repo_name"] = mkdocs_generated_repo_name
        context_data = fully_enabled_context
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/03/04. See revision history on" in rendered_revision
        assert "<a target=\"_blank\" href=\"" + expected_page_source_url + "\">Bitbucket</a>" in rendered_revision
        assert_valid_html(rendered_revision)
