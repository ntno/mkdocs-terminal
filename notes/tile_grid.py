from __future__ import annotations
from typing import Optional, Any, List
from .tile import Tile


class TileGrid:
    def __init__(
        self, tiles: List[Tile], grid_id: Optional[Any]="", grid_css: Optional[Any]=""
    ) -> None:
        self.tiles = tiles
        self.grid_id = grid_id
        self.grid_css = grid_css
        

    def __repr__(self):
        grid_id = f"{self.grid_id}" if (
            self.grid_id is not "") else '[blank]'
        grid_css = f"{self.grid_css}" if (
            self.grid_css is not "") else '[blank]'
        tiles = f"{len(self.tiles)}" if (
            self.tiles is not None) else '[null]'
        return f"TileGrid(tiles='{tiles}', grid_id='{grid_id}', grid_css='{grid_css}')"


    tiles: List[Tile]
    """The grid's tiles."""

    grid_id: Optional[Any]
    """ID to add to the grid's HTML for advanced styling."""

    grid_css: Optional[Any]
    """CSS class to add to the grid's HTML for advanced styling."""
