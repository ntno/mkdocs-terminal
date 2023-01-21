from copy import copy
DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"

def tile_grid(page_metadata={}):
    if page_metadata is not None and page_metadata is dict:
        context_data = {
            "page": {
                "meta": copy(page_metadata)
            }
        }
        from terminal.pluglets.tile_grid import MACRO
        tiles_partial = MACRO.jinja2_env.get_template(DEFAULT_GRID_PARTIAL_PATH)
        rendered_grid = tiles_partial.render(context_data)
        return rendered_grid
    else:
        return "USAGE: {{ tile_grid(page.meta) }}"
