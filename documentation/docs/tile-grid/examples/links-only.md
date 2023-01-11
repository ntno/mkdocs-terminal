---
show_tiles_first: true
tiles:
  - caption: a minimal link tile
    link_href: ../example-page
  - caption: a link tile with text
    link_text: Tile Grid Example
    link_href: ../example-page
  - caption: a link tile with hover title
    link_title: go to the tile grid example page
    link_text: Tile Grid Example
    link_href: ../example-page
  - caption: "#tile_123"
    div_id: "tile_123"
    link_target: "_self"
    link_title: go to overview in this window
    link_text: Tile Grid Overview
    link_href: ../..
  - caption: "#tile_456"
    div_id: "tile_456"
    link_target: "_self"
    link_title: go to tile reference in this window
    link_text: Tile Reference
    link_href: ../../tile
  - caption: ".example_highlight"
    div_css: "example_highlight"
    link_target: "_self"
    link_title: go to grid reference in this window
    link_text: Grid Reference
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
  - caption: a minimal link tile
    link_href: ../example-page
  - caption: a link tile with text
    link_text: Tile Grid Example
    link_href: ../example-page
  - caption: a link tile with hover title
    link_title: go to the tile grid example page
    link_text: Tile Grid Example
    link_href: ../example-page
  - caption: "#tile_123"
    div_id: "tile_123"
    link_target: "_self"
    link_title: go to overview in this window
    link_text: Tile Grid Overview
    link_href: ../..
  - caption: "#tile_456"
    div_id: "tile_456"
    link_target: "_self"
    link_title: go to tile reference in this window
    link_text: Tile Reference
    link_href: ../../tile
  - caption: ".example_highlight"
    div_css: "example_highlight"
    link_target: "_self"
    link_title: go to grid reference in this window
    link_text: Grid Reference
    link_href: ../../grid
---
```
