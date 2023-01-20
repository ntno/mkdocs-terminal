from terminal.pluglets.tile_grid.tile import Tile

def grid(tiles):
    if tiles is not None:
        for tile in tiles:
            Tile(tile).validate()
        return "TODO: " + str(len(tiles))
    return "invalid_tiles"
