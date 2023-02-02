---
show_tiles_inline: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    tooltip: 'to Picsum homepage'
    alt_text: 'Picsum Photo API.'
    link_href: https://picsum.photos/ 
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    tooltip: 'to Picsum homepage'
    alt_text: 'Picsum Photo API.'
    link_href: https://picsum.photos/ 
  - caption: "Steve Richey"
    img_src: ../../../img/picsum/143_200x200.jpeg
    tooltip: 'to Picsum homepage'
    alt_text: 'Picsum Photo API.'
    link_href: https://picsum.photos/
---

--8<--
configuration/palettes/links.md
--8<--

# Sans Dark Palette

To use the sans_dark color palette, add the `palette` attribute to your theme configuration in `mkdocs.yml`:

```yaml
theme:
  name: terminal
  palette: sans_dark
```

<link href="../../../css/palettes/sans_dark.css" rel="stylesheet">

--8<--
elements/examples/index.md
--8<--

## Tile Grid Example
{{ tile_grid(page.meta) }}

<br>