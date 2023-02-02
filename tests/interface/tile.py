from __future__ import annotations

import logging
from typing import Optional, Any

log = logging.getLogger(__name__)


class Tile:
    def __init__(
        self, caption="", img_src="", link_href="", alt_text="", tooltip="", tile_id="", tile_css=""
    ) -> None:
        self.caption = caption
        self.img_src = img_src
        self.link_href = link_href
        self.alt_text = alt_text
        self.tooltip = tooltip
        self.tile_id = tile_id
        self.tile_css = tile_css

    def __repr__(self):
        link_href = f"'{self.link_href}'" if (
            self.link_href is not None) else '[blank]'
        caption = f"'{self.caption}'" if (
            self.caption is not None) else '[blank]'
        img_src = f"'{self.img_src}'" if (
            self.img_src is not None) else '[blank]'
        return f"Tile(caption={caption}, link_href={link_href}, img_src='{img_src}')"

    caption: Optional[Any]
    """The figure caption."""

    img_src: Optional[Any]
    """The image source.  Can be an external image like `https://picsum.photos/id/167/200/200` or an internal MkDocs image like `../img/palettes/default.png`."""

    link_href: Optional[Any]
    """Web page URL.  Can be an external web page or a relative internal MkDocs page like `./tile-grid/`"""

    alt_text: Optional[Any]
    """Text to display for a [link only] tile.  Image description for a [image only] tile.  Link description for a [linked image] tile."""

    tooltip: Optional[Any]
    """Text to display on hover."""

    tile_id: Optional[Any]
    """ID to add to the tile's HTML for advanced styling."""

    tile_css: Optional[Any]
    """CSS class to add to the tile's HTML for advanced styling."""
