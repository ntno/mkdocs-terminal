from copy import copy
DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"
USAGE_MESSAGE = "USAGE: {{ tile_grid(page.meta) }}"


def tile_grid(page_meta={}):
    if page_meta is None:
        return USAGE_MESSAGE
    if page_meta is not dict:
        return USAGE_MESSAGE
    if page_meta is {}:
        return USAGE_MESSAGE
    else:
        context_data = {
            "page": {
                "meta": copy(page_meta)
            }
        }
        from terminal.pluglets.tile_grid import MACRO
        tiles_partial = MACRO.jinja2_env.get_template(DEFAULT_GRID_PARTIAL_PATH)
        rendered_grid = tiles_partial.render(context_data)
        return rendered_grid
