from copy import copy
DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"
USAGE_MESSAGE = "<p class=\"terminal-mkdocs-macro-error-banner\"><strong>USAGE:</strong>&nbsp;&nbsp;<code>{{ tile_grid(page.meta) }}</code></p>"


def tile_grid(page_meta):
    if page_meta is not None and isinstance(page_meta, dict) and len(page_meta.keys()) > 0:
        from terminal.pluglets.tile_grid.main import MACRO
        context_data = {
            "config": MACRO.get_mkdocs_config(),
            "page": {
                "meta": copy(page_meta)
            }
        }
        tiles_partial = MACRO.jinja2_env.get_template(DEFAULT_GRID_PARTIAL_PATH)
        rendered_grid = tiles_partial.render(context_data)
        return rendered_grid
    return USAGE_MESSAGE
