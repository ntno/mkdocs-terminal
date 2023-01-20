from terminal.pluglets.tile_grid.tile import Tile

def grid(tiles):
    result = ""
    if tiles is not None:
        for tile in tiles:
            result = result + str(Tile(tile)) + "  \n"
    else:
        result="invalid_tiles"
    return result
