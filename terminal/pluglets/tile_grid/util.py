from terminal.pluglets.tile_grid.tile import Tile
from terminal.pluglets.tile_grid.tile_grid import TileGrid


def grid(tiles_from_page_metadata):
    tile_list = []
    result = ""
    if tiles_from_page_metadata is not None:
        for tile in tiles_from_page_metadata:
            tile_list.append(Tile(tile))
        tile_grid = TileGrid(tile_list)
        return str(tile_grid)
    else:
        result="invalid_tiles_from_page_metadata"
    return result
