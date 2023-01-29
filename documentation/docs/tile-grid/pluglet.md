# Tile Grid Pluglet

By default the Terminal for MkDocs tile grid is displayed using logic in the theme's template definitions.  The theme's template definitions add extra content around the page's markdown content (for example, the side navigation bar or the latest git revision date for the page).

In order to affect what appears within the page's markdown content; i.e., inline, we can make use of the [MkDocs Macros Plugin].  This plugin, in combination with the theme's built-in Tile Grid Pluglet, will render the tile grid within a page's markdown content instead of before or after the markdown content.


[MkDocs Macros Plugin]: ../../configuration/plugins/macros
[MkDocs Macros Pluglet]: https://mkdocs-macros-plugin.readthedocs.io/en/latest/pluglets/

//todo - figure here

# Setup
Follow the instuctions in the [MkDocs Macros Plugin] documentation.  Then enable the Terminal for MkDocs Tile Grid Pluglet by adding  
```text
mkdocs-terminal:terminal.pluglets.tile_grid.main
```  
to the `modules` list option of the `macros` plugin:

```yaml
plugins:
  - search
  - macros:
      modules: 
        - mkdocs-terminal:terminal.pluglets.tile_grid.main
```

# Usage

## 1. Define Grid
Defined your tile grid according to the [Tile Grid Overview].  

[Tile Grid Overview]: ../

## 2. Configure Grid
Set `show_tiles_inline` to `true`.   

## 3. Call Tile_Grid Macro
Add a call to the `tile_grid` macro wherever on the page you would like the grid to be displayed:

```markdown
---
show_tiles_inline: true
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    img_title: 'to Picsum homepage'
    img_alt: 'close up of fallen leaves.'
    link_href: https://picsum.photos/ 
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    img_title: 'to Picsum homepage'
    img_alt: 'close up of green moss on a log.'
    link_href: https://picsum.photos/ 
  - caption: "Steve Richey"
    img_src: ../../../img/picsum/143_200x200.jpeg
    img_title: 'to Picsum homepage'
    img_alt: 'overhead of fallen leaves.'
    link_href: https://picsum.photos/
---

# My Inline Grid
{% raw %}{{ tile_grid(page.meta) }}{% endraw %}
```




