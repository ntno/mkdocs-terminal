from tests.utils.html import assert_valid_html
# from tests.utils.filters import mock_markup_filter
from tests.interface import page_features, theme_plugins, theme_features
import pytest
PAGE_BASE_PARTIAL_PATH = "partials/page-base.html"
INLINE_MACRO_CALL = "{{ tile_grid(page.meta) }}"
BEFORE_CONTENT_SECTION = "<section id=\"mkdocs-terminal-before-content\" class=\"terminal-mkdocs-pad-to-match-side-nav\">"
CONTENT_SECTION = "<section id=\"mkdocs-terminal-content\">"
AFTER_CONTENT_SECTION = "<section id=\"mkdocs-terminal-after-content\">"
REVISION_SECTION = "<section id=\"mkdocs-terminal-revision\">"
GRID_DIV = "<div class=\"terminal-mkdocs-tile-grid \">"

@pytest.fixture
def page_base_partial(env_with_terminal_loader):
    return env_with_terminal_loader.get_template(PAGE_BASE_PARTIAL_PATH)


@pytest.fixture
def tiles(minimal_linked_image_tile, minimal_link_tile, minimal_image_tile):
    return [minimal_linked_image_tile, minimal_link_tile, minimal_image_tile]


@pytest.fixture
def fully_enabled_config():
    enabled_config = {
        "config": {
            "plugins": [theme_plugins.REVISION],
            "theme": {
                "features": [
                    theme_features.SHOW_REVISION_DATE
                ]
            }
        }
    }
    return enabled_config


def setup_jinja2_context(tiles, fully_enabled_config, grid_meta={}, include_macro_call=False):
    tiles_meta = {"tiles": [tiles]}
    revision_meta = {"revision_date": "revision_date_placeholder"}
    page_meta = {**grid_meta, **tiles_meta, **revision_meta}
    if(include_macro_call):
        page_content = "markdown_content_placeholder\n    " + INLINE_MACRO_CALL
    else:
        page_content = "markdown_content_placeholder" 
    context_data = {
        "page": {
            "content": page_content,
            "meta": page_meta
        },
        **fully_enabled_config
    }
    return context_data


def assert_markdown_content_in_page(html_fragment):
    assert CONTENT_SECTION in html_fragment
    assert "markdown_content_placeholder" in html_fragment


def assert_revision_in_page(html_fragment):
    assert REVISION_SECTION in html_fragment
    assert "revision_date_placeholder" in html_fragment


def assert_tile_grid_in_before_section(html_fragment):
    assert BEFORE_CONTENT_SECTION in html_fragment
    assert GRID_DIV in html_fragment
    assert AFTER_CONTENT_SECTION not in html_fragment
    # TODO - assert grid_indicator inside before_content section


def assert_tile_grid_in_after_section(html_fragment):
    assert AFTER_CONTENT_SECTION in html_fragment
    assert GRID_DIV in html_fragment
    assert BEFORE_CONTENT_SECTION not in html_fragment
    # TODO - assert grid_indicator inside after_content section


class TestGridPlacement():

    def test_that_grid_is_placed_after_markdown_by_default(self, page_base_partial, tiles, fully_enabled_config):
        context_data = setup_jinja2_context(tiles, fully_enabled_config)
        rendered_page = page_base_partial.render(context_data)
        assert_valid_html(rendered_page)
        assert_markdown_content_in_page(rendered_page)
        assert_revision_in_page(rendered_page)
        assert_tile_grid_in_after_section(rendered_page)
        

    @pytest.mark.parametrize("show_tiles_first", [
        pytest.param(
            False, id="Python_False"
        ),
        pytest.param(
            "false", id="YAML_false"
        ),
    ])    
    def test_that_grid_is_placed_after_markdown_when_show_first_is_false(self, show_tiles_first, page_base_partial, tiles, fully_enabled_config):
        context_data = setup_jinja2_context(tiles, fully_enabled_config, grid_meta={page_features.SHOW_TILES_FIRST: show_tiles_first})
        rendered_page = page_base_partial.render(context_data)
        assert_valid_html(rendered_page)
        assert_markdown_content_in_page(rendered_page)
        assert_revision_in_page(rendered_page)
        assert_tile_grid_in_after_section(rendered_page)

    @pytest.mark.parametrize("show_tiles_first", [
        pytest.param(
            True, id="Python_True"
        ),
        pytest.param(
            "true", id="YAML_true"
        ),
    ])    
    def test_that_grid_is_placed_before_markdown_when_show_first_is_true(self, show_tiles_first, page_base_partial, tiles, fully_enabled_config):
        context_data = setup_jinja2_context(tiles, fully_enabled_config, grid_meta={page_features.SHOW_TILES_FIRST: show_tiles_first})
        rendered_page = page_base_partial.render(context_data)
        assert_valid_html(rendered_page)
        assert_markdown_content_in_page(rendered_page)
        assert_revision_in_page(rendered_page)
        assert_tile_grid_in_before_section(rendered_page)


    # @pytest.mark.parametrize("grid_meta, with_macro_call, expected_placement", [
    #     pytest.param(
    #         {}, False, "after", id="no_values_set"
    #     ),
    #     pytest.param(
    #         {page_features.SHOW_TILES_FIRST: "false"}, False, "after", id="tiles_first_set_false"
    #     ),
    #     pytest.param(
    #         {page_features.SHOW_TILES_FIRST: "true"}, False, "before", id="tiles_first_set_true"
    #     ),
    #     pytest.param(
    #         {page_features.SHOW_TILES_INLINE: "true"}, True, "inline", id="tiles_inline_set_true"
    #     ),
    #     pytest.param(
    #         {
    #             page_features.SHOW_TILES_INLINE: "true",
    #             page_features.SHOW_TILES_FIRST: "true"
    #         }, 
    #         True,
    #         "inline", 
    #         id="tiles_inline_overrides_tiless_first"
    #     ),
    # ])
    # def test_that_grid_is_in_expected_place(self, grid_meta, with_macro_call, expected_placement, page_base_partial, tiles, fully_enabled_config):
    #     context_data = setup_jinja2_context(tiles, fully_enabled_config, grid_meta, with_macro_call)
    #     rendered_page = page_base_partial.render(context_data)
    #     assert_valid_html(rendered_page)
    #     assert_markdown_content_in_page(rendered_page)
    #     assert_revision_in_page(rendered_page)
    #     if (expected_placement == "before"):
    #         assert_tile_grid_in_before_section(rendered_page)
    #     elif (expected_placement == "after"):
    #         assert_tile_grid_in_after_section(rendered_page)
    #     elif (expected_placement == "inline"):
    #         assert BEFORE_CONTENT_SECTION not in rendered_page
    #         assert AFTER_CONTENT_SECTION not in rendered_page
    #         assert GRID_DIV not in rendered_page
    #         assert INLINE_MACRO_CALL in rendered_page
