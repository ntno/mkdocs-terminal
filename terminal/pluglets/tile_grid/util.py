from copy import copy
DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"
USAGE_MESSAGE = "<strong>USAGE:</strong> `{{ tile_grid(page.meta) }}`"


def tile_grid(page_meta):
    if page_meta is not None and isinstance(page_meta, dict) and len(page_meta.keys()) > 0:
        context_data = {
            "page": {
                "meta": copy(page_meta)
            }
        }
        from terminal.pluglets.tile_grid import MACRO
        tiles_partial = MACRO.jinja2_env.get_template(DEFAULT_GRID_PARTIAL_PATH)
        rendered_grid = tiles_partial.render(context_data)
        return rendered_grid
    return USAGE_MESSAGE
