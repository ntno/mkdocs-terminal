---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    text: 'close up of fallen leaves.'
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    text: 'close up of green moss on a log.'
  - caption: "Steve Richey"
    img_src: ../../../img/picsum/143_200x200.jpeg
    text: 'overhead of fallen leaves.'
---

# Image Only Tiles 
The tiles on this page do not have `link_*` attributes[^tile-reference].  They are rendered as a captioned images instead of linked images.

# Tiles First
The tiles on this page are placed before the main page content.  This is because the [grid option](../grid.md) `show_tiles_first` is set to `true`.

[^tile-reference]: see [Tile Reference](../tile.md)  


## Markdown

```markdown
---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    text: 'close up of fallen leaves.'
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    text: 'close up of green moss on a log.'
  - caption: "Steve Richey"
    img_src: ../../../img/picsum/143_200x200.jpeg
    text: 'overhead of fallen leaves.'
---
```