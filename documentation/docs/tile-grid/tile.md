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

:   The image source.  Can be an external image like `https://picsum.photos/id/167/200/200` or an internal MkDocs image like `../img/picsum/167_200x200.jpeg`.

`link_href`

:   The link destination.  Can be an external web page or a relative internal MkDocs page like `./tile-grid/`.

`alt_text`

:   **Image Only Tile**: a short description of the image.  
    **Link Only Tile**: the text to display for the hyperlink.  
    **Linked Image Tile**: text which describes the hyperlink destination.  
    For more information see [Alternate Text Resources](tile.md#alternate-text).  

`tooltip`

:   Text to display on hover.

`tile_id`

:   ID to add to the tile's HTML for advanced styling.  
    See [Extra CSS] for example.  

`tile_css`

:   CSS class to add to the tile's HTML for advanced styling.  
    See [Extra CSS] for example.  

[Extra CSS]: examples/links-only.md#extra-css


# Alternate Text

> Pages should provide effective text alternatives for screen readers in the form of alt text. When a screen reader encounters an image, it will attempt to read a text alternative.
> 
> Text alternatives are also important when images do not load. Users with cognitive impairments may prefer to disable images from loading. Likewise, images may not load when a user has a slow internet connection. In both cases, the browser will show the image’s alt text.
>
> [Yale Usability & Web Accessibility Guide](https://usability.yale.edu/web-accessibility/articles/images)

## Best Practices
- Be brief: less than 100 characters.  
- Avoid “image of”, “photo of”, "screenshot of", etc.
- ==Alternate text for image links should describe the purpose of the link, NOT the image.== 
    - If it is important to describe the image itself, add a description in the caption or in the surrounding text.
- Decorative images should have blank or empty alt text.

## Additional Resources

- [Guidance by Image Type/Function](https://www.w3.org/WAI/tutorials/images/)
- [The Importance of Context](https://webaim.org/techniques/alttext/#context)