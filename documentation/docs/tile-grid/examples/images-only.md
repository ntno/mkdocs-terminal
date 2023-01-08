---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
  - caption: 'Steve Richey'
    img_src: ../../../img/picsum/143_200x200.jpeg
---

<br>

# Image Only Tiles 
The tiles on this page do not have `link_*` attributes[^tile-reference].  They are rendered as a captioned images instead of linked images.

# Tiles First
The tiles on this page are placed before the main page content.  This is because the [grid option](../grid.md) `show_tiles_first` is set to `true`.

[^tile-reference]: see [Tile Reference](../tile.md)  

<br>

## Markdown

```markdown
---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
  - caption: 'Steve Richey'
    img_src: ../../../img/picsum/143_200x200.jpeg
---
```