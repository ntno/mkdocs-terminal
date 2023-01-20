from terminal.pluglets.tile_grid.tile import Tile

def grid(tiles):
    if tiles is not None:
        t = Tile()
        t.validate()
        return "TODO: " + str(len(tiles))
    return "invalid_tiles"
