---
show_tiles_first: true
tiles:
  - caption: a captioned link
    link_href: https://github.com
  - caption: display text specified
    alt_text: GitHub
    link_href: https://github.com
  - caption: with hover title
    tooltip: go to the tile grid example page
    alt_text: Tile Grid Example
    link_href: ../example-page
  - caption: "\\#tile_123"
    tile_id: "tile_123"
    tooltip: go to overview
    alt_text: Tile Grid Overview
    link_href: ../..
  - caption: "\\#tile_456"
    tile_id: "tile_456"
    tooltip: go to tile reference
    alt_text: Tile Reference
    link_href: ../../tile
  - caption: ".example_highlight"
    tile_css: "example_highlight"
    tooltip: go to grid reference
    alt_text: Grid Reference
    link_href: ../../grid
---
<style> #tile_456 {border: solid !important;border-width: thin !important;}.example_highlight {background-color: #FFFF00;}</style>
<hr>

# Link Only Tiles 
The tiles on this page do not have `img_*` attributes.  They are rendered as captioned links instead of linked images.

To demonstrate how tiles can be styled individually, the following `<style>` HTML is included in this page's markdown:

## Extra CSS
```html
<style>
  #tile_456 {
    border: solid !important;
    border-width: thin !important;
  }

  .example_highlight {
    background-color: #FFFF00;
  } 
</style>
```

## Tile Markdown

```markdown
---
show_tiles_first: true
tiles:
  - caption: a captioned link
    link_href: https://github.com
  - caption: display text specified
    alt_text: GitHub
    link_href: https://github.com
  - caption: with hover title
    tooltip: go to the tile grid example page
    alt_text: Tile Grid Example
    link_href: ../example-page
  - caption: "\\#tile_123"
    tile_id: "tile_123"
    tooltip: go to overview
    alt_text: Tile Grid Overview
    link_href: ../..
  - caption: "\\#tile_456"
    tile_id: "tile_456"
    tooltip: go to tile reference
    alt_text: Tile Reference
    link_href: ../../tile
  - caption: ".example_highlight"
    tile_css: "example_highlight"
    tooltip: go to grid reference
    alt_text: Grid Reference
    link_href: ../../grid
---
```
