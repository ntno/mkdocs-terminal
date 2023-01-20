from terminal.pluglets.tile_grid.tile import Tile
from terminal.pluglets.tile_grid.tile_grid import TileGrid
from jinja2.environment import Environment
from jinja2 import loaders
from pathlib import Path
DEFAULT_GRID_PARTIAL_PATH = "pluglets/tile_grid/templates/j2-partials/tiles.html"

def grid(tiles_from_page_metadata):
    env = get_env()
    env.loader = pluglet_loader()
    partial_test = env.get_template(DEFAULT_GRID_PARTIAL_PATH)
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
        rendered_grid = partial_test.render(context_data)
        print(rendered_grid)
        return rendered_grid
    else:
        result="invalid_tiles_from_page_metadata"
    return result

def get_env():
    """returns a new environment"""
    return Environment()

def pluglet_loader():
    """returns FileSystemLoader initialized to the pluglet's template directory"""
    here = Path(__file__)
    print("util.py: ", str(here))
    pluglet_folder = here.parent
    print("pluglet folder: ", pluglet_folder)
    pluglets_folder = pluglet_folder.parent
    print("pluglets folder: ", pluglets_folder)
    terminal_folder = pluglets_folder.parent
    print("terminal theme folder: ", terminal_folder)
    return loaders.FileSystemLoader(terminal_folder.resolve())

