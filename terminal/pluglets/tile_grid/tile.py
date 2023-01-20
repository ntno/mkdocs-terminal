from __future__ import annotations
from typing import Optional, Any
ATTRIBUTES_TO_MARKUP= ["caption", "link_text"]


class Tile:
    
    def __init__(
        self, blob, caption: Optional[Any]="", img_src: Optional[Any]="", img_title: Optional[Any]="", img_alt: Optional[Any]="", img_width: Optional[Any]="", img_height: Optional[Any]="", link_href: Optional[Any]="", link_target: Optional[Any]="", link_text: Optional[Any]="", link_title: Optional[Any]="", tile_id: Optional[Any]="", tile_css: Optional[Any]=""
    ) -> None:
        self.caption = caption
        self.img_src = img_src
        self.img_title = img_title
        self.img_alt = img_alt
        self.img_width = img_width
        self.img_height = img_height
        self.link_href = link_href
        self.link_target = link_target
        self.link_text = link_text
        self.link_title = link_title
        self.tile_id = tile_id
        self.tile_css = tile_css
        for key in blob:
            setattr(self, key, blob[key])

    def __repr__(self):
        link_href = f"'{self.link_href}'" if (
            self.link_href is not None) else '[blank]'
        caption = f"'{self.caption}'" if (
            self.caption is not None) else '[blank]'
        img_src = f"'{self.img_src}'" if (
            self.img_src is not None) else '[blank]'
        return f"Tile(caption={caption}, link_href={link_href}, img_src='{img_src}')"

    def validate(self):
        if self.link_href is "" and self.img_src is "":
            return False
        return True

    caption: Optional[Any]=""
    """The figure caption."""

    img_src: Optional[Any]=""
    """The image source.  Can be an external image like `https://picsum.photos/id/167/200/200` or an internal MkDocs image like `../img/palettes/default.png`."""

    img_title: Optional[Any]=""
    """Text to display on hover."""

    img_alt: Optional[Any]=""
    """Alternate text for the image if the image cannot be displayed."""

    img_width: Optional[Any]=""
    """Width to set on the image element."""

    img_height: Optional[Any]=""
    """Height to set on the image element."""

    link_href: Optional[Any]=""
    """Web page URL.  Can be an external web page or an internal MkDocs page like `./default/`."""

    link_target: Optional[Any]=""
    """Specifies where to open the linked webpage.  `_blank` will open the link in a new tab.  `_self` will open the link in the current window."""

    link_text: Optional[Any]=""
    """Text to display for a [link only] tile.  Ignored if `img_src` is specified."""

    link_title: Optional[Any]=""
    """Text to display on hover.  Should not be used if `img_title` is already specified."""

    tile_id: Optional[Any]=""
    """ID to add to the tile's HTML for advanced styling."""

    tile_css: Optional[Any]=""
    """CSS class to add to the tile's HTML for advanced styling."""
