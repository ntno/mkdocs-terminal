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
<!-- NOTE: [start:example]/[end:example] HTML comments support live example in snippets.md. -->
<!-- --8<-- [start:example] -->
--8<--
configuration/palettes/links.md
--8<--

# Gruvbox Dark Palette

To use the gruvbox_dark color palette, add the `palette` attribute to your theme configuration in `mkdocs.yml`:
<!-- --8<-- [end:example] -->
```yaml
theme:
  name: terminal
  palette: gruvbox_dark
```

<link href="../../../css/palettes/gruvbox_dark.css" rel="stylesheet">

--8<--
elements/examples/index.md
--8<--

## Tile Grid Example
{{ tile_grid(page.meta) }}

<br>