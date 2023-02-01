# Tile Reference
A tile can represent an image, a link, or a linked image.  

## Required Attributes

- `img_src` is required for a [image only] tile.  
- `link_href` is required for a [link only] tile.  
- `img_src` and `link_href` are required for a [linked image] tile.  

[image only]: examples/images-only.md
[link only]: examples/links-only.md
[linked image]: examples/example-page.md


## Optional Attributes

`caption`

:   The figure caption.

`img_src`

:   The image source.  Can be an external image like `https://picsum.photos/id/167/200/200` or an internal MkDocs image like `../img/palettes/default.png`.

`link_href`

:   The link destination.  Can be an external web page or a relative internal MkDocs page like `./tile-grid/`.

`text`

:   - **Image Only Tile** a short description of the image (used by screen readers and as a fallback value if the image cannot be loaded)
    - **Link Only Tile** the text to display for the hyperlink
    - **Linked Image Tile** the text which describes the purpose of the link (ex: for a image tile which is linked to a page about various dog breeds your alt text would be "Dog Breeds", *not* an extensive description of the image which may be a picture of a Golden Retriever)  

`title`

:   Text to display on hover.

`img_width`

:   Width to set on the image element.

`img_height`

:   Height to set on the image element.

`tile_id`

:   ID to add to the tile's HTML for advanced styling. See [Extra CSS] for example.  

`tile_css`

:   CSS class to add to the tile's HTML for advanced styling. See [Extra CSS] for example.  

[Extra CSS]: examples/links-only.md#extra-css