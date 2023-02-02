---
show_tiles_inline: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    tooltip: 'to Picsum homepage'
    text: 'close up of fallen leaves.'
    link_href: https://picsum.photos/ 
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    tooltip: 'to Picsum homepage'
    text: 'close up of green moss on a log.'
    link_href: https://picsum.photos/ 
  - caption: "Steve Richey"
    img_src: ../../../img/picsum/143_200x200.jpeg
    tooltip: 'to Picsum homepage'
    text: 'overhead of fallen leaves.'
    link_href: https://picsum.photos/
---

--8<--
configuration/palettes/links.md
--8<--

# Dark Palette

To use the dark color palette, add the `palette` attribute to your theme configuration in `mkdocs.yml`:

```yaml
theme:
  name: terminal
  palette: dark
```

<link href="../../../css/palettes/dark.css" rel="stylesheet">

--8<--
elements/examples/index.md
--8<--

## Tile Grid Example
{{ tile_grid(page.meta) }}

<br>