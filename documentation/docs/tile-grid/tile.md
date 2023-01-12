# Tile Reference
A tile can represent an image, a link, or a linked image.  

<br>

## Required Attributes

- `img_src` is required for a [image only] tile.  
- `link_href` is required for a [link only] tile.  
- `img_src` and `link_href` are required for a [linked image] tile.  

[image only]: examples/images-only.md
[link only]: examples/links-only.md
[linked image]: examples/example-page.md

<br>

## Optional Attributes

`caption`

:   The figure caption.

`img_src`

:   The image source.  Can be an external image like `https://picsum.photos/id/167/200/200` or an internal MkDocs image like `../img/palettes/default.png`.

`img_title`

:   Text to display on hover.

`img_alt`

:   Alternate text for the image if the image cannot be displayed.

`img_width`

:   Width to set on the image element.

`img_height`

:   Height to set on the image element.

`link_href`

:   Web page URL.  Can be an external web page or an internal MkDocs page like `./default/`.

`link_target`

:   Specifies where to open the linked webpage.  `_blank` will open the link in a new tab.  `_self` will open the link in the current window.

`link_text`

:   Text to display for a [link only] tile.  Ignored if `img_src` is specified.

`link_title`

:   Text to display on hover.  Should not be used if `img_title` is already specified.

`tile_id`

:   ID to add to the tile's HTML for advanced styling. See [Extra CSS] for example.  

`tile_css`

:   CSS class to add to the tile's HTML for advanced styling. See [Extra CSS] for example.  

[Extra CSS]: examples/links-only.md#extra-css