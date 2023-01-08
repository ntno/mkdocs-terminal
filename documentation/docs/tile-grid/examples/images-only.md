---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    img_src: https://picsum.photos/id/167/200/200
  - caption: 'Marcin Czerwinski'
    img_src: https://picsum.photos/id/127/200/200
  - caption: 'Steve Richey'
    img_src: https://picsum.photos/id/143/200/200
---
--8<--
tile-grid/examples/links.md
--8<--
<hr>

<br>

# Image Only Tiles 
The tiles on this page do not have `link_*` attributes.  They are rendered as a captioned images instead of linked images.

# Tiles First
The tiles on this page are placed before the main page content.  This is because the [grid option](../grid.md) `show_tiles_first` is set to `true`.

<br>

## Tile Markdown

```markdown
---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    img_src: https://picsum.photos/id/167/200/200
  - caption: 'Marcin Czerwinski'
    img_src: https://picsum.photos/id/127/200/200
  - caption: 'Steve Richey'
    img_src: https://picsum.photos/id/143/200/200
---
```