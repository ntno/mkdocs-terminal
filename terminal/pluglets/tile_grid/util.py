from terminal.pluglets.tile_grid.tile import Tile
from terminal.pluglets.tile_grid.tile_grid import TileGrid



DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"





def grid(tiles_from_page_metadata):
    tile_list = []
    result = ""
    if tiles_from_page_metadata is not None:
        for tile in tiles_from_page_metadata:
            tile_list.append(Tile(tile))
        context_data = {
            "page": {
                "meta": {
                    "tiles": tile_list
                }
            }
        }
        # rendered_grid = partial_test.render(context_data)
        # print(rendered_grid)
        # direct return didn't work: '{{ {% include "pluglets/tile_grid/templates/j2-partials/tiles.html" %} }}'
        # direct return also didn't work "{% include \"pluglets/tile_grid/templates/j2-partials/tiles.html\" %}"
        # return "TODO " + str(len(tile_list))
        from terminal.pluglets.tile_grid import MACRO
        tiles_partial = MACRO.jinja2_env.get_template("pluglets/tile_grid/templates/j2-partials/tiles.html")
        rendered_grid = tiles_partial.render(context_data)
        return rendered_grid
    else:
        result="invalid_tiles_from_page_metadata"
    return result
