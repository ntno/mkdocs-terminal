---
show_tiles_first: true
tiles:
  - caption: a minimal link tile
    link_href: ../all-squares
  - caption: a link tile with text
    link_text: All Squares Example
    link_href: ../all-squares
  - caption: a link tile with hover title
    link_title: go to the all squares example
    link_text: All Squares Example
    link_href: ../all-squares
  - caption: new tab link tile
    link_target: "_blank"
    link_title: go to the misc sizes example in a new tab
    link_text: Misc. Sizes
    link_href: ../misc
  - caption: "#tile_123"
    id: "tile_123"
    link_target: "_self"
    link_title: go to tile overview in this window
    link_text: Tile Overview
    link_href: ..
  - caption: ".example_highlight"
    class: "example_highlight"
    link_target: "_blank"
    link_title: go to overview example in a new tab
    link_text: Overview Example
    link_href: ../example-page
---
<hr>
--8<--
elements/tile-grid/links.md
--8<--

<style>
  .example_highlight {
    background-color: #FFFF00;
  } 
</style>

# Link Only Tiles 
The tiles on this page do not have `img_*` attributes.  They are rendered as captioned links instead of linked images.

To demonstrate how tiles can be styled individually, the following `<style>` HTML is included in this page's markdown:

## Extra CSS
```html
<style>
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
    link_href: ../all-squares
  - caption: a link tile with text
    link_text: All Squares Example
    link_href: ../all-squares
  - caption: a link tile with hover title
    link_title: go to the all squares example
    link_text: All Squares Example
    link_href: ../all-squares
  - caption: new tab link tile
    link_target: "_blank"
    link_title: go to the misc sizes example in a new tab
    link_text: Misc. Sizes
    link_href: ../misc
  - caption: "#tile_123"
    id: "tile_123"
    link_target: "_self"
    link_title: go to tile overview in this window
    link_text: Tile Overview
    link_href: ..
  - caption: ".example_highlight"
    class: "example_highlight"
    link_target: "_blank"
    link_title: go to overview example in a new tab
    link_text: Overview Example
    link_href: ../example-page
```
