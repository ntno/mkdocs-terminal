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

# Default Palette

The default color palette can be explicitly set by adding the `palette` attribute to your theme configuration in `mkdocs.yml`:

```yaml
theme:
  name: terminal
  palette: default
```

--8<--
elements/examples/index.md
--8<--

## Tile Grid Example
{{ tile_grid(page.meta) }}

<br>