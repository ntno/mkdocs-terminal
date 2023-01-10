from __future__ import annotations

import logging
from typing import Optional

log = logging.getLogger(__name__)


class Tile:
    def __init__(
        self, caption="", img_src="", img_title="", img_alt="", link_href="", link_target="", link_text="", link_title="", html_id="", css_class=""
    ) -> None:
        self.caption = caption
        self.img_src = img_src
        self.img_title = img_title
        self.img_alt = img_alt
        self.link_href = link_href
        self.link_target = link_target
        self.link_text = link_text
        self.link_title = link_title
        self.html_id = html_id
        self.css_class = css_class

    def __repr__(self):
        link_href = f"'{self.link_href}'" if (
            self.link_href is not None) else '[blank]'
        caption = f"'{self.caption}'" if (
            self.caption is not None) else '[blank]'
        img_src = f"'{self.img_src}'" if (
            self.img_src is not None) else '[blank]'
        return f"Tile(caption={caption}, link_href={link_href}, img_src='{img_src}')"

    caption: Optional[str]
    """The figure caption."""

    img_src: Optional[str]
    """The image source.  Can be an external image like `https://picsum.photos/id/167/200/200` or an internal MkDocs image like `../img/palettes/default.png`."""

    img_title: Optional[str]
    """Text to display on hover."""

    img_alt: Optional[str]
    """Alternate text for the image if the image cannot be displayed."""

    link_href: Optional[str]
    """Web page URL.  Can be an external web page or an internal MkDocs page like `./default/`."""

    link_target: Optional[str]
    """Specifies where to open the linked webpage.  `_blank` will open the link in a new tab.  `_self` will open the link in the current window."""

    link_text: Optional[str]
    """Text to display for a [link only] tile.  Ignored if `img_src` is specified."""

    link_title: Optional[str]
    """Text to display on hover.  Should not be used if `img_title` is already specified."""

    html_id: Optional[str]
    """ID to add to the tile's HTML for advanced styling."""

    css_class: Optional[str]
    """CSS class to add to the tile's HTML for advanced styling."""
