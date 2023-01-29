# Tile Grid Pluglet

By default the Terminal for MkDocs tile grid is displayed using logic in the theme's template definitions.  The theme's template definitions add extra content around the page's markdown content (for example, the side navigation bar or the latest git revision date for the page).

In order to affect what appears within the page's markdown content; i.e., inline, we can make use of the [MkDocs Macros Plugin].  This plugin, in combination with the theme's built-in Tile Grid Pluglet, will render the tile grid within a page's markdown content instead of before or after the markdown content.


[MkDocs Macros Plugin]: ../../configuration/plugins/macros
[MkDocs Macros Pluglet]: https://mkdocs-macros-plugin.readthedocs.io/en/latest/pluglets/

//todo - figure here

## Setup
install `mkdocs-macros-plugin`.
mkdocs.yml:

```
plugins:
  - md-to-html
  - macros:
      modules: 
        - mkdocs-terminal:terminal.pluglets.tile_grid.main
```

## Usage
`{% raw %}{{ tile_grid(page.meta) }}{% endraw %}`


## 4. Enable Built-In MkDocs

