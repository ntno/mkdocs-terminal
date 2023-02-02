---
show_tiles_first: true
tiles:
  - caption: a captioned link
    link_href: https://github.com
  - caption: display specified text
    link_href: https://github.com
    alt_text: GitHub
  - caption: with tooltip
    link_href: ../example-page
    alt_text: Tile Grid Example
    tooltip: go to the tile grid example page
  - caption: "\\#tile_123"
    link_href: ../..
    alt_text: Tile Grid Overview
    tooltip: go to overview
    tile_id: "tile_123"
  - caption: "\\#tile_456"
    link_href: ../../tile
    alt_text: Tile Reference
    tooltip: go to tile reference
    tile_id: "tile_456"
  - caption: ".example_highlight"
    link_href: ../../grid
    alt_text: Grid Reference
    tooltip: go to grid reference
    tile_css: "example_highlight"
---
<style>
  #tile_456 {
    border: solid;
    border-width: thin;
  }

  .example_highlight {
    background-color: #FFFF00;
  } 
</style>
<hr>

# Link Only Tiles 
The tiles on this page do not have a `img_src` attribute.  They are rendered as captioned links instead of linked images.

To demonstrate how tiles can be styled individually, the following `<style>` HTML is included in this page's markdown:

## Extra CSS
```html
<style>
  #tile_456 {
    border: solid;
    border-width: thin;
  }

  .example_highlight {
    background-color: #FFFF00;
  } 
</style>
```

## Tile Markdown
Note:  

- `tile_id` has been set to `tile_456` in the second to last tile.  
- `tile_css` has been set to `example_highlight` in the last tile.  
```markdown
---
show_tiles_first: true
tiles:
  - caption: a captioned link
    link_href: https://github.com
  - caption: display specified text
    link_href: https://github.com
    alt_text: GitHub
  - caption: with tooltip
    link_href: ../example-page
    alt_text: Tile Grid Example
    tooltip: go to the tile grid example page
  - caption: "\\#tile_123"
    link_href: ../..
    alt_text: Tile Grid Overview
    tooltip: go to overview
    tile_id: "tile_123"
  - caption: "\\#tile_456"
    link_href: ../../tile
    alt_text: Tile Reference
    tooltip: go to tile reference
    tile_id: "tile_456"
  - caption: ".example_highlight"
    link_href: ../../grid
    alt_text: Grid Reference
    tooltip: go to grid reference
    tile_css: "example_highlight"
---
```
