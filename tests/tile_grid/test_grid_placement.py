# from tests.utils.html import assert_valid_html
# from tests.utils.filters import mock_markup_filter
# from tests.interface import theme_plugins
import pytest
PAGE_BASE_PARTIAL_PATH = "partials/page-base.html"


@pytest.fixture
def page_base_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(PAGE_BASE_PARTIAL_PATH)


class TestGridPlacement():

    def test_that_grid_is_after_markdown_content_by_default(self):
        pass

    @pytest.mark.parametrize("grid_configuration, expected_placement", [
        pytest.param(
            {}, "after", id="default_values"
        ),
        pytest.param(
            {"show_tiles_first": False}, "after", id="show_tiles_first_FALSE"
        ),
        pytest.param(
            {"show_tiles_first": True}, "before", id="show_tiles_first_TRUE"
        ),
        pytest.param(
            {"show_tiles_inline": True}, "inline", id="show_tiles_inline_TRUE"
        ),
        pytest.param(
            {
                "show_tiles_inline": True,
                "show_tiles_first": True
            }, "inline", id="inline_overrides_first"
        ),
    ])
    def test_that_grid_is_in_expected_place(self, grid_configuration, expected_placement):
        print(grid_configuration)
        print(expected_placement)
        pass
