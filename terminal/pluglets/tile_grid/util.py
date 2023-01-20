DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"

def tile_grid(mkdocs_context):
    from terminal.pluglets.tile_grid import MACRO
    tiles_partial = MACRO.jinja2_env.get_template(DEFAULT_GRID_PARTIAL_PATH)
    rendered_grid = tiles_partial.render(mkdocs_context)
    return rendered_grid

