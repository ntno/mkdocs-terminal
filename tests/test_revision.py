from tests.utils.html import assert_valid_html
import pytest


class TestRevision():
    def test_that_revision_renders_when_no_page_meta(self, env_with_terminal_loader):
        revision_partial = env_with_terminal_loader.get_template("partials/revision.html")
        context_data = {
            "page": {},
            "config": {}
        }
        try:
            revision_partial.render(context_data)
        except Exception as ex:
            pytest.fail(f"Got exception during render: {ex})")

    def test_that_no_last_updated_text_when_no_revision_date(self, env_with_terminal_loader):
        revision_partial = env_with_terminal_loader.get_template("partials/revision.html")
        context_data = {
            "page": {
                "meta": {}
            },
            "config": {}
        }
        rendered_revision = revision_partial.render(context_data)
        assert rendered_revision.strip() == ""

    def test_that_last_updated_text_when_page_has_revision_date(self, env_with_terminal_loader):
        revision_partial = env_with_terminal_loader.get_template("partials/revision.html")
        context_data = {
            "page": {
                "meta": {
                    "revision_date": "2023/01/01"
                }
            },
            "config": {}
        }
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/01/01" in rendered_revision
        assert_valid_html(rendered_revision)

    def test_that_github_history_link_added_when_site_has_page_edit_url_and_repo_name_set(self, env_with_terminal_loader):
        revision_partial = env_with_terminal_loader.get_template("partials/revision.html")
        mkdocs_generated_page_url = "https://github.com/myUsername/myRepository/edit/main/docs/index.md"
        expected_page_history_url = "https://github.com/myUsername/myRepository/commits/main/docs/index.md"
        mkdocs_generated_repo_name = "GitHub"
        context_data = {
            "page": {
                "edit_url": mkdocs_generated_page_url,
                "meta": {
                    "revision_date": "2023/01/02"
                }
            },
            "config": {
                "repo_name": mkdocs_generated_repo_name
            }
        }
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/01/02" in rendered_revision
        assert "See revision history on" in rendered_revision
        assert "<a target=\"_blank\" href=\"" + expected_page_history_url + "\">GitHub</a>" in rendered_revision
        assert_valid_html(rendered_revision)

    def test_that_bitbucket_source_link_added_when_site_has_page_edit_url_and_repo_name_set(self, env_with_terminal_loader):
        revision_partial = env_with_terminal_loader.get_template("partials/revision.html")
        mkdocs_generated_page_url = "https://bitbucket.org/myUsername/myRepository/src/main/docs/index.md?mode=edit"
        expected_page_source_url = "https://bitbucket.org/myUsername/myRepository/src/main/docs/index.md?mode=read"
        mkdocs_generated_repo_name = "Bitbucket"
        context_data = {
            "page": {
                "edit_url": mkdocs_generated_page_url,
                "meta": {
                    "revision_date": "2023/03/04"
                }
            },
            "config": {
                "repo_name": mkdocs_generated_repo_name
            }
        }
        rendered_revision = revision_partial.render(context_data)
        assert "Page last updated 2023/03/04" in rendered_revision
        assert "See revision history on" in rendered_revision
        assert "<a target=\"_blank\" href=\"" + expected_page_source_url + "\">Bitbucket</a>" in rendered_revision
        assert_valid_html(rendered_revision)
